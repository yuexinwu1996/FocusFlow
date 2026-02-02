import SwiftUI
import Combine

/// Analysis mode for AI Review feature
enum AnalysisMode: String, Codable, CaseIterable {
    case basic = "basic"       // Basic analysis - app names only, no permission needed
    case advanced = "advanced" // Advanced analysis - screen capture, requires permission
}

@MainActor // <--- Add this
protocol AppStateManaging: ObservableObject {
    // This requirement must now be fulfilled on the main actor
    var isRecording: Bool { get }
    var objectWillChange: ObservableObjectPublisher { get }
}

@MainActor
final class AppState: ObservableObject, AppStateManaging { // <-- Add AppStateManaging here
    static let shared = AppState()

    private let recordingKey = "isRecording"
    private let aiReviewEnabledKey = "aiReviewEnabled"
    private let analysisModeKey = "analysisMode"
    private var shouldPersist = false

    @Published var isRecording: Bool {
        didSet {
            // Only persist after onboarding is complete
            if shouldPersist {
                UserDefaults.standard.set(isRecording, forKey: recordingKey)
            }
        }
    }

    /// AI Review feature toggle - default OFF
    @Published var aiReviewEnabled: Bool = false {
        didSet {
            if shouldPersist {
                UserDefaults.standard.set(aiReviewEnabled, forKey: aiReviewEnabledKey)
            }
        }
    }

    /// Analysis mode - basic (app names only) or advanced (screen capture)
    @Published var analysisMode: AnalysisMode = .basic {
        didSet {
            if shouldPersist {
                UserDefaults.standard.set(analysisMode.rawValue, forKey: analysisModeKey)
            }
        }
    }

    private init() {
        // Always start with false - AppDelegate will set the correct value
        // didSet doesn't fire during initialization, so this won't save
        self.isRecording = false
        self.aiReviewEnabled = false
        self.analysisMode = .basic
    }

    /// Enable persistence after onboarding is complete
    func enablePersistence() {
        shouldPersist = true
    }

    /// Get the saved recording preference, if any
    func getSavedPreference() -> Bool? {
        if UserDefaults.standard.object(forKey: recordingKey) != nil {
            return UserDefaults.standard.bool(forKey: recordingKey)
        }
        return nil
    }

    /// Get saved AI Review enabled state
    func getSavedAIReviewEnabled() -> Bool? {
        if UserDefaults.standard.object(forKey: aiReviewEnabledKey) != nil {
            return UserDefaults.standard.bool(forKey: aiReviewEnabledKey)
        }
        return nil
    }

    /// Get saved analysis mode
    func getSavedAnalysisMode() -> AnalysisMode? {
        if let rawValue = UserDefaults.standard.string(forKey: analysisModeKey) {
            return AnalysisMode(rawValue: rawValue)
        }
        return nil
    }

    /// Restore AI Review settings from saved preferences
    func restoreAIReviewSettings() {
        if let savedEnabled = getSavedAIReviewEnabled() {
            aiReviewEnabled = savedEnabled
        }
        if let savedMode = getSavedAnalysisMode() {
            analysisMode = savedMode
        }
    }
}
