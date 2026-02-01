//
//  LLMProviderSetupView.swift
//  Dayflow
//
//  LLM provider setup flow with step-by-step configuration
//

import SwiftUI
import Foundation
import AppKit

struct CLIResult {
    let stdout: String
    let stderr: String
    let exitCode: Int32
}

/// Run a CLI command via login shell.
/// This replicates Terminal.app behavior - if user can run it in Terminal, it works here.
@discardableResult
func runCLI(
    _ command: String,
    args: [String] = [],
    env: [String: String]? = nil,
    cwd: URL? = nil
) throws -> CLIResult {
    // Build the full command with args
    let cmdParts = [command] + args.map { LoginShellRunner.shellEscape($0) }
    var fullCommand = cmdParts.joined(separator: " ")

    // Add environment variable exports if provided
    if let env = env, !env.isEmpty {
        let envExports = env.map { key, value in
            "\(key)=\(LoginShellRunner.shellEscape(value))"
        }.joined(separator: " ")
        fullCommand = "\(envExports) \(fullCommand)"
    }

    // Add cd if working directory specified
    if let cwd = cwd {
        fullCommand = "cd \(LoginShellRunner.shellEscape(cwd.path)) && \(fullCommand)"
    }

    let result = LoginShellRunner.run(fullCommand, timeout: 60)
    return CLIResult(stdout: result.stdout, stderr: result.stderr, exitCode: result.exitCode)
}

/// Streaming CLI runner that uses login shell for Terminal.app-like behavior.
final class StreamingCLI {
    private var process: Process?
    private let stdoutPipe = Pipe()
    private let stderrPipe = Pipe()

    func cancel() {
        process?.terminate()
    }

    /// Run a command via login shell with streaming output.
    /// - Parameters:
    ///   - command: The command name (e.g., "codex", "claude") - no path needed
    ///   - args: Arguments to pass to the command
    ///   - env: Optional environment variable overrides
    ///   - cwd: Optional working directory
    ///   - onStdout: Callback for stdout chunks
    ///   - onStderr: Callback for stderr chunks
    ///   - onFinish: Callback when process exits with exit code
    func run(
        command: String,
        args: [String],
        env: [String: String]? = nil,
        cwd: URL? = nil,
        onStdout: @escaping (String) -> Void,
        onStderr: @escaping (String) -> Void,
        onFinish: @escaping (Int32) -> Void
    ) {
        let proc = Process()
        process = proc

        // Build shell command from command + args
        let cmdParts = [command] + args.map { LoginShellRunner.shellEscape($0) }
        var shellCommand = cmdParts.joined(separator: " ")

        // Add environment exports if provided
        if let env = env, !env.isEmpty {
            let envExports = env.map { key, value in
                "\(key)=\(LoginShellRunner.shellEscape(value))"
            }.joined(separator: " ")
            shellCommand = "\(envExports) \(shellCommand)"
        }

        // Add cd if working directory specified
        if let cwd = cwd {
            shellCommand = "cd \(LoginShellRunner.shellEscape(cwd.path)) && \(shellCommand)"
        }

        proc.executableURL = URL(fileURLWithPath: "/bin/zsh")
        // -l = login shell (sources .zprofile), -i = interactive (sources .zshrc)
        // Both are needed because PATH setup can be in either file
        proc.arguments = ["-l", "-i", "-c", shellCommand]
        proc.standardInput = FileHandle.nullDevice

        proc.standardOutput = stdoutPipe
        proc.standardError = stderrPipe

        stdoutPipe.fileHandleForReading.readabilityHandler = { handle in
            let data = handle.availableData
            guard !data.isEmpty, let chunk = String(data: data, encoding: .utf8) else { return }
            DispatchQueue.main.async {
                onStdout(chunk)
            }
        }

        stderrPipe.fileHandleForReading.readabilityHandler = { handle in
            let data = handle.availableData
            guard !data.isEmpty, let chunk = String(data: data, encoding: .utf8) else { return }
            DispatchQueue.main.async {
                onStderr(chunk)
            }
        }

        do {
            try proc.run()
            proc.terminationHandler = { process in
                self.stdoutPipe.fileHandleForReading.readabilityHandler = nil
                self.stderrPipe.fileHandleForReading.readabilityHandler = nil
                DispatchQueue.main.async {
                    onFinish(process.terminationStatus)
                }
            }
        } catch {
            DispatchQueue.main.async {
                onStderr("Failed to start \(command): \(error.localizedDescription)")
                onFinish(-1)
            }
        }
    }
}

struct LLMProviderSetupView: View {
    let providerType: String // "ollama" or "gemini"
    let onBack: () -> Void
    let onComplete: () -> Void
    
    private var activeProviderType: String { providerType }
    
    private var headerTitle: String {
        switch activeProviderType {
        case "ollama":
            return String(localized: "setup_header_local")
        case "chatgpt_claude":
            return String(localized: "setup_header_cli")
        default:
            return String(localized: "setup_header_gemini")
        }
    }
    
    // Layout constants
    private let sidebarWidth: CGFloat = 250
    private let fixedOffset: CGFloat = 50
    
    @StateObject private var setupState = ProviderSetupState()
    @State private var sidebarOpacity: Double = 0
    @State private var contentOpacity: Double = 0
    @State private var nextButtonHovered: Bool = false // legacy, unused after refactor
    @State private var googleButtonHovered: Bool = false // legacy, unused after refactor
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Header with Back button and Title on same line
            HStack(alignment: .center, spacing: 0) {
                // Back button container matching sidebar width
                HStack {
                    Button(action: handleBack) {
                        HStack(spacing: 12) {
                            Image(systemName: "chevron.left")
                                .font(.system(size: 12, weight: .semibold))
                                .foregroundColor(.black.opacity(0.7))
                                .frame(width: 20, alignment: .center)
                            
                            Text("back")
                                .font(.custom("Nunito", size: 15))
                                .fontWeight(.medium)
                                .foregroundColor(.black.opacity(0.7))
                        }
                    }
                    .buttonStyle(.plain)
                    // Position where sidebar items start: 20 + 16 = 36px
                    .padding(.leading, 36) // Align with sidebar item structure
                    .pointingHandCursor()
                    
                    Spacer()
                }
                .frame(width: sidebarWidth)
                
                // Title in the content area
                HStack {
                    Text(headerTitle)
                        .font(.custom("Nunito", size: 32))
                        .fontWeight(.semibold)
                        .foregroundColor(.black.opacity(0.9))
                    
                    Spacer()
                }
                .padding(.leading, 40) // Gap between sidebar and content
            }
            .padding(.leading, fixedOffset)
            .padding(.top, fixedOffset)
            .padding(.bottom, 40)
            
            // Main content area with sidebar and content
            HStack(alignment: .top, spacing: 40) {
                // Sidebar - fixed width 250px
                VStack(alignment: .leading, spacing: 0) {
                    SetupSidebarView(
                        steps: setupState.steps,
                        currentStepId: setupState.currentStep.id,
                        onStepSelected: { setupState.navigateToStep($0) }
                    )
                    Spacer()
                }
                .frame(width: sidebarWidth)
                .opacity(sidebarOpacity)
                
                // Content area - wrapped in VStack to match sidebar alignment
                VStack(alignment: .leading, spacing: 0) {
                    currentStepContent
                        .frame(maxWidth: 500, alignment: .leading)
                    Spacer()
                }
                .opacity(contentOpacity)
                .textSelection(.enabled)
            }
            .padding(.leading, fixedOffset)
            
