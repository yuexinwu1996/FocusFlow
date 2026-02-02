//
//  AppActivityRecorder.swift
//  Dayflow
//
//  Basic mode data collector - tracks app names without screen capture.
//  No permissions required.
//

import Foundation
import AppKit
import Combine

/// Data structure for app activity observations
struct AppActivityData: Codable, Sendable {
    let timestamp: Date
    let appName: String
    let bundleIdentifier: String
    let windowTitle: String?
}

/// Records app activity for basic analysis mode.
/// Uses NSWorkspace to track frontmost application - no permissions needed.
final class AppActivityRecorder {
    static let shared = AppActivityRecorder()

    private var isTracking = false
    private var trackingTimer: Timer?
    private var cancellables = Set<AnyCancellable>()
    private let queue = DispatchQueue(label: "com.dayflow.appactivityrecorder", qos: .utility)

    /// Tracking interval in seconds (default: 10 seconds, same as screenshot interval)
    private let trackingInterval: TimeInterval = {
        let interval = UserDefaults.standard.double(forKey: "appActivityTrackingInterval")
        return interval > 0 ? interval : 10.0
    }()

    private var observations: [AppActivityData] = []
    private let maxObservations = 1000 // Keep last 1000 observations in memory

    private init() {
        setupAppStateObserver()
    }

    private func setupAppStateObserver() {
        // Observe AI Review enabled state and analysis mode
        Task { @MainActor in
            AppState.shared.$aiReviewEnabled
                .combineLatest(AppState.shared.$analysisMode)
                .removeDuplicates { $0.0 == $1.0 && $0.1 == $1.1 }
                .sink { [weak self] (enabled, mode) in
                    guard let self = self else { return }
                    if enabled && mode == .basic {
                        self.startTracking()
                    } else {
                        self.stopTracking()
                    }
                }
                .store(in: &cancellables)
        }
    }

    /// Start tracking app activity
    func startTracking() {
        guard !isTracking else { return }
        isTracking = true

        print("[AppActivityRecorder] Starting app activity tracking (interval: \(trackingInterval)s)")

        // Initial capture
        captureCurrentApp()

        // Schedule periodic captures
        DispatchQueue.main.async { [weak self] in
            guard let self = self else { return }
            self.trackingTimer = Timer.scheduledTimer(withTimeInterval: self.trackingInterval, repeats: true) { [weak self] _ in
                self?.captureCurrentApp()
            }
        }
    }

    /// Stop tracking app activity
    func stopTracking() {
        guard isTracking else { return }
        isTracking = false

        print("[AppActivityRecorder] Stopping app activity tracking")

        DispatchQueue.main.async { [weak self] in
            self?.trackingTimer?.invalidate()
            self?.trackingTimer = nil
        }
    }

    /// Capture current frontmost application
    private func captureCurrentApp() {
        queue.async { [weak self] in
            guard let self = self else { return }

            let workspace = NSWorkspace.shared
            guard let frontmostApp = workspace.frontmostApplication else {
                return
            }

            let appName = frontmostApp.localizedName ?? "Unknown"
            let bundleId = frontmostApp.bundleIdentifier ?? ""

            // Try to get window title (may be nil if not accessible)
            let windowTitle = self.getWindowTitle(for: frontmostApp)

            let data = AppActivityData(
                timestamp: Date(),
                appName: appName,
                bundleIdentifier: bundleId,
                windowTitle: windowTitle
            )

            self.observations.append(data)

            // Trim observations if exceeding max
            if self.observations.count > self.maxObservations {
                self.observations.removeFirst(self.observations.count - self.maxObservations)
            }

            print("[AppActivityRecorder] Captured: \(appName) - \(windowTitle ?? "no title")")
        }
    }

    /// Attempt to get window title for the application
    /// Note: This may require Accessibility permissions for full access
    private func getWindowTitle(for app: NSRunningApplication) -> String? {
        // For now, we'll just use the app name
        // Getting actual window title would require Accessibility API permissions
        // which defeats the purpose of "no permission needed" mode

        // Future enhancement: if user has granted Accessibility permission,
        // we could use AXUIElement to get actual window titles
        return nil
    }

    /// Get recent observations for a time range
    func getObservations(from startDate: Date, to endDate: Date) -> [AppActivityData] {
        return observations.filter { $0.timestamp >= startDate && $0.timestamp <= endDate }
    }

    /// Get all observations
    func getAllObservations() -> [AppActivityData] {
        return observations
    }

    /// Clear all observations
    func clearObservations() {
        queue.async { [weak self] in
            self?.observations.removeAll()
        }
    }

    /// Format observations as text for LLM processing
    func formatObservationsForLLM(from startDate: Date, to endDate: Date) -> String {
        let relevantObs = getObservations(from: startDate, to: endDate)

        guard !relevantObs.isEmpty else {
            return "No app activity recorded in this time period."
        }

        let formatter = DateFormatter()
        formatter.dateFormat = "h:mm a"

        // Group consecutive observations of the same app
        var grouped: [(app: String, start: Date, end: Date)] = []

        for obs in relevantObs {
            if let last = grouped.last, last.app == obs.appName {
                // Extend the last entry
                grouped[grouped.count - 1].end = obs.timestamp
            } else {
                // New entry
                grouped.append((app: obs.appName, start: obs.timestamp, end: obs.timestamp))
            }
        }

        // Format as text
        return grouped.map { entry in
            let startStr = formatter.string(from: entry.start)
            let endStr = formatter.string(from: entry.end)
            return "[\(startStr) - \(endStr)]: Using \(entry.app)"
        }.joined(separator: "\n")
    }
}
