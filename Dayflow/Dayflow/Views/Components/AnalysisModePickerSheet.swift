//
//  AnalysisModePickerSheet.swift
//  Dayflow
//
//  Modal sheet for selecting AI Review analysis mode.
//

import SwiftUI

struct AnalysisModePickerSheet: View {
    @Binding var isPresented: Bool
    var onModeSelected: (AnalysisMode) -> Void
    var onCancel: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            // Header
            VStack(alignment: .leading, spacing: 6) {
                Text("analysis_mode_title")
                    .font(.custom("InstrumentSerif-Regular", size: 24))
                    .foregroundColor(Color(hex: "333333"))

                Text("analysis_mode_subtitle")
                    .font(.custom("Nunito", size: 13))
                    .foregroundColor(Color(hex: "707070"))
            }

            // Mode options
            VStack(spacing: 12) {
                // Basic mode (recommended)
                AnalysisModeCard(
                    mode: .basic,
                    isRecommended: true,
                    title: String(localized: "analysis_mode_basic"),
                    description: String(localized: "analysis_mode_basic_desc"),
                    icon: "app.badge",
                    iconColor: Color(hex: "42D0BB")
                ) {
                    onModeSelected(.basic)
                    isPresented = false
                }

                // Advanced mode
                AnalysisModeCard(
                    mode: .advanced,
                    isRecommended: false,
                    title: String(localized: "analysis_mode_advanced"),
                    description: String(localized: "analysis_mode_advanced_desc"),
                    icon: "rectangle.dashed.badge.record",
                    iconColor: Color(hex: "F96E00"),
                    badge: String(localized: "analysis_mode_needs_permission")
                ) {
                    onModeSelected(.advanced)
                    isPresented = false
                }
            }

            // Cancel button
            Button(action: {
                onCancel()
                isPresented = false
            }) {
                Text("cancel")
                    .font(.custom("Nunito", size: 14).weight(.medium))
                    .foregroundColor(Color(hex: "707070"))
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 10)
            }
            .buttonStyle(.plain)
        }
        .padding(24)
        .frame(width: 340)
        .background(
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .fill(Color(red: 0.98, green: 0.97, blue: 0.96))
                .shadow(color: .black.opacity(0.15), radius: 20, x: 0, y: 10)
        )
        .overlay(
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .stroke(Color(red: 0.91, green: 0.88, blue: 0.87), lineWidth: 1)
        )
    }
}

private struct AnalysisModeCard: View {
    let mode: AnalysisMode
    let isRecommended: Bool
    let title: String
    let description: String
    let icon: String
    let iconColor: Color
    var badge: String? = nil
    let action: () -> Void

    @State private var isHovered = false

    var body: some View {
        Button(action: action) {
            HStack(alignment: .top, spacing: 14) {
                // Icon
                ZStack {
                    Circle()
                        .fill(iconColor.opacity(0.15))
                        .frame(width: 44, height: 44)

                    Image(systemName: icon)
                        .font(.system(size: 20, weight: .medium))
                        .foregroundColor(iconColor)
                }

                // Content
                VStack(alignment: .leading, spacing: 4) {
                    HStack(spacing: 6) {
                        Text(title)
                            .font(.custom("Nunito", size: 15).weight(.semibold))
                            .foregroundColor(Color(hex: "333333"))

                        if isRecommended {
                            Text("analysis_mode_recommended")
                                .font(.custom("Nunito", size: 11).weight(.medium))
                                .foregroundColor(.white)
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(
                                    Capsule()
                                        .fill(Color(hex: "42D0BB"))
                                )
                        }
                    }

                    Text(description)
                        .font(.custom("Nunito", size: 12))
                        .foregroundColor(Color(hex: "707070"))
                        .fixedSize(horizontal: false, vertical: true)

                    if let badge = badge {
                        HStack(spacing: 4) {
                            Image(systemName: "lock.shield")
                                .font(.system(size: 10))
                            Text(badge)
                                .font(.custom("Nunito", size: 10))
                        }
                        .foregroundColor(Color(hex: "F96E00"))
                        .padding(.top, 2)
                    }
                }

                Spacer()

                // Arrow
                Image(systemName: "chevron.right")
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(Color(hex: "CCCCCC"))
            }
            .padding(14)
            .background(
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .fill(isHovered ? Color.white : Color.white.opacity(0.7))
            )
            .overlay(
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .stroke(
                        isHovered ? iconColor.opacity(0.5) : Color(red: 0.91, green: 0.88, blue: 0.87),
                        lineWidth: isHovered ? 1.5 : 1
                    )
            )
        }
        .buttonStyle(.plain)
        .onHover { hovering in
            withAnimation(.easeInOut(duration: 0.15)) {
                isHovered = hovering
            }
        }
    }
}

#Preview("Analysis Mode Picker Sheet") {
    ZStack {
        Color(red: 0.5, green: 0.5, blue: 0.5).opacity(0.3)
            .ignoresSafeArea()

        AnalysisModePickerSheet(
            isPresented: .constant(true),
            onModeSelected: { mode in
                print("Selected mode: \(mode)")
            },
            onCancel: {
                print("Cancelled")
            }
        )
    }
}