            Spacer() // Push everything to top
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .onAppear {
            setupState.configureSteps(for: activeProviderType)
            animateAppearance()
        }
        .preferredColorScheme(.light)
    }
    
    private var nextButtonText: String {
        if let title = setupState.currentStep.contentType.informationTitle {
            if (title == "Testing" || title == "Test Connection") && !setupState.testSuccessful {
                return String(localized: "test_required")
            }
        }
        return String(localized: "next")
    }
    
    @ViewBuilder
    private var nextButton: some View {
        if setupState.isLastStep {
            DayflowSurfaceButton(
                action: { saveConfiguration(); onComplete() },
                content: {
                    HStack(spacing: 8) {
                        Image(systemName: "checkmark.circle.fill").font(.system(size: 14))
                        Text("complete_setup").font(.custom("Nunito", size: 14)).fontWeight(.semibold)
                    }
                },
                background: Color(red: 0.25, green: 0.17, blue: 0),
                foreground: .white,
                borderColor: .clear,
                cornerRadius: 8,
                horizontalPadding: 24,
                verticalPadding: 12,
                showOverlayStroke: true
            )
        } else {
            DayflowSurfaceButton(
                action: handleContinue,
                content: {
                    HStack(spacing: 6) {
                        Text(nextButtonText).font(.custom("Nunito", size: 14)).fontWeight(.semibold)
                        if nextButtonText == String(localized: "next") {
                            Image(systemName: "chevron.right").font(.system(size: 12, weight: .medium))
                        }
                    }
                },
                background: Color(red: 0.25, green: 0.17, blue: 0),
                foreground: .white,
                borderColor: .clear,
                cornerRadius: 8,
                horizontalPadding: 24,
                verticalPadding: 12,
                showOverlayStroke: true
            )
            .disabled(!setupState.canContinue)
            .opacity(!setupState.canContinue ? 0.5 : 1.0)
        }
    }
    
    @ViewBuilder
    private var currentStepContent: some View {
        let step = setupState.currentStep
        
        switch step.contentType {
        case .localChoice:
            VStack(alignment: .leading, spacing: 20) {
                VStack(alignment: .leading, spacing: 8) {
                    Text("local_choose_engine_title")
                        .font(.custom("Nunito", size: 24))
                        .fontWeight(.semibold)
                        .foregroundColor(.black.opacity(0.9))
                    Text("local_choose_engine_subtitle")
                        .font(.custom("Nunito", size: 14))
                        .foregroundColor(.black.opacity(0.6))
                }
                HStack(alignment: .center, spacing: 12) {
                    DayflowSurfaceButton(
                        action: { setupState.selectEngine(.lmstudio); openLMStudioDownload() },
                        content: {
                            AsyncImage(url: URL(string: "https://lmstudio.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Flmstudio-app-logo.11b4d746.webp&w=96&q=75")) { phase in
                                switch phase {
                                case .success(let image): image.resizable().scaledToFit()
                                case .failure(_): Image(systemName: "desktopcomputer").resizable().scaledToFit().foregroundColor(.white.opacity(0.6))
                                case .empty: ProgressView().scaleEffect(0.7)
                                @unknown default: EmptyView()
                                }
                            }
                            .frame(width: 18, height: 18)
                            Text("local_download_lmstudio")
                                .font(.custom("Nunito", size: 14))
                                .fontWeight(.semibold)
                        },
                        background: Color(red: 0.25, green: 0.17, blue: 0),
                        foreground: .white,
                        borderColor: .clear,
                        cornerRadius: 8,
                        showOverlayStroke: true
                    )
                }
                Text("local_have_server_note")
                    .font(.custom("Nunito", size: 13))
                    .foregroundColor(.black.opacity(0.6))
                HStack { Spacer(); nextButton }
            }
        case .localModelInstall:
            VStack(alignment: .leading, spacing: 16) {
                Text("local_install_qwen_title")
                    .font(.custom("Nunito", size: 24))
                    .fontWeight(.semibold)
                    .foregroundColor(.black.opacity(0.9))
                if setupState.localEngine == .ollama {
                    Text("local_install_ollama_subtitle")
                        .font(.custom("Nunito", size: 14))
                        .foregroundColor(.black.opacity(0.6))
                    TerminalCommandView(
                        title: String(localized: "terminal_run_this"),
                        subtitle: String(localized: "terminal_downloads_qwen"),
                        command: "ollama pull qwen3-vl:4b"
                    )
                } else if setupState.localEngine == .lmstudio {
                    VStack(alignment: .leading, spacing: 16) {
                        Text("local_install_lmstudio_subtitle")
                            .font(.custom("Nunito", size: 14))
                            .foregroundColor(.black.opacity(0.6))

                        DayflowSurfaceButton(
                            action: openLMStudioModelDownload,
                            content: {
                                HStack(spacing: 8) {
                                    Image(systemName: "arrow.down.circle.fill").font(.system(size: 14))
                                    Text("local_download_qwen_lmstudio").font(.custom("Nunito", size: 14)).fontWeight(.semibold)
                                }
                            },
                            background: Color(red: 0.25, green: 0.17, blue: 0),
                            foreground: .white,
                            borderColor: .clear,
                            cornerRadius: 8,
                            horizontalPadding: 24,
                            verticalPadding: 12,
                            showOverlayStroke: true
                        )

                        VStack(alignment: .leading, spacing: 6) {
                            Text("local_lmstudio_open_prompt")
                                .font(.custom("Nunito", size: 13))
                                .foregroundColor(.black.opacity(0.65))

                            Text("local_lmstudio_turn_on_server")
                                .font(.custom("Nunito", size: 13))
                                .foregroundColor(.black.opacity(0.65))
                        }
                        .padding(.top, 4)

                        // Fallback manual instructions
                        VStack(alignment: .leading, spacing: 4) {
                            Text("local_manual_setup")
                                .font(.custom("Nunito", size: 12))
                                .fontWeight(.semibold)
                                .foregroundColor(.black.opacity(0.5))
                            Text("local_manual_step1")
                                .font(.custom("Nunito", size: 12))
                                .foregroundColor(.black.opacity(0.45))
                            Text("local_manual_step2")
                                .font(.custom("Nunito", size: 12))
                                .foregroundColor(.black.opacity(0.45))
                        }
                        .padding(.top, 8)
                    }
                } else {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("local_use_any_vlm_title")
                            .font(.custom("Nunito", size: 16))
                            .fontWeight(.semibold)
                            .foregroundColor(.black.opacity(0.85))
                        Text("local_use_any_vlm_subtitle")
                            .font(.custom("Nunito", size: 14))
                            .foregroundColor(.black.opacity(0.75))
                    }
                }
                HStack { Spacer(); nextButton }
            }
        case .terminalCommand(let command):
            VStack(alignment: .leading, spacing: 24) {
                TerminalCommandView(
                    title: String(localized: "terminal_command_title"),
                    subtitle: String(localized: "terminal_copy_instruction"),
                    command: command
                )
                
                HStack {
                    Spacer()
                    nextButton
                }
            }
            
        case .apiKeyInput:
            VStack(alignment: .leading, spacing: 24) {
                APIKeyInputView(
                    apiKey: $setupState.apiKey,
                    title: String(localized: "gemini_enter_key_title"),
                    subtitle: String(localized: "gemini_enter_key_subtitle"),
                    placeholder: "AIza...",
                    onValidate: { key in
                        // Basic validation for now
                        return key.hasPrefix("AIza") && key.count > 30
                    }
                )

                VStack(alignment: .leading, spacing: 12) {
                    Text("gemini_model_choice")
                        .font(.custom("Nunito", size: 16))
                        .fontWeight(.semibold)
                        .foregroundColor(.black.opacity(0.85))

                    Picker("Gemini model", selection: $setupState.geminiModel) {
                        ForEach(GeminiModel.allCases, id: \.self) { model in
                            Text(model.shortLabel).tag(model)
                        }
                    }
                    .pickerStyle(.segmented)

                    Text(GeminiModelPreference(primary: setupState.geminiModel).fallbackSummary)
                        .font(.custom("Nunito", size: 13))
                        .foregroundColor(.black.opacity(0.55))
                }
                .onChange(of: setupState.geminiModel) {
                    setupState.persistGeminiModelSelection(source: "onboarding_picker")
                }
                
                HStack {
                    Spacer()
                    nextButton
                }
            }
            
        case .modelDownload(let command):
            VStack(alignment: .leading, spacing: 24) {
                VStack(alignment: .leading, spacing: 8) {
                    Text("model_download_title")
                        .font(.custom("Nunito", size: 24))
                        .fontWeight(.semibold)
                        .foregroundColor(.black.opacity(0.9))

                    Text("model_download_subtitle")
                        .font(.custom("Nunito", size: 14))
                        .foregroundColor(.black.opacity(0.6))
                }

                TerminalCommandView(
                    title: String(localized: "terminal_run_this"),
                    subtitle: "This will download the \(LocalModelPreset.qwen3VL4B.displayName) model (about 5GB)",
                    command: command
                )
                
                HStack {
                    Spacer()
                    nextButton
                }
            }
            
        case .information(let title, let description):
            VStack(alignment: .leading, spacing: 24) {
                VStack(alignment: .leading, spacing: 16) {
                    Text(title)
                        .font(.custom("Nunito", size: 24))
                        .fontWeight(.semibold)
                        .foregroundColor(.black.opacity(0.9))
                    if !description.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
                        Text(description)
                            .font(.custom("Nunito", size: 14))
                            .foregroundColor(.black.opacity(0.6))
                            .fixedSize(horizontal: false, vertical: true)
                            .multilineTextAlignment(.leading)
                            .lineLimit(nil)
                        // Additional guidance for the local intro step only
                        if step.id == "intro" && providerType == "ollama" {
                            (
                                Text("local_advanced_users_prefix") +
                                Text("local_vision_capable").fontWeight(.bold) +
                                Text("local_advanced_users_suffix")
                            )
                            .font(.custom("Nunito", size: 14))
                            .foregroundColor(.black.opacity(0.6))
                            .fixedSize(horizontal: false, vertical: true)
                            .multilineTextAlignment(.leading)
                        }
                    }
                }

                // Content area scrolls if needed; Next stays visible below
                ScrollView(.vertical, showsIndicators: true) {
                    VStack(alignment: .leading, spacing: 16) {
                        if title == "Testing" || title == "Test Connection" {
                            if providerType == "gemini" {
                                TestConnectionView(
                                    onTestComplete: { success in
                                        setupState.hasTestedConnection = true
                                        setupState.testSuccessful = success
                                    }
                                )
                            } else if providerType == "chatgpt_claude" {
                                ChatCLITestView(
                                    selectedTool: setupState.preferredCLITool,
                                    onTestComplete: { success in
                                        setupState.hasTestedConnection = true
                                        setupState.testSuccessful = success
                                    }
                                )
                            } else {
                                // Engine selection: LM Studio or Custom
                                VStack(alignment: .leading, spacing: 12) {
                                    Text("local_which_tool")
                                        .font(.custom("Nunito", size: 14))
                                        .foregroundColor(.black.opacity(0.65))
                                    Picker("Engine", selection: $setupState.localEngine) {
                                        Text("local_lm_studio").tag(LocalEngine.lmstudio)
                                        Text("local_custom_model").tag(LocalEngine.custom)
                                    }
                                    .pickerStyle(.segmented)
                                    .frame(maxWidth: 380)
                                }
                                .onChange(of: setupState.localEngine) { _, newValue in
                                    setupState.selectEngine(newValue)
                                }

                                LocalLLMTestView(
                                    baseURL: $setupState.localBaseURL,
                                    modelId: $setupState.localModelId,
                                    apiKey: $setupState.localAPIKey,
                                    engine: setupState.localEngine,
                                    showInputs: setupState.localEngine == .custom,
                                    onTestComplete: { success in
                                        setupState.hasTestedConnection = true
                                        setupState.testSuccessful = success
                                    }
                                )
                            }
                        }
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.trailing, 2)
                }
                .frame(maxHeight: 420)

                HStack {
                    Spacer()
                    nextButton
                }
            }
            
        case .cliDetection:
            ChatCLIDetectionStepView(
                codexStatus: setupState.codexCLIStatus,
                codexReport: setupState.codexCLIReport,
                claudeStatus: setupState.claudeCLIStatus,
                claudeReport: setupState.claudeCLIReport,
                isChecking: setupState.isCheckingCLIStatus,
                onRetry: { setupState.refreshCLIStatuses() },
                onInstall: { tool in openChatCLIInstallPage(for: tool) },
                selectedTool: setupState.preferredCLITool,
                onSelectTool: { tool in setupState.selectPreferredCLITool(tool) },
                nextButton: { nextButton }
            )
            .onAppear {
                setupState.ensureCLICheckStarted()
            }
            
        case .apiKeyInstructions:
            VStack(alignment: .leading, spacing: 24) {
                VStack(alignment: .leading, spacing: 8) {
                    Text("gemini_get_key_title")
                        .font(.custom("Nunito", size: 24))
                        .fontWeight(.semibold)
                        .foregroundColor(.black.opacity(0.9))

                    Text("gemini_free_tier_desc")
                        .font(.custom("Nunito", size: 14))
                        .foregroundColor(.black.opacity(0.6))
                }

                VStack(alignment: .leading, spacing: 16) {
                    HStack(alignment: .top, spacing: 12) {
                        Text("gemini_step_1")
                            .font(.custom("Nunito", size: 14))
                            .foregroundColor(.black.opacity(0.6))
                            .frame(width: 20, alignment: .leading)

                        Group {
                            Text("gemini_visit_studio")
                                .font(.custom("Nunito", size: 14))
                                .foregroundColor(.black.opacity(0.8))
                            + Text("gemini_studio_url")
                                .font(.custom("Nunito", size: 14))
                                .foregroundColor(Color(red: 1, green: 0.42, blue: 0.02))
                                .underline()
                        }
                        .onTapGesture { openGoogleAIStudio() }
                        .pointingHandCursor()
                    }

                    HStack(alignment: .top, spacing: 12) {
                        Text("gemini_step_2")
                            .font(.custom("Nunito", size: 14))
                            .foregroundColor(.black.opacity(0.6))
                            .frame(width: 20, alignment: .leading)

                        Text("api_click_get_key")
                            .font(.custom("Nunito", size: 14))
                            .foregroundColor(.black.opacity(0.8))
                    }

                    HStack(alignment: .top, spacing: 12) {
                        Text("gemini_step_3")
                            .font(.custom("Nunito", size: 14))
                            .foregroundColor(.black.opacity(0.6))
                            .frame(width: 20, alignment: .leading)

                        Text("api_create_copy")
                            .font(.custom("Nunito", size: 14))
                            .foregroundColor(.black.opacity(0.8))
                    }
                }
                .padding(.vertical, 12)

                // Buttons row with Open Google AI Studio on left, Next on right
                HStack {
                    DayflowSurfaceButton(
                        action: openGoogleAIStudio,
                        content: {
                            HStack(spacing: 8) {
                                Image(systemName: "safari").font(.system(size: 14))
                                Text("api_open_google_studio").font(.custom("Nunito", size: 14)).fontWeight(.semibold)
                            }
                        },
                        background: Color(red: 0.25, green: 0.17, blue: 0),
                        foreground: .white,
                        borderColor: .clear,
                        cornerRadius: 8,
                        horizontalPadding: 24,
                        verticalPadding: 12,
                        showOverlayStroke: true
                    )
                    Spacer()
                    nextButton
                }
            }
        }
    }
    
    private func handleBack() {
        if setupState.currentStepIndex == 0 {
            onBack()
        } else {
            setupState.goBack()
        }
    }
    
    private func handleContinue() {
        // Persist local config immediately after a successful local test when user advances
        if activeProviderType == "ollama" {
            if case .information(let title, _) = setupState.currentStep.contentType,
               (title == "Testing" || title == "Test Connection"),
               setupState.testSuccessful {
                persistLocalSettings()
            }
        }

        if setupState.isLastStep {
            saveConfiguration()
            onComplete()
        } else {
            setupState.markCurrentStepCompleted()
            setupState.goNext()
        }
    }
    
    private func saveConfiguration() {
        // Save API key to keychain for Gemini
        if activeProviderType == "gemini" && !setupState.apiKey.isEmpty {
            KeychainManager.shared.store(setupState.apiKey, for: "gemini")
            GeminiModelPreference(primary: setupState.geminiModel).save()
        }
        
        // Save local endpoint for local engine selection
        if activeProviderType == "ollama" {
            persistLocalSettings()
        }
        
        // Mark setup as complete
        UserDefaults.standard.set(true, forKey: "\(activeProviderType)SetupComplete")
    }

    // Persist provider choice + local settings without marking setup complete
    private func persistLocalSettings() {
        let endpoint = setupState.localBaseURL
        let type = LLMProviderType.ollamaLocal(endpoint: endpoint)
        if let encoded = try? JSONEncoder().encode(type) {
            UserDefaults.standard.set(encoded, forKey: "llmProviderType")
        }
        // Store model id for local engines
        UserDefaults.standard.set(setupState.localModelId, forKey: "llmLocalModelId")
        LocalModelPreferences.syncPreset(for: setupState.localEngine, modelId: setupState.localModelId)
        // Store local engine selection for header/model defaults
        UserDefaults.standard.set(setupState.localEngine.rawValue, forKey: "llmLocalEngine")
        // Store selected provider key for robustness across relaunches
        UserDefaults.standard.set("ollama", forKey: "selectedLLMProvider")
        // Also store the endpoint explicitly for other parts of the app if needed
        UserDefaults.standard.set(endpoint, forKey: "llmLocalBaseURL")
        persistLocalAPIKey(setupState.localAPIKey)
    }

    private func persistLocalAPIKey(_ value: String) {
        let trimmed = value.trimmingCharacters(in: .whitespacesAndNewlines)
        if trimmed.isEmpty {
            UserDefaults.standard.removeObject(forKey: "llmLocalAPIKey")
        } else {
            UserDefaults.standard.set(trimmed, forKey: "llmLocalAPIKey")
        }
    }
    
    private func openGoogleAIStudio() {
        if let url = URL(string: "https://aistudio.google.com/app/apikey") {
            NSWorkspace.shared.open(url)
        }
    }
    
    private func openLMStudioDownload() {
        if let url = URL(string: "https://lmstudio.ai/") {
            NSWorkspace.shared.open(url)
        }
    }

    private func openLMStudioModelDownload() {
        if let url = URL(string: "https://model.lmstudio.ai/download/lmstudio-community/Qwen3-VL-4B-Instruct-GGUF") {
            NSWorkspace.shared.open(url)
        }
    }
    
    private func openChatCLIInstallPage(for tool: CLITool) {
        guard let url = tool.installURL else { return }
        NSWorkspace.shared.open(url)
    }
    
    private func animateAppearance() {
        withAnimation(.easeOut(duration: 0.4)) {
            sidebarOpacity = 1
        }
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
            withAnimation(.easeOut(duration: 0.4)) {
                contentOpacity = 1
            }
        }
    }
}

