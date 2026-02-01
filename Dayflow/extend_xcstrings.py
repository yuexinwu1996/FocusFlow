#!/usr/bin/env python3
import json

# Read existing xcstrings
with open("Dayflow/Localizable.xcstrings", "r", encoding="utf-8") as f:
    data = json.load(f)

# New translations to add
new_translations = [
    # LLM Selection View
    ("llm_not_sure", "Not sure which to choose? ", "不确定选哪个？"),
    ("llm_gemini_easiest", "Bring your own keys is the easiest setup (30s).", "自备 API 密钥是最简单的设置（30 秒）。"),
    ("llm_switch_anytime", " You can switch at any time in the settings.", " 你可以随时在设置中切换。"),
    ("llm_cli_detected", "You have Codex/Claude CLI installed! ", "你已安装 Codex/Claude CLI！"),
    ("llm_cli_recommended", "We recommend using it for the best experience.", "我们建议使用它以获得最佳体验。"),
    
    # LLM Feature descriptions
    ("llm_local_private", "100% private - everything's processed on your computer", "100% 隐私 - 一切都在你的电脑上处理"),
    ("llm_local_offline", "Works completely offline", "完全离线运行"),
    ("llm_local_less_intelligence", "Significantly less intelligence", "智能程度显著较低"),
    ("llm_local_most_setup", "Requires the most setup", "需要最多设置"),
    ("llm_local_ram", "16GB+ of RAM recommended", "建议 16GB+ 内存"),
    ("llm_local_battery", "Can be battery-intensive", "可能耗电较大"),
    
    ("llm_gemini_intelligent", "Utilizes more intelligent AI via Google's Gemini models", "利用 Google 的 Gemini 模型获得更智能的 AI"),
    ("llm_gemini_free", "Uses Gemini's generous free tier (no credit card needed)", "使用 Gemini 的慷慨免费层（无需信用卡）"),
    ("llm_gemini_faster", "Faster, more accurate than local models", "比本地模型更快、更准确"),
    ("llm_gemini_api_key", "Requires getting an API key (takes 2 clicks)", "需要获取 API 密钥（只需 2 次点击）"),
    
    ("llm_chatgpt_perfect", "Perfect for existing ChatGPT Plus or Claude Pro subscribers", "适合现有 ChatGPT Plus 或 Claude Pro 订阅者"),
    ("llm_chatgpt_superior", "Superior intelligence and reliability", "卓越的智能和可靠性"),
    ("llm_chatgpt_minimal", "Minimal impact - uses <1% of your daily limit", "影响极小 - 使用不到每日限额的 1%"),
    ("llm_chatgpt_cli", "Requires installing Codex or Claude CLI", "需要安装 Codex 或 Claude CLI"),
    ("llm_chatgpt_subscription", "Requires a paid ChatGPT or Claude subscription", "需要付费的 ChatGPT 或 Claude 订阅"),
    
    # Settings View - Tabs
    ("settings_storage_subtitle", "Recording status and disk usage", "录制状态和磁盘使用"),
    ("settings_providers_subtitle", "Manage LLM providers and customize prompts", "管理 LLM 提供商和自定义提示"),
    ("settings_other_subtitle", "General preferences & support", "常规偏好与支持"),
    
    # Settings - Common actions
    ("settings_edit_config", "Edit configuration", "编辑配置"),
    ("settings_reset_defaults", "Reset to Dayflow defaults", "重置为 Dayflow 默认值"),
    ("settings_switch_provider", "Switch", "切换"),
    
    # Settings - Other options
    ("settings_show_journal_debug", "Show Journal debug panel", "显示日志调试面板"),
    ("settings_dock_icon_subtitle", "When off, Dayflow runs as a menu bar–only app.", "关闭时，Dayflow 作为仅菜单栏应用运行。"),
    ("settings_launch_subtitle", "Keeps the menu bar controller running right after you sign in so capture can resume instantly.", "在你登录后立即保持菜单栏控制器运行，以便捕获可以立即恢复。"),
    
    # Permission & Setup
    ("permission_macos_ask", "macOS will ask for screen recording permission to enable activity tracking.", "macOS 将请求屏幕录制权限以启用活动追踪。"),
    ("permission_privacy_guaranteed", "Your privacy is guaranteed: All recordings stay on your Mac. With local AI models, even processing happens on-device. Nothing leaves your computer.", "你的隐私得到保障：所有录制都保留在你的 Mac 上。使用本地 AI 模型，甚至处理也在设备上进行。什么都不会离开你的电脑。"),
    ("permission_quit_reopen", "Quit & Reopen", "退出并重新打开"),
    ("permission_open_settings", "Open System Settings", "打开系统设置"),
    ("permission_turn_on_recording", "Turn on Screen Recording for Dayflow, then quit and reopen the app to finish.", "为 Dayflow 开启屏幕录制，然后退出并重新打开应用以完成。"),
    
    # API Setup
    ("api_get_gemini_key", "Get your Gemini API key", "获取你的 Gemini API 密钥"),
    ("api_gemini_free_tier", "Google's Gemini offers a generous free tier that should allow you to run Dayflow ~15 hours a day for free - no credit card required", "Google 的 Gemini 提供慷慨的免费层，可让你每天免费运行 Dayflow 约 15 小时 - 无需信用卡"),
    ("api_open_google_studio", "Open Google AI Studio", "打开 Google AI Studio"),
    ("api_click_get_key", "Click \"Get API key\" in the top right", "点击右上角的「获取 API 密钥」"),
    ("api_create_copy", "Create a new API key and copy it", "创建新的 API 密钥并复制"),
    ("api_keychain_safe", "Your API key is encrypted and stored in your macOS Keychain - never uploaded anywhere", "你的 API 密钥已加密并存储在 macOS 钥匙串中 - 永远不会上传到任何地方"),
    ("api_complete_setup", "Complete Setup", "完成设置"),
    ("api_key_validation", "API key should start with 'AIza' and be at least 30 characters", "API 密钥应以 'AIza' 开头且至少 30 个字符"),
    
    # Common UI
    ("select_date", "Select Date", "选择日期"),
    ("retry", "Retry", "重试"),
    ("undo", "Undo", "撤销"),
    ("copy", "Copy", "复制"),
    ("copied", "Copied", "已复制"),
    
    # Empty states
    ("no_activity_data", "No activity data yet", "还没有活动数据"),
    ("all_caught_up", "All caught up!", "全部完成！"),
    ("nothing_to_review", "Nothing to review yet", "还没有需要审核的内容"),
    
    # Time-related
    ("tracked_this_week", "tracked this week", "本周追踪"),
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

print(f"Added {len(new_translations)} new translations")
print(f"Total strings: {len(data['strings'])}")
