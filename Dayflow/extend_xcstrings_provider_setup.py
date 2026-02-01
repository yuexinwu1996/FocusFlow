#!/usr/bin/env python3
import json

# Read existing xcstrings
with open("Dayflow/Localizable.xcstrings", "r", encoding="utf-8") as f:
    data = json.load(f)

# New translations for LLMProviderSetupView
new_translations = [
    # Header Titles
    ("setup_header_local", "Use local AI", "使用本地 AI"),
    ("setup_header_cli", "Connect ChatGPT or Claude", "连接 ChatGPT 或 Claude"),
    ("setup_header_gemini", "Gemini", "Gemini"),

    # Common Buttons & Actions
    ("back", "Back", "返回"),
    ("next", "Next", "下一步"),
    ("complete_setup", "Complete Setup", "完成设置"),
    ("test_required", "Test Required", "需要测试"),
    ("testing", "Testing...", "测试中..."),
    ("test_successful", "Test Successful!", "测试成功！"),
    ("test_cli", "Test CLI", "测试 CLI"),
    ("copy_logs", "Copy logs", "复制日志"),

    # Step Titles
    ("step_before_begin", "Before you begin", "开始之前"),
    ("step_choose_engine", "Choose engine", "选择引擎"),
    ("step_install_model", "Install model", "安装模型"),
    ("step_test_connection", "Test connection", "测试连接"),
    ("step_complete", "Complete", "完成"),
    ("step_check_installations", "Check installations", "检查安装"),
    ("step_get_api_key", "Get API key", "获取 API 密钥"),
    ("step_enter_api_key", "Enter API key", "输入 API 密钥"),

    # Information Titles
    ("info_for_experienced", "For experienced users", "面向有经验的用户"),
    ("info_test_connection", "Test Connection", "测试连接"),
    ("info_all_set", "All set!", "全部就绪！"),
    ("info_install_cli", "Install Codex CLI (ChatGPT) or Claude Code", "安装 Codex CLI（ChatGPT）或 Claude Code"),
    ("info_setup", "Setup", "设置"),

    # Local Setup - Engine Selection
    ("local_choose_engine_title", "Choose your local AI engine", "选择你的本地 AI 引擎"),
    ("local_choose_engine_subtitle", "For local use, LM Studio is the most reliable; Ollama has a known thinking bug in onboarding (can't turn thinking off) and performance is unreliable.", "对于本地使用，LM Studio 最可靠；Ollama 在引导过程中存在已知的思考问题（无法关闭思考）且性能不可靠。"),
    ("local_download_lmstudio", "Download LM Studio", "下载 LM Studio"),
    ("local_have_server_note", "Already have a local server? Make sure it's OpenAI-compatible. You can set a custom base URL in the next step.", "已有本地服务器？请确保它兼容 OpenAI。你可以在下一步设置自定义基础 URL。"),
    ("local_which_tool", "Which tool are you using?", "你在使用哪个工具？"),
    ("local_lm_studio", "LM Studio", "LM Studio"),
    ("local_custom_model", "Custom model", "自定义模型"),

    # Local Setup - Model Installation
    ("local_install_qwen_title", "Install Qwen3-VL 4B", "安装 Qwen3-VL 4B"),
    ("local_install_ollama_subtitle", "After installing Ollama, run this in your terminal to download the model (≈5GB):", "安装 Ollama 后，在终端中运行此命令下载模型（约 5GB）："),
    ("local_install_lmstudio_subtitle", "After installing LM Studio, download the recommended model:", "安装 LM Studio 后，下载推荐的模型："),
    ("local_download_qwen_lmstudio", "Download Qwen3-VL 4B in LM Studio", "在 LM Studio 中下载 Qwen3-VL 4B"),
    ("local_lmstudio_open_prompt", "This will open LM Studio and prompt you to download the model (≈3GB).", "这将打开 LM Studio 并提示你下载模型（约 3GB）。"),
    ("local_lmstudio_turn_on_server", "Once downloaded, turn on 'Local Server' in LM Studio (default http://localhost:1234)", "下载后，在 LM Studio 中开启「本地服务器」（默认 http://localhost:1234）"),
    ("local_manual_setup", "Manual setup:", "手动设置："),
    ("local_manual_step1", "1. Open LM Studio → Models tab", "1. 打开 LM Studio → 模型标签页"),
    ("local_manual_step2", "2. Search for 'Qwen3-VL-4B' and install the Instruct variant", "2. 搜索「Qwen3-VL-4B」并安装 Instruct 变体"),
    ("local_use_any_vlm_title", "Use any OpenAI-compatible VLM", "使用任何兼容 OpenAI 的 VLM"),
    ("local_use_any_vlm_subtitle", "Make sure your server exposes the OpenAI Chat Completions API and has Qwen3-VL 4B (or Qwen2.5-VL 3B if you need the legacy model) installed.", "确保你的服务器公开了 OpenAI Chat Completions API，并安装了 Qwen3-VL 4B（如需旧版模型可使用 Qwen2.5-VL 3B）。"),

    # Local Setup - Advanced Text
    ("local_advanced_users_prefix", "Advanced users can pick any ", "高级用户可以选择任何"),
    ("local_vision_capable", "vision-capable", "支持视觉的"),
    ("local_advanced_users_suffix", " LLM, but we strongly recommend using Qwen3-VL 4B based on our internal benchmarks.", " LLM，但根据我们的内部基准测试，我们强烈建议使用 Qwen3-VL 4B。"),

    # Local Setup - Testing
    ("local_test_instruction", "Click the button below to verify your local server responds to a simple chat completion.", "点击下方按钮验证你的本地服务器能响应简单的聊天完成请求。"),
    ("local_complete_message", "Local AI is configured and ready to use with Dayflow.", "本地 AI 已配置完成，可与 Dayflow 一起使用。"),
    ("local_test_error_help", "If you get stuck here, you can go back and choose the 'Bring your own key' option — it only takes a minute to set up.", "如果在这里遇到困难，你可以返回选择「自备密钥」选项 —— 只需一分钟即可完成设置。"),

    # Local Setup - Form Labels
    ("local_base_url", "Base URL", "基础 URL"),
    ("local_model_id", "Model ID", "模型 ID"),
    ("local_api_key_optional", "API key (optional)", "API 密钥（可选）"),
    ("local_api_key_help", "Stored locally in UserDefaults and sent as a Bearer token for custom endpoints (LiteLLM, OpenRouter, etc.)", "存储在本地 UserDefaults 中，作为 Bearer 令牌发送给自定义端点（LiteLLM、OpenRouter 等）"),

    # CLI Setup
    ("cli_intro_message", "If you have a paid ChatGPT/Claude account, you can have Dayflow tap into your existing usage limits. Everything flows through your current account - no extra charges - and you can opt out of training for privacy. You only need one CLI installed and signed in on this Mac; we'll verify it automatically next.", "如果你有付费的 ChatGPT/Claude 账户，可以让 Dayflow 利用你现有的使用额度。一切都通过你当前的账户进行 - 无额外费用 - 你可以选择退出训练以保护隐私。你只需在这台 Mac 上安装并登录一个 CLI；我们将在下一步自动验证。"),
    ("cli_detailed_instruction", "Dayflow can talk to ChatGPT (via the Codex CLI) or Claude Code. You only need one installed and signed in on this Mac. After installing, run `codex auth` or `claude login` in Terminal to connect it to your account.", "Dayflow 可以与 ChatGPT（通过 Codex CLI）或 Claude Code 通信。你只需在这台 Mac 上安装并登录其中一个。安装后，在终端中运行 `codex auth` 或 `claude login` 连接到你的账户。"),
    ("cli_choose_provider", "Choose which provider Dayflow should use", "选择 Dayflow 应使用哪个提供商"),
    ("cli_tip_switch", "Tip: Once both are installed, you can choose which provider Dayflow uses from Settings → AI Provider.", "提示：安装两者后，你可以从设置 → AI 提供商中选择 Dayflow 使用哪个提供商。"),
    ("cli_test_instruction", "Run a quick test to verify your CLI is working and signed in.", "运行快速测试以验证你的 CLI 是否正常工作并已登录。"),
    ("cli_test_question", "We'll ask your CLI a simple question to verify it's working and signed in.", "我们将向你的 CLI 提出一个简单问题以验证其是否正常工作并已登录。"),
    ("cli_select_first", "Select ChatGPT or Claude above before running the test.", "运行测试前请先选择上方的 ChatGPT 或 Claude。"),
    ("cli_complete_message", "ChatGPT and Claude tooling is ready. You can fine-tune which assistant to use anytime from Settings → AI Provider.", "ChatGPT 和 Claude 工具已就绪。你可以随时从设置 → AI 提供商中微调要使用的助手。"),
    ("cli_debug_output", "Debug output:", "调试输出："),
    ("cli_run_command", "Run a command as Dayflow", "以 Dayflow 身份运行命令"),
    ("cli_path_help", "Helpful for checking PATH differences. We run using the same environment as the detection step.", "有助于检查 PATH 差异。我们使用与检测步骤相同的环境运行。"),

    # Gemini Setup
    ("gemini_get_key_title", "Get your Gemini API key", "获取你的 Gemini API 密钥"),
    ("gemini_free_tier_desc", "Google's Gemini offers a generous free tier that should allow you to run Dayflow ~15 hours a day for free - no credit card required", "Google 的 Gemini 提供慷慨的免费层，可让你每天免费运行 Dayflow 约 15 小时 - 无需信用卡"),
    ("gemini_step_1", "1.", "1."),
    ("gemini_visit_studio", "Visit Google AI Studio ", "访问 Google AI Studio "),
    ("gemini_studio_url", "(aistudio.google.com)", "（aistudio.google.com）"),
    ("gemini_step_2", "2.", "2."),
    ("gemini_step_3", "3.", "3."),
    ("gemini_model_choice", "Choose your Gemini model. If you're on the free tier, pick 3 Flash, it's the most powerful model and is completely free to use. If you're on a paid plan, which is not recommended, I recommend 2.5 Flash-Lite to minimize costs.", "选择你的 Gemini 模型。如果使用免费层，请选择 3 Flash，这是最强大的模型且完全免费。如果你是付费计划（不推荐），我建议选择 2.5 Flash-Lite 以降低成本。"),
    ("gemini_test_instruction", "Click the button below to verify your API key works with Gemini", "点击下方按钮验证你的 API 密钥是否适用于 Gemini"),
    ("gemini_complete_message", "Gemini is now configured and ready to use with Dayflow.", "Gemini 现已配置完成，可与 Dayflow 一起使用。"),
    ("gemini_enter_key_title", "Enter your API key:", "输入你的 API 密钥："),
    ("gemini_enter_key_subtitle", "Paste your Gemini API key below", "在下方粘贴你的 Gemini API 密钥"),

    # Terminal Commands
    ("terminal_command_title", "Terminal command:", "终端命令："),
    ("terminal_run_this", "Run this command:", "运行此命令："),
    ("terminal_copy_instruction", "Copy the code below and try running it in your terminal", "复制下方代码并尝试在终端中运行"),
    ("terminal_downloads_qwen", "Downloads Qwen3 Vision 4B for Ollama", "为 Ollama 下载 Qwen3 Vision 4B"),

    # Model Download
    ("model_download_title", "Download the AI model", "下载 AI 模型"),
    ("model_download_subtitle", "This model enables Dayflow to understand what's on your screen", "此模型使 Dayflow 能够理解你屏幕上的内容"),

    # Setup Warnings
    ("setup_advanced_warning", "This path is recommended only if you're comfortable running LLMs locally and debugging technical issues. If terms like vLLM or API endpoint don't ring a bell, we recommend going back and picking ChatGPT, Claude, or Gemini. It's non-technical and takes about 30 seconds.\\n\\nFor local mode, Dayflow recommends Qwen3-VL 4B as the core vision-language model (Qwen2.5-VL 3B remains available if you need a smaller download).", "仅在你熟悉本地运行 LLM 和调试技术问题时才推荐此路径。如果 vLLM 或 API 端点等术语对你来说很陌生，我们建议返回选择 ChatGPT、Claude 或 Gemini。这些方案无需技术知识且只需约 30 秒。\\n\\n对于本地模式，Dayflow 推荐 Qwen3-VL 4B 作为核心视觉语言模型（如需更小的下载，仍可使用 Qwen2.5-VL 3B）。"),
]

for key, en, zh in new_translations:
    if key not in data["strings"]:
        data["strings"][key] = {
            "extractionState": "manual",
            "localizations": {
                "en": {
                    "stringUnit": {
                        "state": "translated",
                        "value": en
                    }
                },
                "zh-Hans": {
                    "stringUnit": {
                        "state": "translated",
                        "value": zh
                    }
                }
            }
        }

# Write back
with open("Dayflow/Localizable.xcstrings", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_translations)} new translations for LLMProviderSetupView")
print(f"Total strings: {len(data['strings'])}")