class ProviderSetupState: ObservableObject {
    @Published var steps: [SetupStep] = []
    @Published var currentStepIndex: Int = 0
    @Published var apiKey: String = ""
    @Published var hasTestedConnection: Bool = false
    @Published var testSuccessful: Bool = false
    @Published var geminiModel: GeminiModel
    // Local engine configuration
    @Published var localEngine: LocalEngine = .lmstudio
    @Published var localBaseURL: String = LocalEngine.lmstudio.defaultBaseURL
    @Published var localModelId: String = LocalModelPreferences.defaultModelId(for: .lmstudio)
    @Published var localAPIKey: String = UserDefaults.standard.string(forKey: "llmLocalAPIKey") ?? ""
    // CLI detection
    @Published var codexCLIStatus: CLIDetectionState = .unknown
    @Published var claudeCLIStatus: CLIDetectionState = .unknown
    @Published var isCheckingCLIStatus: Bool = false
    @Published var codexCLIReport: CLIDetectionReport?
    @Published var claudeCLIReport: CLIDetectionReport?
    @Published var debugCommandInput: String = "which codex"
    @Published var debugCommandOutput: String = ""
    @Published var isRunningDebugCommand: Bool = false
    @Published var cliPrompt: String = "Say hello"
    @Published var codexStreamOutput: String = ""
    @Published var claudeStreamOutput: String = ""
    @Published var isRunningCodexStream: Bool = false
    @Published var isRunningClaudeStream: Bool = false
    @Published var preferredCLITool: CLITool? = ProviderSetupState.loadStoredPreferredCLITool()

    private var lastSavedGeminiModel: GeminiModel
    private var hasStartedCLICheck = false
    private let codexStreamer = StreamingCLI()
    private let claudeStreamer = StreamingCLI()
    private var codexStartTask: Task<Void, Never>?
    private var claudeStartTask: Task<Void, Never>?

    init() {
        let preference = GeminiModelPreference.load()
        self.geminiModel = preference.primary
        self.lastSavedGeminiModel = preference.primary
    }
    
