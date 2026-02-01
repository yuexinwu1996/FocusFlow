#!/usr/bin/env python3
"""
Generate complete Localizable.xcstrings with English and Chinese translations
"""
import json
from collections import OrderedDict

# Translation dictionary (English -> Chinese)
TRANSLATIONS = {
    # Common
    "Start": "开始",
    "Next": "下一步",
    "Back": "返回",
    "Cancel": "取消",
    "Close": "关闭",
    "OK": "确定",
    "Confirm": "确认",
    "Submit": "提交",
    "Retry": "重试",
    "Undo": "撤销",
    "Switch": "切换",
    "Share": "分享",
    "Copy": "复制",
    "Copied": "已复制",

    # Onboarding
    "Your day has a story. Uncover it with Dayflow.": "你的一天自有故事，让 Dayflow 为你发现。",
    "You are ready to go!": "一切就绪！",
    "Welcome to Dayflow! Let it run for about 30 minutes to gather enough data, then come back to explore your personalized timeline. If you have any issues, feature requests, or feedback please use the feedback tab. I would love to hear from you! ": "欢迎来到 Dayflow！让它运行约 30 分钟以收集足够的数据，然后回来探索你的个性化时间轴。如有问题、功能需求或反馈，请使用反馈标签页。我非常期待听到你的声音！",
    "I have a small favor to ask. I'd love to understand where you first heard about Dayflow.": "我有个小小的请求。我想了解你最初是在哪里听说 Dayflow 的。",
    "Choose a way to run Dayflow": "选择运行 Dayflow 的方式",
    "Not sure which to choose? ": "不确定选哪个？",
    "Bring your own keys is the easiest setup (30s).": "自备 API 密钥是最简单的设置（30 秒）。",
    " You can switch at any time in the settings.": " 你可以随时在设置中切换。",
    "You have Codex/Claude CLI installed! ": "你已安装 Codex/Claude CLI！",
    "We recommend using it for the best experience.": "我们建议使用它以获得最佳体验。",

    # LLM Provider Selection
    "Use local AI": "使用本地 AI",
    "Gemini": "Gemini",
    "ChatGPT or Claude": "ChatGPT 或 Claude",
    "MOST PRIVATE": "最隐私",
    "RECOMMENDED": "推荐",
    "NEW": "新",
    "100% private - everything's processed on your computer": "100% 隐私 - 一切都在你的电脑上处理",
    "Works completely offline": "完全离线运行",
    "Significantly less intelligence": "智能程度显著较低",
    "Requires the most setup": "需要最多设置",
    "16GB+ of RAM recommended": "建议 16GB+ 内存",
    "Can be battery-intensive": "可能耗电较大",
    "Utilizes more intelligent AI via Google's Gemini models": "利用 Google 的 Gemini 模型获得更智能的 AI",
    "Uses Gemini's generous free tier (no credit card needed)": "使用 Gemini 的慷慨免费层（无需信用卡）",
    "Faster, more accurate than local models": "比本地模型更快、更准确",
    "Requires getting an API key (takes 2 clicks)": "需要获取 API 密钥（只需 2 次点击）",
    "Perfect for existing ChatGPT Plus or Claude Pro subscribers": "适合现有 ChatGPT Plus 或 Claude Pro 订阅者",
    "Superior intelligence and reliability": "卓越的智能和可靠性",
    "Minimal impact - uses <1% of your daily limit": "影响极小 - 使用不到每日限额的 1%",
    "Requires installing Codex or Claude CLI": "需要安装 Codex 或 Claude CLI",
    "Requires a paid ChatGPT or Claude subscription": "需要付费的 ChatGPT 或 Claude 订阅",

    # API Key Setup
    "Get your Gemini API key": "获取你的 Gemini API 密钥",
    "Google's Gemini offers a generous free tier that should allow you to run Dayflow ~15 hours a day for free - no credit card required": "Google 的 Gemini 提供慷慨的免费层，可让你每天免费运行 Dayflow 约 15 小时 - 无需信用卡",
    "Open Google AI Studio": "打开 Google AI Studio",
    'Click "Get API key" in the top right': "点击右上角的「获取 API 密钥」",
    "Create a new API key and copy it": "创建新的 API 密钥并复制",
    "Your API key is encrypted and stored in your macOS Keychain - never uploaded anywhere": "你的 API 密钥已加密并存储在 macOS 钥匙串中 - 永远不会上传到任何地方",
    "Complete Setup": "完成设置",
    "API key should start with 'AIza' and be at least 30 characters": "API 密钥应以 'AIza' 开头且至少 30 个字符",

    # Screen Recording Permission
    "Last step!": "最后一步！",
    "Ensure Dayflow can capture your screen": "确保 Dayflow 可以捕获你的屏幕",
    "macOS will ask for screen recording permission to enable activity tracking.": "macOS 将请求屏幕录制权限以启用活动追踪。",
    "Your privacy is guaranteed: All recordings stay on your Mac. With local AI models, even processing happens on-device. Nothing leaves your computer.": "你的隐私得到保障：所有录制都保留在你的 Mac 上。使用本地 AI 模型，甚至处理也在设备上进行。什么都不会离开你的电脑。",
    "Grant Permission": "授予权限",
    "✓ Permission granted! Click Next to continue.": "✓ 权限已授予！点击下一步继续。",
    "Turn on Screen Recording for Dayflow, then quit and reopen the app to finish.": "为 Dayflow 开启屏幕录制，然后退出并重新打开应用以完成。",
    "Open System Settings": "打开系统设置",
    "Quit & Reopen": "退出并重新打开",

    # Menu Bar
    "Pause Dayflow": "暂停 Dayflow",
    "Resume Dayflow": "恢复 Dayflow",
    "Open Dayflow": "打开 Dayflow",
    "Open Recordings": "打开录制文件夹",
    "Check for Updates": "检查更新",
    "Quit Completely": "完全退出",
    "Dayflow paused for ": "Dayflow 已暂停 ",
    "15 Min": "15 分钟",
    "30 Min": "30 分钟",
    "1 Hour": "1 小时",
    "∞": "∞",

    # Settings
    "Settings": "设置",
    "Manage how Dayflow runs": "管理 Dayflow 的运行方式",
    "Storage": "存储",
    "Providers": "提供商",
    "Other": "其他",
    "Recording status and disk usage": "录制状态和磁盘使用",
    "Manage LLM providers and customize prompts": "管理 LLM 提供商和自定义提示",
    "General preferences & support": "常规偏好与支持",
    "Launch Dayflow at login": "登录时启动 Dayflow",
    "Keeps the menu bar controller running right after you sign in so capture can resume instantly.": "在你登录后立即保持菜单栏控制器运行，以便捕获可以立即恢复。",
    "Share crash reports and anonymous usage data": "分享崩溃报告和匿名使用数据",
    "Show Journal debug panel": "显示日志调试面板",
    "Show Dock icon": "显示 Dock 图标",
    "When off, Dayflow runs as a menu bar–only app.": "关闭时，Dayflow 作为仅菜单栏应用运行。",
    "Gemini model": "Gemini 模型",
    "Dayflow automatically downgrades if your chosen model is rate limited or unavailable.": "如果你选择的模型受到速率限制或不可用，Dayflow 会自动降级。",
    "Choose which provider Dayflow should use": "选择 Dayflow 应使用的提供商",
    "Switch providers at any time": "随时切换提供商",
    "Edit configuration": "编辑配置",
    "Reset to Dayflow defaults": "重置为 Dayflow 默认值",
    "Overrides apply only when their toggle is on. Unchecked sections fall back to Dayflow's defaults.": "仅当切换开关打开时才应用覆盖。未选中的部分将回退到 Dayflow 的默认值。",

    # Timeline / Main View
    "Select an activity to view details": "选择一个活动以查看详情",
    "No cards yet": "还没有卡片",
    "Cards are generated about every 15 minutes. If Dayflow is on and no cards show up within 30 minutes, please report a bug.": "卡片大约每 15 分钟生成一次。如果 Dayflow 开启且 30 分钟内没有卡片显示，请报告错误。",
    "Recording is off": "录制已关闭",
    "Dayflow recording is currently turned off, so cards aren't being produced.": "Dayflow 录制当前已关闭，因此不会生成卡片。",
    "Change category": "更改分类",
    "SUMMARY": "摘要",
    "DETAILED SUMMARY": "详细摘要",
    "Select Date": "选择日期",

    # Dashboard
    "Dashboard": "仪表板",
    "This feature is in development. Reach out via the feedback tab if you want to be the first to beta test it!": "此功能正在开发中。如果你想成为第一批测试用户，请通过反馈标签页联系我们！",
    "Ask and track answers to any question about your day, such as 'How many times did I check Twitter today?', 'How long did I spend in Figma?', or 'What was my longest deep-work block?'": "询问并追踪关于你一天的任何问题的答案，例如"今天我查看了多少次 Twitter？"、"我在 Figma 中花了多长时间？"或"我最长的深度工作时间是多久？"",
    "Your day so far": "到目前为止的一天",
    "Your day so far is a preview of what's to come in Dashboard. This feature is still in beta and may change rapidly.": "到目前为止的一天是仪表板即将推出功能的预览。此功能仍处于测试阶段，可能会快速变化。",
    "Total focus time": "总专注时间",
    "Longest focus duration": "最长专注时长",
    "Distractions so far": "到目前为止的分心",
    "Edit categories to calculate distractions.": "编辑分类以计算分心。",
    "Edit categories to calculate focus.": "编辑分类以计算专注。",
    "Your focus": "你的专注",
    "TOTAL": "总计",

    # Journal
    "Dayflow Journal": "Dayflow 日志",
    "BETA": "测试版",
    "Enter access code": "输入访问代码",
    "Get early access": "获取早期访问",
    "Set your intentions today": "设定今天的目标",
    "Dayflow helps you track your daily and longer term goals, gives you the space to reflect, and generates a summary of each day.": "Dayflow 帮助你追踪日常和长期目标，为你提供反思空间，并生成每天的摘要。",
    "Dayflow helps you track your daily and longer term pursuits, gives you the space to reflect, and generates a summary of each day.": "Dayflow 帮助你追踪日常和长期追求，为你提供反思空间，并生成每天的摘要。",
    "Start onboarding": "开始引导",
    "Today's intentions": "今天的目标",
    "Notes for today": "今天的笔记",
    "Long term goals": "长期目标",
    "Today's reflections": "今天的反思",
    "Return near the end of your day to reflect on your intentions.": "在一天快结束时回来反思你的目标。",
    "Return near the end of your day to reflect on your intentions. Let Dayflow generate a narrative summary based on the activities on your Timeline.": "在一天快结束时回来反思你的目标。让 Dayflow 根据时间轴上的活动生成叙述性摘要。",
    "Your reflections": "你的反思",
    "Generating summary...": "生成摘要中...",
    "Need at least 1 hour of timeline activity to summarize": "需要至少 1 小时的时间轴活动才能生成摘要",
    "Dayflow summary": "Dayflow 摘要",
    "Summarizing your day recorded on your timeline…": "总结你时间轴上记录的一天...",
    "Regenerate summary": "重新生成摘要",
    "Set daily intentions and track your progress": "设定每日目标并追踪进度",
    "No journal entry for this day": "这一天没有日志条目",
    "Summary from yesterday": "昨天的摘要",
    "Set today's intentions": "设定今天的目标",
    "Set reminders": "设置提醒",
    "Set recurring notifications to remind yourself to set your intentions and reflect.": "设置重复通知以提醒自己设定目标和反思。",
    "Repeat on": "重复于",

    # Feedback & Support
    "Thank you!": "谢谢！",
    "Tell us more about your feedback": "告诉我们更多关于你的反馈",
    "I'd like to share this log to the developer to help improve the product.": "我想将此日志分享给开发者以帮助改进产品。",
    "Thank you for your feedback!": "感谢你的反馈！",
    "If you find that your activities are summarized inaccurately, try editing the descriptions of your categories to improve Dayflow's accuracy.": "如果你发现活动摘要不准确，请尝试编辑分类的描述以提高 Dayflow 的准确性。",
    "Reach out": "联系我们",
    "Email Jerry": "发邮件给 Jerry",
    "Join Discord": "加入 Discord",
    "Star Dayflow on GitHub": "在 GitHub 上给 Dayflow 点星",
    "Email works great if you want to drop a quick note, Discord if you want to join the community, and if you'd prefer to chat, find some time on my calendar - I'd love to dig into why Dayflow is or isn't working well for you.": "如果你想快速留言，电子邮件很好用；如果你想加入社区，Discord 是不错的选择；如果你更喜欢聊天，可以在我的日历上找时间 - 我很想深入了解 Dayflow 对你来说是否好用。",

    # Categories
    "Create a new category": "创建新分类",
    "Add a category to get started.": "添加一个分类以开始。",
    "Customize your categories": "自定义你的分类",
    "This step is optional. You can customize the categories or create new ones anytime while using Dayflow.": "此步骤是可选的。你可以在使用 Dayflow 时随时自定义分类或创建新分类。",
    "Edit colors": "编辑颜色",
    "This step is optional. You can change the colors anytime while using Dayflow.": "此步骤是可选的。你可以在使用 Dayflow 时随时更改颜色。",
    "Drag to category": "拖动到分类",
    "Edit title and description": "编辑标题和描述",

    # Timeline Review
    "All caught up!": "全部完成！",
    "Nothing to review yet": "还没有需要审核的内容",
    "Swipe on each card on your Timeline to review your day.": "在时间轴上的每张卡片上滑动以审核你的一天。",
    "You've reviewed all your activities so far.\\nThe Timeline right panel will be updated with your rating.": "你已经审核了到目前为止的所有活动。\\n时间轴右侧面板将更新你的评分。",
    "Come back after a few timeline cards appear.": "等几张时间轴卡片出现后再回来。",
    "Your review": "你的审核",
    "Thumbs up": "赞",
    "Thumbs down": "踩",

    # Local AI Setup
    "Choose your local AI engine": "选择你的本地 AI 引擎",
    "Ollama": "Ollama",
    "LM Studio": "LM Studio",
    "Custom": "自定义",
    "For local use, LM Studio is the most reliable; Ollama has a known thinking bug in onboarding (can't turn thinking off) and performance is unreliable.": "对于本地使用，LM Studio 最可靠；Ollama 在引导过程中有已知的思考错误（无法关闭思考），性能不可靠。",
    "Already have a local server? Make sure it's OpenAI-compatible. You can set a custom base URL in the next step.": "已经有本地服务器？确保它兼容 OpenAI。你可以在下一步设置自定义基础 URL。",
    "Download the AI model": "下载 AI 模型",
    "After installing Ollama, run this in your terminal to download the model (≈5GB):": "安装 Ollama 后，在终端中运行此命令以下载模型（约 5GB）：",
    "Download LM Studio": "下载 LM Studio",
    "After installing LM Studio, download the recommended model:": "安装 LM Studio 后，下载推荐的模型：",
    "Download Qwen3-VL 4B in LM Studio": "在 LM Studio 中下载 Qwen3-VL 4B",
    "1. Open LM Studio → Models tab": "1. 打开 LM Studio → 模型选项卡",
    "2. Search for 'Qwen3-VL-4B' and install the Instruct variant": "2. 搜索 'Qwen3-VL-4B' 并安装 Instruct 变体",
    "This will open LM Studio and prompt you to download the model (≈3GB).": "这将打开 LM Studio 并提示你下载模型（约 3GB）。",
    "Once downloaded, turn on 'Local Server' in LM Studio (default http://localhost:1234)": "下载后，在 LM Studio 中打开"本地服务器"（默认 http://localhost:1234）",
    "Base URL": "基础 URL",
    "Model ID": "模型 ID",
    "API key (optional)": "API 密钥（可选）",
    "Stored locally in UserDefaults and sent as a Bearer token for custom endpoints (LiteLLM, OpenRouter, etc.)": "本地存储在 UserDefaults 中，并作为 Bearer token 发送到自定义端点（LiteLLM、OpenRouter 等）",
    "This model enables Dayflow to understand what's on your screen": "此模型使 Dayflow 能够理解你屏幕上的内容",

    # What's New
    "What's New in %@ 🎉": "🎉 %@ 的新功能",
    "Configure WhatsNewConfiguration.configuredRelease to preview.": "配置 WhatsNewConfiguration.configuredRelease 以预览。",
    "View release notes": "查看发布说明",

    # Export
    "Download a Markdown export for any date range": "下载任何日期范围的 Markdown 导出",
    "Export start date": "导出开始日期",
    "Export end date": "导出结束日期",
    "Includes titles, summaries, and details for each card.": "包括每张卡片的标题、摘要和详细信息。",
    "Start date must be on or before end date.": "开始日期必须在结束日期之前或相同。",

    # Storage
    "Open folders or adjust per-type storage caps": "打开文件夹或调整每种类型的存储上限",
    "Adjust storage limit": "调整存储限制",
    "Lower %@ limit?": "降低 %@ 限制？",
    "Reducing the %@ limit to %@ will immediately delete the oldest %@ data to stay under the new cap.": "将 %@ 限制降低到 %@ 将立即删除最旧的 %@ 数据以保持在新上限之下。",

    # Misc
    "Processing": "处理中",
    "Recording": "录制中",
    "Record": "录制",
    "Calendar": "日历",
    "tracked this week": "本周追踪",
    "Copy timeline": "复制时间轴",
    "Copy timeline to clipboard": "将时间轴复制到剪贴板",
    "Copy logs": "复制日志",
    "Debug": "调试",
    "No activity data yet": "还没有活动数据",
    "Permission Required": "需要权限",
    "Access granted!": "已授予访问权限！",
    "Screen Recording": "屏幕录制",
    "Thanks for using Dayflow": "感谢使用 Dayflow",
}