    var currentStep: SetupStep {
        guard currentStepIndex < steps.count else {
            return SetupStep(id: "fallback", title: "Setup", contentType: .information("Complete", "Setup is complete"))
        }
        return steps[currentStepIndex]
    }
    
    var canContinue: Bool {
        switch currentStep.contentType {
        case .apiKeyInput:
            return !apiKey.isEmpty && apiKey.count > 20
        case .cliDetection:
            return isSelectedCLIToolReady
        case .information(_, _):
            if currentStep.id == "verify" || currentStep.id == "test" {
                return testSuccessful
            }
            return true
        case .terminalCommand(_), .modelDownload(_), .localChoice, .localModelInstall, .apiKeyInstructions:
            return true
        }
    }
    
    var isLastStep: Bool {
        return currentStepIndex == steps.count - 1
    }
    
    func configureSteps(for provider: String) {
        switch provider {
        case "ollama":
            steps = [
                SetupStep(
                    id: "intro",
                    title: String(localized: "step_before_begin"),
                    contentType: .information(
                        String(localized: "info_for_experienced"),
                        String(localized: "setup_advanced_warning")
                    )
                ),
                SetupStep(id: "choose", title: String(localized: "step_choose_engine"), contentType: .localChoice),
                SetupStep(id: "model", title: String(localized: "step_install_model"), contentType: .localModelInstall),
                SetupStep(id: "test", title: String(localized: "step_test_connection"), contentType: .information(String(localized: "info_test_connection"), String(localized: "local_test_instruction"))),
                SetupStep(id: "complete", title: String(localized: "step_complete"), contentType: .information(String(localized: "info_all_set"), String(localized: "local_complete_message")))
            ]
        case "chatgpt_claude":
            preferredCLITool = ProviderSetupState.loadStoredPreferredCLITool()
            steps = [
                SetupStep(
                    id: "intro",
                    title: String(localized: "step_before_begin"),
                    contentType: .information(
                        String(localized: "info_install_cli"),
                        String(localized: "cli_intro_message")
                    )
                ),
                SetupStep(
                    id: "detect",
                    title: String(localized: "step_check_installations"),
                    contentType: .cliDetection
                ),
                SetupStep(
                    id: "test",
                    title: String(localized: "step_test_connection"),
                    contentType: .information(
                        String(localized: "info_test_connection"),
                        String(localized: "cli_test_instruction")
                    )
                ),
                SetupStep(
                    id: "complete",
                    title: String(localized: "step_complete"),
                    contentType: .information(
                        String(localized: "info_all_set"),
                        String(localized: "cli_complete_message")
                    )
                )
            ]
            codexCLIStatus = .unknown
            claudeCLIStatus = .unknown
            codexCLIReport = nil
            claudeCLIReport = nil
            isCheckingCLIStatus = false
            hasStartedCLICheck = false
            cancelCodexStream()
            cancelClaudeStream()
            codexStreamOutput = ""
            claudeStreamOutput = ""
            cliPrompt = "Say hello"
        default: // gemini
            steps = [
                SetupStep(id: "getkey", title: String(localized: "step_get_api_key"),
                          contentType: .apiKeyInstructions),
                SetupStep(id: "enterkey", title: String(localized: "step_enter_api_key"),
                          contentType: .apiKeyInput),
                SetupStep(id: "verify", title: String(localized: "step_test_connection"),
                          contentType: .information(String(localized: "info_test_connection"), String(localized: "gemini_test_instruction"))),
                SetupStep(id: "complete", title: String(localized: "step_complete"),
                          contentType: .information(String(localized: "info_all_set"), String(localized: "gemini_complete_message")))
            ]
        }
    }
    
    func goNext() {
        // Save API key to keychain when moving from API key input step
        if currentStep.contentType.isApiKeyInput && !apiKey.isEmpty {
            KeychainManager.shared.store(apiKey, for: "gemini")
            // Reset test state when API key changes
            hasTestedConnection = false
            testSuccessful = false
            persistGeminiModelSelection(source: "onboarding_step")
        }

        if currentStepIndex < steps.count - 1 {
            currentStepIndex += 1
        }
    }
    
    func goBack() {
        if currentStepIndex > 0 {
            currentStepIndex -= 1
        }
    }
    
    func navigateToStep(_ stepId: String) {
        if let index = steps.firstIndex(where: { $0.id == stepId }) {
            // Reset test state when navigating to test step
            if stepId == "verify" || stepId == "test" {
                hasTestedConnection = false
                testSuccessful = false
            }
            // Allow free navigation between all steps
            currentStepIndex = index
        }
    }
    
    func markCurrentStepCompleted() {
        if currentStepIndex < steps.count {
            steps[currentStepIndex].markCompleted()
        }
    }

    func persistGeminiModelSelection(source: String) {
        guard geminiModel != lastSavedGeminiModel else { return }
        lastSavedGeminiModel = geminiModel
        GeminiModelPreference(primary: geminiModel).save()

        Task { @MainActor in
            AnalyticsService.shared.capture("gemini_model_selected", [
                "source": source,
                "model": geminiModel.rawValue
            ])
        }

        // Changing models should prompt the user to re-run the connection test
        hasTestedConnection = false
        testSuccessful = false
    }
    
    private var isSelectedCLIToolReady: Bool {
        guard let preferredCLITool else { return false }
        return isToolAvailable(preferredCLITool)
    }
    
    func ensureCLICheckStarted() {
        guard !hasStartedCLICheck else { return }
        hasStartedCLICheck = true
        refreshCLIStatuses()
    }
    
    func refreshCLIStatuses() {
        if isCheckingCLIStatus { return }
        isCheckingCLIStatus = true
        codexCLIStatus = .checking
        claudeCLIStatus = .checking
        codexCLIReport = nil
        claudeCLIReport = nil
        
        Task.detached { [weak self] in
            guard let self else { return }
            async let codex = CLIDetector.detect(tool: .codex)
            async let claude = CLIDetector.detect(tool: .claude)
            let (codexResult, claudeResult) = await (codex, claude)
            
            await MainActor.run {
                self.codexCLIReport = codexResult
                self.claudeCLIReport = claudeResult
                self.codexCLIStatus = codexResult.state
                self.claudeCLIStatus = claudeResult.state
                self.isCheckingCLIStatus = false
                self.ensurePreferredCLIToolIsValid()
            }
        }
    }
    
    @MainActor
    func runDebugCommand() {
        guard !debugCommandInput.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
            debugCommandOutput = "Enter a command to run."
            return
        }
        if isRunningDebugCommand { return }
        isRunningDebugCommand = true
        debugCommandOutput = "Running..."
        
        let command = debugCommandInput
        Task.detached { [weak self] in
            let result = CLIDetector.runDebugCommand(command)
            await MainActor.run { [weak self] in
                guard let self else { return }
                var output = ""
                output += "Exit code: \(result.exitCode)\n"
                if !result.stdout.isEmpty {
                    output += "\nstdout:\n\(result.stdout)"
                }
                if !result.stderr.isEmpty {
                    output += "\nstderr:\n\(result.stderr)"
                }
                if result.stdout.isEmpty && result.stderr.isEmpty {
                    output += "\n(no output)"
                }
                self.debugCommandOutput = output
                self.isRunningDebugCommand = false
            }
        }
    }
    
    func selectPreferredCLITool(_ tool: CLITool) {
        guard isToolAvailable(tool) else { return }
        preferredCLITool = tool
        persistPreferredCLITool()
    }
    
    func persistPreferredCLITool() {
        guard let tool = preferredCLITool else {
            UserDefaults.standard.removeObject(forKey: Self.cliPreferenceKey)
            return
        }
        UserDefaults.standard.set(tool.rawValue, forKey: Self.cliPreferenceKey)
    }
    
    private func ensurePreferredCLIToolIsValid() {
        if let current = preferredCLITool, isToolAvailable(current) {
            return
        }
        if isToolAvailable(.codex) {
            preferredCLITool = .codex
        } else if isToolAvailable(.claude) {
            preferredCLITool = .claude
        } else {
            preferredCLITool = nil
        }
        persistPreferredCLITool()
    }
    
    private func isToolAvailable(_ tool: CLITool) -> Bool {
        switch tool {
        case .codex:
            if codexCLIStatus.isInstalled { return true }
            return codexCLIReport?.resolvedPath != nil
        case .claude:
            if claudeCLIStatus.isInstalled { return true }
            return claudeCLIReport?.resolvedPath != nil
        }
    }
    
    private static func loadStoredPreferredCLITool() -> CLITool? {
        guard let raw = UserDefaults.standard.string(forKey: Self.cliPreferenceKey) else {
            return nil
        }
        return CLITool(rawValue: raw)
    }
    
    private static let cliPreferenceKey = "chatCLIPreferredTool"
    
    func runCodexStream() {
        guard !isRunningCodexStream else { return }
        codexStartTask?.cancel()
        isRunningCodexStream = true
        codexStreamOutput = "Checking for Codex CLI...\n"

        codexStartTask = Task { @MainActor in
            let installed = await Task.detached(priority: .utility) {
                CLIDetector.isInstalled(.codex)
            }.value

            guard !Task.isCancelled else { return }

            guard installed else {
                codexStreamOutput = "Codex CLI not found. Install it and run 'codex auth' in Terminal."
                isRunningCodexStream = false
                codexStartTask = nil
                return
            }

            let prompt = cliPrompt.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty ? "Say hello" : cliPrompt
            codexStreamOutput = "Running codex with prompt: \(prompt)\n\n"
            codexStartTask = nil

            // Build args with dynamic MCP disable flags
            var streamArgs = ["exec", "--skip-git-repo-check", "-c", "model_reasoning_effort=high"]
            let mcpServers = LoginShellRunner.getCodexMCPServerNames()
            for serverName in mcpServers {
                streamArgs.append(contentsOf: ["--config", "mcp_servers.\(serverName).enabled=false"])
            }
            streamArgs.append(contentsOf: ["-c", "rmcp_client=false", "-c", "features.web_search_request=false", "--", prompt])

            codexStreamer.run(
                command: "codex",
                args: streamArgs,
                onStdout: { [weak self] chunk in
                    self?.codexStreamOutput.append(chunk)
                },
                onStderr: { [weak self] chunk in
                    self?.codexStreamOutput.append("\n[stderr] \(chunk)")
                },
                onFinish: { [weak self] code in
                    guard let self else { return }
                    self.codexStreamOutput.append("\n\nExited \(code)\n")
                    self.isRunningCodexStream = false
                }
            )
        }
    }
    
    func cancelCodexStream() {
        codexStartTask?.cancel()
        codexStartTask = nil
        codexStreamer.cancel()
        if isRunningCodexStream {
            codexStreamOutput.append("\n\nCancelled.\n")
        }
        isRunningCodexStream = false
    }
    
    func runClaudeStream() {
        guard !isRunningClaudeStream else { return }
        claudeStartTask?.cancel()
        isRunningClaudeStream = true
        claudeStreamOutput = "Checking for Claude CLI...\n"

        claudeStartTask = Task { @MainActor in
            let installed = await Task.detached(priority: .utility) {
                CLIDetector.isInstalled(.claude)
            }.value

            guard !Task.isCancelled else { return }

            guard installed else {
                claudeStreamOutput = "Claude CLI not found. Install it and run 'claude login' in Terminal."
                isRunningClaudeStream = false
                claudeStartTask = nil
                return
            }

            let prompt = cliPrompt.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty ? "Say hello" : cliPrompt
            claudeStreamOutput = "Running claude with prompt: \(prompt)\n\n"
            claudeStartTask = nil

            claudeStreamer.run(
                command: "claude",
                args: ["--print", "--output-format", "json", "--strict-mcp-config", "--", prompt],
                onStdout: { [weak self] chunk in
                    self?.claudeStreamOutput.append(chunk)
                },
                onStderr: { [weak self] chunk in
                    self?.claudeStreamOutput.append("\n[stderr] \(chunk)")
                },
                onFinish: { [weak self] code in
                    guard let self else { return }
                    self.claudeStreamOutput.append("\n\nExited \(code)\n")
                    self.isRunningClaudeStream = false
                }
            )
        }
    }
    
    func cancelClaudeStream() {
        claudeStartTask?.cancel()
        claudeStartTask = nil
        claudeStreamer.cancel()
        if isRunningClaudeStream {
            claudeStreamOutput.append("\n\nCancelled.\n")
        }
        isRunningClaudeStream = false
    }
}

struct SetupStep: Identifiable {
    let id: String
    let title: String
    let contentType: StepContentType
    private(set) var isCompleted: Bool = false
    
    mutating func markCompleted() {
        isCompleted = true
    }
}

enum StepContentType {
    case terminalCommand(String)
    case apiKeyInput
    case apiKeyInstructions
    case modelDownload(String)
    case information(String, String)
    case localChoice
    case localModelInstall
    case cliDetection
    
    var isApiKeyInput: Bool {
        if case .apiKeyInput = self {
            return true
        }
        return false
    }
    
    var informationTitle: String? {
        if case .information(let title, _) = self {
            return title
        }
        return nil
    }
}


extension ProviderSetupState {
    @MainActor func selectEngine(_ engine: LocalEngine) {
        localEngine = engine
        if engine != .custom {
            localBaseURL = engine.defaultBaseURL
        }
        let defaultModel = LocalModelPreferences.defaultModelId(for: engine == .custom ? .ollama : engine)
        localModelId = defaultModel
        LocalModelPreferences.syncPreset(for: engine, modelId: defaultModel)

        // Track local engine selection for analytics
        AnalyticsService.shared.capture("local_engine_selected", [
            "engine": engine.rawValue,
            "base_url": localBaseURL,
            "default_model": defaultModel,
            "has_api_key": !localAPIKey.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
        ])
    }
    
    var localCurlCommand: String {
        let payload = "{\"model\":\"\(localModelId)\",\"messages\":[{\"role\":\"user\",\"content\":\"Say 'hello' and your model name.\"}],\"max_tokens\":50}"
        let authHeader = localEngine == .lmstudio ? " -H \"Authorization: Bearer lm-studio\"" : ""
        let endpoint = LocalEndpointUtilities.chatCompletionsURL(baseURL: localBaseURL)?.absoluteString ?? "\(localBaseURL)/v1/chat/completions"
        return "curl -s \(endpoint) -H \"Content-Type: application/json\"\(authHeader) -d '\(payload)'"
    }
}

private enum LocalLLMTestConstants {
    static let blankImageDataURL = LocalLLMTestImageFactory.blankImageDataURL(width: 1280, height: 720)
    static let prompt = "What color is this image? Answer with a single word."
    static let slowMachineMessage = "It took longer than 30 seconds, so your machine doesn't appear powerful enough to run this model locally."
    static let maxLatency: TimeInterval = 30
}

private enum LocalLLMTestImageFactory {
    static func blankImageDataURL(width: Int, height: Int) -> String {
        guard let data = makeWhiteImageData(width: width, height: height) else {
            assertionFailure("Failed to build local LLM test image")
            return ""
        }
        return "data:image/jpeg;base64,\(data.base64EncodedString())"
    }

    private static func makeWhiteImageData(width: Int, height: Int) -> Data? {
        guard let bitmap = NSBitmapImageRep(
            bitmapDataPlanes: nil,
            pixelsWide: width,
            pixelsHigh: height,
            bitsPerSample: 8,
            samplesPerPixel: 4,
            hasAlpha: true,
            isPlanar: false,
            colorSpaceName: .deviceRGB,
            bytesPerRow: 0,
            bitsPerPixel: 0
        ) else {
            return nil
        }

        let rect = NSRect(x: 0, y: 0, width: width, height: height)
        NSGraphicsContext.saveGraphicsState()
        if let context = NSGraphicsContext(bitmapImageRep: bitmap) {
            NSGraphicsContext.current = context
            NSColor.white.setFill()
            rect.fill()
            context.flushGraphics()
        }
        NSGraphicsContext.restoreGraphicsState()

        return bitmap.representation(using: .jpeg, properties: [:])
    }
}

struct LocalLLMTestView: View {
    @Binding private var baseURL: String
    @Binding private var modelId: String
    @Binding private var apiKey: String
    private let engine: LocalEngine
    private let showInputs: Bool
    private let buttonLabel: String
    private let basePlaceholder: String?
    private let modelPlaceholder: String?
    private let onTestComplete: (Bool) -> Void

    init(
        baseURL: Binding<String>,
        modelId: Binding<String>,
        apiKey: Binding<String> = .constant(""),
        engine: LocalEngine,
        showInputs: Bool = true,
        buttonLabel: String = "Test Local API",
        basePlaceholder: String? = nil,
        modelPlaceholder: String? = nil,
        onTestComplete: @escaping (Bool) -> Void
    ) {
        _baseURL = baseURL
        _modelId = modelId
        _apiKey = apiKey
        self.engine = engine
        self.showInputs = showInputs
        self.buttonLabel = buttonLabel
        self.basePlaceholder = basePlaceholder
        self.modelPlaceholder = modelPlaceholder
        self.onTestComplete = onTestComplete
    }

    private let accentColor = Color(red: 0.25, green: 0.17, blue: 0)
    private let successAccentColor = Color(red: 0.34, green: 1, blue: 0.45)
    private var trimmedAPIKey: String {
        apiKey.trimmingCharacters(in: .whitespacesAndNewlines)
    }

    @State private var isTesting = false
    @State private var resultMessage: String?
    @State private var success: Bool = false
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            if showInputs {
                VStack(alignment: .leading, spacing: 8) {
                    Text("local_base_url")
                        .font(.custom("Nunito", size: 13))
                        .foregroundColor(.black.opacity(0.6))
                    TextField(basePlaceholder ?? engine.defaultBaseURL, text: $baseURL)
                        .textFieldStyle(.roundedBorder)
                }

                VStack(alignment: .leading, spacing: 8) {
                    Text("local_model_id")
                        .font(.custom("Nunito", size: 13))
                        .foregroundColor(.black.opacity(0.6))
                    TextField(modelPlaceholder ?? LocalModelPreferences.defaultModelId(for: engine), text: $modelId)
                        .textFieldStyle(.roundedBorder)
                }

                if engine == .custom {
                    VStack(alignment: .leading, spacing: 6) {
                        Text("local_api_key_optional")
                            .font(.custom("Nunito", size: 13))
                            .foregroundColor(.black.opacity(0.6))
                        SecureField("sk-live-...", text: $apiKey)
                            .textFieldStyle(.roundedBorder)
                            .disableAutocorrection(true)
                        Text("local_api_key_help")
                            .font(.custom("Nunito", size: 11))
                            .foregroundColor(.black.opacity(0.5))
                    }
                }
            }
            