def create_string_entry(key, en_value, zh_value):
    """Create a string entry in xcstrings format"""
    return {
        "extractionState": "manual",
        "localizations": {
            "en": {
                "stringUnit": {
                    "state": "translated",
                    "value": en_value
                }
            },
            "zh-Hans": {
                "stringUnit": {
                    "state": "translated",
                    "value": zh_value
                }
            }
        }
    }

def generate_key(text):
    """Generate a key from English text"""
    # Remove special characters and convert to lowercase
    key = text.lower()

    # Replace spaces with underscores
    key = key.replace(" ", "_")

    # Remove non-alphanumeric characters (except underscores)
    key = ''.join(c for c in key if c.isalnum() or c == '_')

    # Limit length
    if len(key) > 80:
        words = text.split()
        if len(words) > 3:
            key = '_'.join(words[:3]).lower()
            key = ''.join(c for c in key if c.isalnum() or c == '_')

    return key

def main():
    xcstrings = OrderedDict()
    xcstrings["sourceLanguage"] = "en"
    xcstrings["strings"] = OrderedDict()
    xcstrings["version"] = "1.0"

    # Add all translations
    for en_text, zh_text in sorted(TRANSLATIONS.items()):
        key = generate_key(en_text)
        # Ensure unique keys
        original_key = key
        counter = 1
        while key in xcstrings["strings"]:
            key = f"{original_key}_{counter}"
            counter += 1

        xcstrings["strings"][key] = create_string_entry(key, en_text, zh_text)

    # Write to file
    output_path = "Dayflow/Localizable.xcstrings"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(xcstrings, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(xcstrings['strings'])} translations")
    print(f"Written to {output_path}")

if __name__ == '__main__':
    main()