            DayflowSurfaceButton(
                action: runTest,
                content: {
                    HStack(spacing: 8) {
                        if isTesting {
                            ProgressView().scaleEffect(0.8)
                        } else {
                            Image(systemName: success ? "checkmark.circle.fill" : "bolt.fill").font(.system(size: 14))
                        }
                        let idleLabel = success ? String(localized: "test_successful") : buttonLabel
                        Text(isTesting ? String(localized: "testing") : idleLabel)
                            .font(.custom("Nunito", size: 14))
                            .fontWeight(.semibold)
                    }
                },
                background: success ? successAccentColor.opacity(0.2) : accentColor,
                foreground: success ? .black : .white,
                borderColor: success ? successAccentColor.opacity(0.3) : .clear,
                cornerRadius: 8,
                horizontalPadding: 24,
                verticalPadding: 12,
                showOverlayStroke: !success
            )
            .disabled(isTesting)
            
            if let msg = resultMessage {
                Text(msg)
                    .font(.custom("Nunito", size: 13))
                    .foregroundColor(success ? .black.opacity(0.7) : Color(hex: "E91515"))
                    .padding(.vertical, 6)
                if !success {
                    Text("local_test_error_help")
                        .font(.custom("Nunito", size: 12))
                        .foregroundColor(.black.opacity(0.55))
                        .padding(.top, 2)
                }
            }
        }
    }
    private func runTest() {
        guard !isTesting else { return }
        isTesting = true
        success = false
        resultMessage = nil

        guard let url = LocalEndpointUtilities.chatCompletionsURL(baseURL: baseURL) else {
            resultMessage = "Invalid base URL"
            isTesting = false
            onTestComplete(false)
            return
        }

        let payload = LocalLLMChatRequest(
            model: modelId,
            messages: [
                LocalLLMChatMessage(
                    role: "user",
                    content: [
                        .text(LocalLLMTestConstants.prompt),
                        .imageDataURL(LocalLLMTestConstants.blankImageDataURL)
                    ]
                )
            ],
            maxTokens: 10
        )

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        if engine == .lmstudio { request.setValue("Bearer lm-studio", forHTTPHeaderField: "Authorization") }
        if engine == .custom && !trimmedAPIKey.isEmpty {
            request.setValue("Bearer \(trimmedAPIKey)", forHTTPHeaderField: "Authorization")
        }
        let encoder = JSONEncoder()
        encoder.keyEncodingStrategy = .convertToSnakeCase
        request.httpBody = try? encoder.encode(payload)
        request.timeoutInterval = 35

        let startedAt = Date()

        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                let duration = Date().timeIntervalSince(startedAt)
                if duration > LocalLLMTestConstants.maxLatency {
                    self.resultMessage = LocalLLMTestConstants.slowMachineMessage
                    self.success = false
                    self.isTesting = false
                    self.onTestComplete(false)
                    return
                }
                if let error = error {
                    self.resultMessage = error.localizedDescription
                    self.isTesting = false
                    self.onTestComplete(false)
                    return
                }
                guard let http = response as? HTTPURLResponse, let data = data else {
                    self.resultMessage = "No response"; self.isTesting = false; self.onTestComplete(false); return
                }
                if http.statusCode == 200 {
                    // Success: don't print raw response body; keep UI clean
                    self.resultMessage = nil
                    self.success = true
                    self.isTesting = false
                    self.onTestComplete(true)
                } else {
                    let body = String(data: data, encoding: .utf8) ?? ""
                    self.resultMessage = "HTTP \(http.statusCode): \(body)"
                    self.isTesting = false
                    self.onTestComplete(false)
                }
            }
        }.resume()
    }
}

private struct LocalLLMChatRequest: Codable {
    let model: String
    let messages: [LocalLLMChatMessage]
    let maxTokens: Int
}

private struct LocalLLMChatMessage: Codable {
    let role: String
    let content: [LocalLLMChatContent]
}

private struct LocalLLMChatContent: Codable {
    let type: String
    let text: String?
    let imageURL: LocalLLMChatImageURL?

    static func text(_ value: String) -> LocalLLMChatContent {
        LocalLLMChatContent(type: "text", text: value, imageURL: nil)
    }

    static func imageDataURL(_ url: String) -> LocalLLMChatContent {
        LocalLLMChatContent(type: "image_url", text: nil, imageURL: LocalLLMChatImageURL(url: url))
    }
}

private struct LocalLLMChatImageURL: Codable {
    let url: String
}

struct ChatCLITestView: View {
    let selectedTool: CLITool?
    let onTestComplete: (Bool) -> Void

    private let accentColor = Color(red: 0.25, green: 0.17, blue: 0)
    private let successAccentColor = Color(red: 0.34, green: 1, blue: 0.45)

    @State private var isTesting = false
    @State private var success = false
    @State private var resultMessage: String?
    @State private var debugOutput: String?

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("cli_test_question")
                .font(.custom("Nunito", size: 13))
                .foregroundColor(.black.opacity(0.6))
                .fixedSize(horizontal: false, vertical: true)

            DayflowSurfaceButton(
                action: runTest,
                content: {
                    HStack(spacing: 8) {
                        if isTesting {
                            ProgressView().scaleEffect(0.8)
                        } else {
                            Image(systemName: success ? "checkmark.circle.fill" : "bolt.fill").font(.system(size: 14))
                        }
                        let idleLabel = success ? String(localized: "test_successful") : String(localized: "test_cli")
                        Text(isTesting ? String(localized: "testing") : idleLabel)
                            .font(.custom("Nunito", size: 14))
                            .fontWeight(.semibold)
                    }
                },
                background: success ? successAccentColor.opacity(0.2) : accentColor,
                foreground: success ? .black : .white,
                borderColor: success ? successAccentColor.opacity(0.3) : .clear,
                cornerRadius: 8,
                horizontalPadding: 24,
                verticalPadding: 12,
                showOverlayStroke: !success
            )
            .disabled(isTesting || selectedTool == nil)
            .opacity(selectedTool == nil ? 0.5 : 1.0)

            if selectedTool == nil {
                Text("cli_select_first")
                    .font(.custom("Nunito", size: 12))
                    .foregroundColor(.black.opacity(0.6))
            }

            if let msg = resultMessage {
                HStack(alignment: .center, spacing: 8) {
                    Text(msg)
                        .font(.custom("Nunito", size: 13))
                        .foregroundColor(success ? .black.opacity(0.7) : Color(hex: "E91515"))

                    if debugOutput != nil {
                        Button(action: copyDebugLogs) {
                            Text("copy_logs")
                                .font(.custom("Nunito", size: 11))
                                .foregroundColor(.black.opacity(0.4))
                                .underline()
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.vertical, 6)
            }

            // Debug output - shows raw CLI response for troubleshooting (only on failure)
            if let debug = debugOutput, !success {
                VStack(alignment: .leading, spacing: 6) {
                    Text("cli_debug_output")
                        .font(.custom("Nunito", size: 11))
                        .fontWeight(.semibold)
                        .foregroundColor(.black.opacity(0.5))
                    ScrollView {
                        Text(debug)
                            .font(.system(size: 11, design: .monospaced))
                            .foregroundColor(.black.opacity(0.6))
                            .textSelection(.enabled)
                            .frame(maxWidth: .infinity, alignment: .leading)
                    }
                    .frame(maxHeight: 120)
                    .padding(8)
                    .background(Color.black.opacity(0.03))
                    .cornerRadius(6)
                }
                .padding(.top, 4)
            }
        }
    }

    private func runTest() {
        guard !isTesting else { return }
        guard let tool = selectedTool else {
            resultMessage = "Pick ChatGPT or Claude first."
            return
        }

        isTesting = true
        success = false
        resultMessage = nil
        debugOutput = nil

        Task.detached {
            let outcome: Result<CLIResult, Error> = {
                do {
                    return .success(try performTest(for: tool))
                } catch {
                    return .failure(error)
                }
            }()

            await MainActor.run {
                isTesting = false
                switch outcome {
                case .success(let cliResult):
                    // Build debug output for troubleshooting
                    var debugParts: [String] = []
                    debugParts.append("Tool: \(tool.shortName)")
                    debugParts.append("Exit code: \(cliResult.exitCode)")
                    debugParts.append("Shell: \(LoginShellRunner.userLoginShell.path)")

                    // Show all installations found (helps debug multi-install issues)
                    let cmdName = tool == .codex ? "codex" : "claude"
                    let whichResult = LoginShellRunner.run("which -a \(cmdName)", timeout: 5)
                    if whichResult.exitCode == 0 {
                        let paths = whichResult.stdout.trimmingCharacters(in: .whitespacesAndNewlines)
                        if !paths.isEmpty {
                            debugParts.append("Installations found:\n\(paths)")
                        }
                    }

                    if !cliResult.stdout.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
                        debugParts.append("stdout:\n\(cliResult.stdout)")
                    }
                    if !cliResult.stderr.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
                        debugParts.append("stderr:\n\(cliResult.stderr)")
                    }
                    debugOutput = debugParts.joined(separator: "\n\n")

                    // Check exit code FIRST - non-zero means failure
                    if cliResult.exitCode != 0 {
                        success = false
                        if let authError = detectAuthError(cliResult, for: tool) {
                            resultMessage = authError
                        } else {
                            let stderrTrimmed = cliResult.stderr.trimmingCharacters(in: .whitespacesAndNewlines)
                            if stderrTrimmed.isEmpty {
                                if tool == .claude {
                                    resultMessage = "Claude CLI returned an error. You may need to sign in — run 'claude login' in Terminal."
                                } else {
                                    resultMessage = "Codex CLI returned an error. You may need to sign in — run 'codex auth' in Terminal."
                                }
                            } else {
                                resultMessage = "CLI error: \(stderrTrimmed.prefix(150))"
                            }
                        }
                        onTestComplete(false)
                        return
                    }

                    // Exit code is 0, now check for expected response
                    let passed = parseForSuccess(cliResult, for: tool)
                    success = passed
                    if passed {
                        resultMessage = "CLI is working!"
                    } else if cliResult.stdout.isEmpty {
                        resultMessage = "CLI returned empty response. Make sure you're signed in."
                    } else {
                        let preview = cliResult.stdout.prefix(100)
                        resultMessage = "Got: \"\(preview)\" — expected '4'"
                    }
                    onTestComplete(passed)
                case .failure(let error):
                    success = false
                    resultMessage = error.localizedDescription

                    // Build debug output even for errors
                    var debugParts: [String] = []
                    debugParts.append("Tool: \(tool.shortName)")
                    debugParts.append("Error: \(error.localizedDescription)")
                    debugParts.append("Shell: \(LoginShellRunner.userLoginShell.path)")

                    let cmdName = tool == .codex ? "codex" : "claude"
                    let whichResult = LoginShellRunner.run("which -a \(cmdName)", timeout: 5)
                    if whichResult.exitCode == 0 {
                        let paths = whichResult.stdout.trimmingCharacters(in: .whitespacesAndNewlines)
                        if !paths.isEmpty {
                            debugParts.append("Installations found:\n\(paths)")
                        }
                    } else {
                        debugParts.append("Installations found: none")
                    }

                    debugOutput = debugParts.joined(separator: "\n\n")
                    onTestComplete(false)
                }
            }
        }
    }

    private func copyDebugLogs() {
        guard let debug = debugOutput else { return }
        NSPasteboard.general.clearContents()
        NSPasteboard.general.setString(debug, forType: .string)
    }

    private func performTest(for tool: CLITool) throws -> CLIResult {
        guard CLIDetector.isInstalled(tool) else {
            throw NSError(domain: "ChatCLITest", code: 1, userInfo: [NSLocalizedDescriptionKey: "\(tool.shortName) CLI not found. Install it and run '\(tool == .codex ? "codex auth" : "claude login")' in Terminal."])
        }

        // Use a sandboxed directory to avoid permission prompts for Downloads/Desktop
        let safeWorkingDir = FileManager.default.temporaryDirectory

        // Simple math test - deterministic and doesn't require image handling
        let prompt = "What is 2+2? Answer with just the number."

        switch tool {
        case .codex:
            // --skip-git-repo-check needed because app runs from sandboxed directory
            // Disable MCP servers dynamically to avoid connecting to user's configured servers during test
            // -- separator ensures prompt isn't parsed as an option
            var codexArgs = [
                "exec",
                "--skip-git-repo-check",
                "-c", "model_reasoning_effort=low"
            ]
            // Dynamically disable each MCP server by name
            let mcpServers = LoginShellRunner.getCodexMCPServerNames()
            for serverName in mcpServers {
                codexArgs.append(contentsOf: ["--config", "mcp_servers.\(serverName).enabled=false"])
            }
            codexArgs.append(contentsOf: [
                "-c", "rmcp_client=false",
                "-c", "features.web_search_request=false",
                "--",
                prompt
            ])
            return try runCLI(
                "codex",
                args: codexArgs,
                cwd: safeWorkingDir
            )
        case .claude:
            // --strict-mcp-config disables all user MCP servers
            // -- separator ensures prompt isn't parsed as an option
            return try runCLI(
                "claude",
                args: [
                    "--print",
                    "--output-format", "text",
                    "--strict-mcp-config",
                    "--",
                    prompt
                ],
                cwd: safeWorkingDir
            )
        }
    }

    private func parseForSuccess(_ result: CLIResult, for tool: CLITool) -> Bool {
        let combined = (result.stdout + " " + result.stderr)
        // Simple math test - check for "4" in the response
        return combined.contains("4")
    }

    private func detectAuthError(_ result: CLIResult, for tool: CLITool) -> String? {
        let combined = (result.stdout + " " + result.stderr).lowercased()

        // Check for common auth failure patterns
        let isAuthError = combined.contains("invalid api key")
            || combined.contains("please run /login")
            || combined.contains("401 unauthorized")
            || combined.contains("not logged in")
            || combined.contains("codex auth")
            || combined.contains("claude login")
            || combined.contains("authentication required")
            || combined.contains("unauthorized")

        guard isAuthError else { return nil }

        // Return the correct message based on which tool we're actually testing
        switch tool {
        case .claude:
            return "Claude CLI is not signed in. Run 'claude login' in Terminal to authenticate."
        case .codex:
            return "Codex CLI is not signed in. Run 'codex auth' in Terminal to authenticate."
        }
    }
}

enum CLITool: String, CaseIterable {
    case codex
    case claude
    
    var displayName: String {
        switch self {
        case .codex: return "ChatGPT (Codex CLI)"
        case .claude: return "Claude Code"
        }
    }
    
    var shortName: String {
        switch self {
        case .codex: return "ChatGPT"
        case .claude: return "Claude"
        }
    }
    
    var subtitle: String {
        switch self {
        case .codex:
            return "OpenAI's ChatGPT desktop tooling with codex CLI"
        case .claude:
            return "Anthropic's Claude Code command-line helper"
        }
    }
    
    var executableName: String {
        switch self {
        case .codex: return "codex"
        case .claude: return "claude"
        }
    }
    
    var versionCommand: String {
        "\(executableName) --version"
    }
    
    var installURL: URL? {
        switch self {
        case .codex:
            return URL(string: "https://developers.openai.com/codex/cli/")
        case .claude:
            return URL(string: "https://docs.anthropic.com/en/docs/claude-code/setup")
        }
    }
    
    var iconName: String {
        switch self {
        case .codex: return "terminal"
        case .claude: return "bolt.horizontal.circle"
        }
    }
}

enum CLIDetectionState: Equatable {
    case unknown
    case checking
    case installed(version: String)
    case notFound
    case failed(message: String)
    
    var isInstalled: Bool {
        if case .installed = self { return true }
        return false
    }
    
    var statusLabel: String {
        switch self {
        case .unknown:
            return "Not checked"
        case .checking:
            return "Checking…"
        case .installed:
            return "Installed"
        case .notFound:
            return "Not installed"
        case .failed:
            return "Error"
        }
    }
    
    var detailMessage: String? {
        switch self {
        case .installed(let version):
            return version.trimmingCharacters(in: .whitespacesAndNewlines)
        case .failed(let message):
            let trimmed = message.trimmingCharacters(in: .whitespacesAndNewlines)
            return trimmed.isEmpty ? nil : trimmed
        default:
            return nil
        }
    }
}

struct CLIDetectionReport {
    let state: CLIDetectionState
    let resolvedPath: String?
    let stdout: String?
    let stderr: String?
}

struct CLIDetector {
    /// Detect if a CLI tool is installed by running `tool --version` via login shell.
    /// This replicates exactly what happens when user types in Terminal.app.
    static func detect(tool: CLITool) async -> CLIDetectionReport {
        let result = LoginShellRunner.run("\(tool.executableName) --version", timeout: 10)

        if result.exitCode == 0 {
            let trimmed = result.stdout.trimmingCharacters(in: .whitespacesAndNewlines)
            let firstLine = trimmed.components(separatedBy: .newlines).first ?? trimmed
            let summary = firstLine.isEmpty ? "\(tool.shortName) detected" : firstLine
            return CLIDetectionReport(state: .installed(version: summary), resolvedPath: tool.executableName, stdout: result.stdout, stderr: result.stderr)
        }

        if result.exitCode == 127 || result.stderr.contains("command not found") {
            return CLIDetectionReport(state: .notFound, resolvedPath: nil, stdout: result.stdout, stderr: result.stderr)
        }

        let message = result.stderr.trimmingCharacters(in: .whitespacesAndNewlines)
        if message.isEmpty {
            return CLIDetectionReport(state: .failed(message: "Exit code \(result.exitCode)"), resolvedPath: tool.executableName, stdout: result.stdout, stderr: result.stderr)
        }
        return CLIDetectionReport(state: .failed(message: message), resolvedPath: tool.executableName, stdout: result.stdout, stderr: result.stderr)
    }

    /// Check if a CLI tool is installed (simple boolean check)
    static func isInstalled(_ tool: CLITool) -> Bool {
        LoginShellRunner.isInstalled(tool.executableName)
    }

    /// Run an arbitrary debug command via login shell
    static func runDebugCommand(_ command: String) -> CLIResult {
        let result = LoginShellRunner.run(command, timeout: 30)
        return CLIResult(stdout: result.stdout, stderr: result.stderr, exitCode: result.exitCode)
    }
}

struct ChatCLIDetectionStepView<NextButton: View>: View {
    let codexStatus: CLIDetectionState
    let codexReport: CLIDetectionReport?
    let claudeStatus: CLIDetectionState
    let claudeReport: CLIDetectionReport?
    let isChecking: Bool
    let onRetry: () -> Void
    let onInstall: (CLITool) -> Void
    let selectedTool: CLITool?
    let onSelectTool: (CLITool) -> Void
    @ViewBuilder let nextButton: () -> NextButton
    
    private let accentColor = Color(red: 0.25, green: 0.17, blue: 0)
    
    var body: some View {
        VStack(alignment: .leading, spacing: 24) {
            Text("cli_detailed_instruction")
                .font(.custom("Nunito", size: 14))
                .foregroundColor(.black.opacity(0.6))

            HStack(alignment: .top, spacing: 14) {
                ChatCLIToolStatusRow(
                    tool: .codex,
                    status: codexStatus,
                    onInstall: { onInstall(.codex) }
                )
                ChatCLIToolStatusRow(
                    tool: .claude,
                    status: claudeStatus,
                    onInstall: { onInstall(.claude) }
                )
            }

            Text("cli_tip_switch")
                .font(.custom("Nunito", size: 12))
                .foregroundColor(.black.opacity(0.5))

            VStack(alignment: .leading, spacing: 10) {
                Text("cli_choose_provider")
                    .font(.custom("Nunito", size: 13))
                    .fontWeight(.semibold)
                    .foregroundColor(.black.opacity(0.65))
                HStack(spacing: 12) {
                    ForEach(CLITool.allCases, id: \.self) { tool in
                        selectionButton(for: tool)
                    }
                }
            }
            .padding(16)
            .background(Color.white.opacity(0.5))
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.black.opacity(0.05), lineWidth: 1)
            )
            
            HStack {
                DayflowSurfaceButton(
                    action: {
                        if !isChecking {
                            onRetry()
                        }
                    },
                    content: {
                        HStack(spacing: 8) {
                            if isChecking {
                                ProgressView().scaleEffect(0.7)
                            } else {
                                Image(systemName: "arrow.clockwise").font(.system(size: 13, weight: .semibold))
                            }
                            Text(isChecking ? "Checking…" : "Re-check")
                                .font(.custom("Nunito", size: 14))
                                .fontWeight(.semibold)
                        }
                    },
                    background: accentColor,
                    foreground: .white,
                    borderColor: .clear,
                    cornerRadius: 8,
                    horizontalPadding: 20,
                    verticalPadding: 10,
                    showOverlayStroke: true
                )
                .disabled(isChecking)
                
                Spacer()
                
                nextButton()
                    .opacity(canContinue ? 1.0 : 0.5)
                    .allowsHitTesting(canContinue)
            }
        }
    }
    
    private var canContinue: Bool {
        guard let selectedTool else { return false }
        return isToolAvailable(selectedTool)
    }
    
    private func isToolAvailable(_ tool: CLITool) -> Bool {
        switch tool {
        case .codex:
            if codexStatus.isInstalled { return true }
            return codexReport?.resolvedPath != nil
        case .claude:
            if claudeStatus.isInstalled { return true }
            return claudeReport?.resolvedPath != nil
        }
    }
    
    @ViewBuilder
    private func selectionButton(for tool: CLITool) -> some View {
        let enabled = isToolAvailable(tool)
        Button(action: {
            if enabled {
                onSelectTool(tool)
            }
        }) {
            HStack(spacing: 6) {
                Image(systemName: selectedTool == tool ? "checkmark.circle.fill" : "circle")
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundColor(enabled ? accentColor : Color.gray.opacity(0.6))
                VStack(alignment: .leading, spacing: 2) {
                    Text(tool.shortName)
                        .font(.custom("Nunito", size: 13))
                        .fontWeight(.semibold)
                        .foregroundColor(.black.opacity(enabled ? 0.85 : 0.4))
                    Text(enabled ? "Ready to use" : "Install to enable")
                        .font(.custom("Nunito", size: 11))
                        .foregroundColor(.black.opacity(enabled ? 0.5 : 0.35))
                }
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 10)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(
                RoundedRectangle(cornerRadius: 10)
                    .fill(selectedTool == tool ? Color.white.opacity(0.9) : Color.white.opacity(0.5))
            )
            .overlay(
                RoundedRectangle(cornerRadius: 10)
                    .stroke(selectedTool == tool ? accentColor.opacity(0.4) : Color.black.opacity(0.05), lineWidth: 1)
            )
        }
        .buttonStyle(.plain)
        .disabled(!enabled)
        .opacity(enabled ? 1.0 : 0.5)
    }
}

struct ChatCLIToolStatusRow: View {
    let tool: CLITool
    let status: CLIDetectionState
    let onInstall: () -> Void

    private let accentColor = Color(red: 0.25, green: 0.17, blue: 0)

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            // Icon and title row
            HStack(spacing: 10) {
                Image(systemName: tool.iconName)
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundColor(.black.opacity(0.75))
                    .frame(width: 30, height: 30)
                    .background(Color.white.opacity(0.7))
                    .cornerRadius(6)

                Text(tool.shortName)
                    .font(.custom("Nunito", size: 15))
                    .fontWeight(.semibold)
                    .foregroundColor(.black.opacity(0.9))

                Spacer()

                statusView
            }

            // Version info if installed
            if let detail = status.detailMessage, !detail.isEmpty {
                Text(detail)
                    .font(.custom("Nunito", size: 11))
                    .foregroundColor(.black.opacity(0.55))
                    .lineLimit(1)
            }

            // Install button if needed
            if shouldShowInstallButton {
                DayflowSurfaceButton(
                    action: onInstall,
                    content: {
                        HStack(spacing: 6) {
                            Image(systemName: "arrow.down.circle.fill").font(.system(size: 11, weight: .semibold))
                            Text(installLabel)
                                .font(.custom("Nunito", size: 12))
                                .fontWeight(.semibold)
                        }
                    },
                    background: .white.opacity(0.85),
                    foreground: accentColor,
                    borderColor: accentColor.opacity(0.35),
                    cornerRadius: 6,
                    horizontalPadding: 12,
                    verticalPadding: 6,
                    showOverlayStroke: true
                )
            }
        }
        .padding(14)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color.white.opacity(0.6))
        .cornerRadius(12)
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Color.black.opacity(0.05), lineWidth: 1)
        )
    }

    @ViewBuilder
    private var statusView: some View {
        switch status {
        case .checking, .unknown:
            HStack(spacing: 5) {
                ProgressView().scaleEffect(0.5)
                Text(status.statusLabel)
                    .font(.custom("Nunito", size: 11))
                    .foregroundColor(accentColor)
            }
            .padding(.horizontal, 10)
            .padding(.vertical, 5)
            .background(accentColor.opacity(0.12))
            .cornerRadius(999)
        case .installed:
            Text(status.statusLabel)
                .font(.custom("Nunito", size: 11))
                .fontWeight(.semibold)
                .foregroundColor(Color(red: 0.13, green: 0.7, blue: 0.23))
                .padding(.horizontal, 10)
                .padding(.vertical, 5)
                .background(Color(red: 0.13, green: 0.7, blue: 0.23).opacity(0.17))
                .cornerRadius(999)
        case .notFound:
            Text(status.statusLabel)
                .font(.custom("Nunito", size: 11))
                .fontWeight(.semibold)
                .foregroundColor(Color(hex: "E91515"))
                .padding(.horizontal, 10)
                .padding(.vertical, 5)
                .background(Color(hex: "FFD1D1"))
                .cornerRadius(999)
        case .failed:
            Text(status.statusLabel)
                .font(.custom("Nunito", size: 11))
                .fontWeight(.semibold)
                .foregroundColor(Color(red: 0.91, green: 0.34, blue: 0.16))
                .padding(.horizontal, 10)
                .padding(.vertical, 5)
                .background(Color(red: 0.91, green: 0.34, blue: 0.16).opacity(0.18))
                .cornerRadius(999)
        }
    }

    private var shouldShowInstallButton: Bool {
        switch status {
        case .notFound, .failed:
            return tool.installURL != nil
        default:
            return false
        }
    }

    private var installLabel: String {
        switch status {
        case .failed:
            return "Setup guide"
        default:
            return "Install"
        }
    }
}

struct DebugField: View {
    let label: String
    let value: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(label)
                .font(.custom("Nunito", size: 11))
                .fontWeight(.semibold)
                .foregroundColor(.black.opacity(0.55))
            ScrollView(.vertical, showsIndicators: true) {
                Text(value)
                    .font(.system(.footnote, design: .monospaced))
                    .foregroundColor(.black.opacity(0.75))
                    .textSelection(.enabled)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(8)
                    .background(Color.white.opacity(0.85))
                    .cornerRadius(6)
            }
            .frame(maxHeight: 100)
        }
    }
}

struct DebugCommandConsole: View {
    @Binding var command: String
    let output: String
    let isRunning: Bool
    let runAction: () -> Void
    
    private let accentColor = Color(red: 0.25, green: 0.17, blue: 0)
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("cli_run_command")
                .font(.custom("Nunito", size: 13))
                .fontWeight(.semibold)
                .foregroundColor(.black.opacity(0.7))
            Text("cli_path_help")
                .font(.custom("Nunito", size: 12))
                .foregroundColor(.black.opacity(0.55))
            HStack(spacing: 10) {
                TextField("Command", text: $command)
                    .textFieldStyle(.roundedBorder)
                    .font(.system(.body, design: .monospaced))
                DayflowSurfaceButton(
                    action: runAction,
                    content: {
                        HStack(spacing: 6) {
                            if isRunning {
                                ProgressView().scaleEffect(0.7)
                            } else {
                                Image(systemName: "play.fill").font(.system(size: 12, weight: .semibold))
                            }
                            Text(isRunning ? "Running..." : "Run")
                                .font(.custom("Nunito", size: 13))
                                .fontWeight(.semibold)
                        }
                    },
                    background: accentColor,
                    foreground: .white,
                    borderColor: .clear,
                    cornerRadius: 8,
                    horizontalPadding: 14,
                    verticalPadding: 10,
                    showOverlayStroke: true
                )
                .disabled(isRunning)
            }
            ScrollView {
                Text(output.isEmpty ? "Output will appear here" : output)
                    .font(.system(.footnote, design: .monospaced))
                    .foregroundColor(.black.opacity(output.isEmpty ? 0.4 : 0.75))
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(10)
                    .background(Color.white.opacity(0.85))
                    .cornerRadius(8)
            }
            .frame(maxHeight: 160)
        }
        .padding(16)
        .background(Color.white.opacity(0.55))
        .cornerRadius(16)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(Color.black.opacity(0.05), lineWidth: 1)
        )
    }
}
