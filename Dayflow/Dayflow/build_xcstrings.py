#!/usr/bin/env python3
"""
Build comprehensive Localizable.xcstrings with English and Chinese translations
"""

import json
import re
from collections import OrderedDict

# Translation mappings - comprehensive Chinese translations
TRANSLATIONS = {
    # Common UI elements
    "Start": "开始",
    "Next": "下一步",
    "Back": "返回",
    "Continue": "继续",
    "Cancel": "取消",
    "Close": "关闭",
    "Complete": "完成",
    "Confirm": "确认",
    "Submit": "提交",
    "Save": "保存",
    "Undo": "撤销",
    "Retry": "重试",
    "Share": "分享",
    "Edit": "编辑",
    "Delete": "删除",
    "Switch": "切换",
    "Copied": "已复制",

    # Menu items
    "Open Dayflow": "打开 Dayflow",
    "Pause Dayflow": "暂停 Dayflow",
    "Resume Dayflow": "恢复 Dayflow",
    "Open Recordings": "打开录制文件夹",
    "Check for Updates": "检查更新",
    "Quit Completely": "完全退出",
    "Dayflow paused for": "Dayflow 已暂停",
    "15 Min": "15 分钟",
    "30 Min": "30 分钟",
    "1 Hour": "1 小时",

    # Onboarding
    "Your day has a story. Uncover it with Dayflow.": "你的一天自有故事，让 Dayflow 为你发现。",
    "You are ready to go!": "一切就绪！",
    "Welcome to Dayflow! Let it run for about 30 minutes to gather enough data, then come back to explore your personalized timeline. If you have any issues, feature requests, or feedback please use the feedback tab. I would love to hear from you!": "欢迎来到 Dayflow！让它运行约 30 分钟以收集足够的数据，然后回来探索你的个性化时间轴。如有问题、功能需求或反馈，请使用反馈标签页。我非常期待听到你的声音！",
    "I have a small favor to ask. I'd love to understand where you first heard about Dayflow.": "我有个小小的请求。我想了解你最初是在哪里听说 Dayflow 的。",

    # How It Works
    "How Dayflow Works": "Dayflow 工作原理",
    "Install and Forget": "安装即忘",
    "Dayflow takes periodic screen captures to understand what you're working on, all stored privately on your device. You can toggle this whenever you like.": "Dayflow 定期截屏以了解你的工作内容，所有数据都私密存储在你的设备上。你可以随时切换此功能。",
    "Privacy by Default": "默认隐私",
    "Dayflow can run entirely on local AI models, which means your data never leaves your computer. You can also find the source code below - please consider giving it a star on Github!": "Dayflow 可以完全在本地 AI 模型上运行，这意味着你的数据永远不会离开你的计算机。你还可以在下方找到源代码 - 请考虑在 Github 上给它点个星！",
    "Understand your Day": "理解你的一天",
    "Knows the difference between YouTube tutorials and YouTube rabbit holes. Dayflow actually gets what you're working on.": "能区分 YouTube 教程和 YouTube 兔子洞。Dayflow 真正理解你的工作内容。",
    "Star Dayflow on GitHub": "在 GitHub 上为 Dayflow 点星",

    # LLM Selection
    "Choose a way to run Dayflow": "选择运行 Dayflow 的方式",
    "Use local AI": "使用本地 AI",
    "MOST PRIVATE": "最私密",
    "100% private - everything's processed on your computer": "100% 私密 - 一切都在你的计算机上处理",
    "Works completely offline": "完全离线工作",
    "Significantly less intelligence": "智能程度显著降低",
    "Requires the most setup": "需要最多设置",
    "16GB+ of RAM recommended": "建议 16GB+ 内存",
    "Can be battery-intensive": "可能耗电",

    "Gemini": "Gemini",
    "RECOMMENDED": "推荐",
    "NEW": "新",
    "Utilizes more intelligent AI via Google's Gemini models": "通过 Google 的 Gemini 模型使用更智能的 AI",
    "Uses Gemini's generous free tier (no credit card needed)": "使用 Gemini 的慷慨免费层（无需信用卡）",
    "Faster, more accurate than local models": "比本地模型更快、更准确",
    "Requires getting an API key (takes 2 clicks)": "需要获取 API 密钥（只需 2 次点击）",

    "ChatGPT or Claude": "ChatGPT 或 Claude",
    "Perfect for existing ChatGPT Plus or Claude Pro subscribers": "完美适合现有 ChatGPT Plus 或 Claude Pro 订阅者",
    "Superior intelligence and reliability": "卓越的智能和可靠性",
    "Minimal impact - uses <1% of your daily limit": "影响最小 - 使用不到每日限额的 1%",
    "Requires installing Codex or Claude CLI": "需要安装 Codex 或 Claude CLI",
    "Requires a paid ChatGPT or Claude subscription": "需要付费 ChatGPT 或 Claude 订阅",

    "Not sure which to choose?": "不确定选择哪个？",
    "Bring your own keys is the easiest setup (30s).": "自带密钥是最简单的设置（30 秒）。",
    "You can switch at any time in the settings.": "你可以随时在设置中切换。",
    "You have Codex/Claude CLI installed!": "你已安装 Codex/Claude CLI！",
    "We recommend using it for the best experience.": "我们建议使用它以获得最佳体验。",

    # Screen Recording Permission
    "Last step!": "最后一步！",
    "Screen Recording": "屏幕录制",
    "Screen recordings are stored locally on your Mac and can be processed entirely on-device using local AI models.": "屏幕录制内容存储在你的 Mac 本地，可以完全在设备上使用本地 AI 模型处理。",
    "✓ Permission granted! Click Next to continue.": "✓ 权限已授予！点击下一步继续。",
    "Turn on Screen Recording for Dayflow, then quit and reopen the app to finish.": "为 Dayflow 开启屏幕录制，然后退出并重新打开应用以完成。",
    "Grant Permission": "授予权限",
    "Open System Settings": "打开系统设置",
    "Quit & Reopen": "退出并重新打开",
    "Checking...": "检查中...",

    # API Key Input
    "Enter your API key:": "输入你的 API 密钥：",
    "API key should start with 'AIza' and be at least 30 characters": "API 密钥应以 'AIza' 开头且至少 30 个字符",
    "Your API key is encrypted and stored in your macOS Keychain - never uploaded anywhere": "你的 API 密钥已加密并存储在 macOS 钥匙串中 - 永远不会上传到任何地方",

    # Test Connection
    "Test Connection": "测试连接",
    "Testing connection...": "测试连接中...",
    "Test Successful!": "测试成功！",
    "Test Failed - Try Again": "测试失败 - 重试",
    "Connection successful! Your API key is working.": "连接成功！你的 API 密钥正常工作。",
    "No API key found. Please enter your API key first.": "未找到 API 密钥。请先输入你的 API 密钥。",

    # Settings
    "Settings": "设置",
    "Manage how Dayflow runs": "管理 Dayflow 的运行方式",
    "Storage": "存储",
    "Recording status and disk usage": "录制状态和磁盘使用情况",
    "Providers": "提供商",
    "Manage LLM providers and customize prompts": "管理 LLM 提供商并自定义提示",
    "Other": "其他",
    "General preferences & support": "常规偏好设置和支持",

    # Dashboard
    "Dashboard": "仪表板",
    "This feature is in development. Reach out via the feedback tab if you want to be the first to beta test it!": "此功能正在开发中。如果你想成为第一批测试者，请通过反馈标签页联系我们！",
    "Ask and track answers to any question about your day, such as 'How many times did I check Twitter today?', 'How long did I spend in Figma?', or 'What was my longest deep-work block?'": "询问并跟踪关于你一天的任何问题的答案，例如'我今天查看 Twitter 多少次？''我在 Figma 上花了多长时间？'或'我最长的深度工作时段是多久？'",

    # Journal
    "Dayflow Journal": "Dayflow 日记",
    "BETA": "测试版",
    "Enter access code": "输入访问代码",
    "Get early access": "获取早期访问权限",
    "Set your intentions today": "设定今天的意图",
    "Dayflow helps you track your daily and longer term goals, gives you the space to reflect, and generates a summary of each day.": "Dayflow 帮助你跟踪每日和长期目标，给你反思的空间，并生成每天的摘要。",
    "Start onboarding": "开始引导",
    "Set today's intentions": "设定今天的意图",
    "Today's intentions": "今天的意图",
    "What are you working towards?": "你在努力做什么？",
    "What mindset do you want to carry today?": "今天你想保持什么心态？",
    "Return near the end of your day to reflect on your intentions.": "在一天快结束时回来反思你的意图。",
    "Today's reflections": "今天的反思",
    "How was your day? What did you do? How do you feel?": "你今天过得怎么样？你做了什么？你感觉如何？",
    "Set reminders": "设置提醒",
    "Week in review": "本周回顾",

    # Timeline
    "Select an activity to view details": "选择一个活动以查看详情",
    "No activity data yet": "还没有活动数据",
    "Select Date": "选择日期",
    "Review Your Day": "回顾你的一天",
    "Swipe on each card on your Timeline to review your day.": "在时间轴上的每张卡片上滑动以回顾你的一天。",
    "All caught up!": "全部完成！",
    "Nothing to review yet": "还没有需要回顾的",
    "You've reviewed all your activities so far.\\nThe Timeline right panel will be updated with your rating.": "你已经回顾了到目前为止的所有活动。\\n时间轴右侧面板将根据你的评分更新。",

    # Categories
    "Customize your categories": "自定义你的分类",
    "Edit colors": "编辑颜色",
    "Add a category to get started.": "添加一个分类以开始。",
    "Create a new category": "创建新分类",
    "Change category": "更改分类",
    "Drag to category": "拖动到分类",

    # Time tracking
    "Total time captured": "总记录时间",
    "Your focus": "你的专注",
    "Total focus time": "总专注时间",
    "Longest focus duration": "最长专注时长",
    "Distractions so far": "到目前为止的分心",
    "Total time distracted": "总分心时间",
    "tracked this week": "本周跟踪",

    # Feedback
    "Tell us more about your feedback": "告诉我们更多关于你的反馈",
    "Thank you for your feedback!": "感谢你的反馈！",
    "Thumbs up": "点赞",
    "Thumbs down": "不喜欢",

    # Misc
    "Launch Dayflow at login": "登录时启动 Dayflow",
    "Keeps the menu bar controller running right after you sign in so capture can resume instantly.": "登录后立即保持菜单栏控制器运行，以便立即恢复捕获。",
    "Share crash reports and anonymous usage data": "分享崩溃报告和匿名使用数据",
    "Show Dock icon": "显示 Dock 图标",
    "When off, Dayflow runs as a menu bar–only app.": "关闭时，Dayflow 仅作为菜单栏应用运行。",
    "Show Journal debug panel": "显示日记调试面板",
    "View release notes": "查看发布说明",
    "Copy timeline": "复制时间轴",
    "Copy timeline to clipboard": "复制时间轴到剪贴板",
    "Includes titles, summaries, and details for each card.": "包括每张卡片的标题、摘要和详情。",
    "Export timeline": "导出时间轴",
    "Download a Markdown export for any date range": "下载任意日期范围的 Markdown 导出",
    "Export start date": "导出开始日期",
    "Export end date": "导出结束日期",
    "Start date must be on or before end date.": "开始日期必须早于或等于结束日期。",
}

def create_string_unit(en_value, zh_value=None):
    """Create a string unit with English and optionally Chinese translation"""
    result = {
        "en": {
            "stringUnit": {
                "state": "translated",
                "value": en_value
            }
        }
    }

    if zh_value:
        result["zh-Hans"] = {
            "stringUnit": {
                "state": "translated",
                "value": zh_value
            }
        }
    else:
        # If no translation provided, mark as needs translation
        result["zh-Hans"] = {
            "stringUnit": {
                "state": "needs_translation",
                "value": en_value  # Use English as placeholder
            }
        }

    return result

def generate_key(text):
    """Generate a reasonable key from text"""
    # Remove special characters and convert to lowercase
    key = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    key = key.strip().lower()
    # Replace spaces with dots for hierarchy
    key = re.sub(r'\s+', '_', key)

    # Limit length
    if len(key) > 50:
        words = key.split('_')
        key = '_'.join(words[:5])  # Take first 5 words

    return key if key else "unnamed"

def build_xcstrings():
    """Build the complete Localizable.xcstrings file"""

    # Read extracted strings
    with open('extracted_strings.txt', 'r', encoding='utf-8') as f:
        strings = [line.strip() for line in f if line.strip()]

    # Start with existing translations from the current file
    existing = {
        "onboarding.welcome.tagline": ("Your day has a story. Uncover it with Dayflow.", "你的一天自有故事，让 Dayflow 为你发现。"),
        "common.start": ("Start", "开始"),
        "onboarding.completion.title": ("You are ready to go!", "一切就绪！"),
        "onboarding.completion.message": ("Welcome to Dayflow! Let it run for about 30 minutes to gather enough data, then come back to explore your personalized timeline. If you have any issues, feature requests, or feedback please use the feedback tab. I would love to hear from you! ", "欢迎来到 Dayflow！让它运行约 30 分钟以收集足够的数据，然后回来探索你的个性化时间轴。如有问题、功能需求或反馈，请使用反馈标签页。我非常期待听到你的声音！"),
        "onboarding.completion.referral_prompt": ("I have a small favor to ask. I'd love to understand where you first heard about Dayflow.", "我有个小小的请求。我想了解你最初是在哪里听说 Dayflow 的。"),
        "menu.pause_dayflow": ("Pause Dayflow", "暂停 Dayflow"),
        "menu.resume_dayflow": ("Resume Dayflow", "恢复 Dayflow"),
        "menu.open_dayflow": ("Open Dayflow", "打开 Dayflow"),
        "menu.open_recordings": ("Open Recordings", "打开录制文件夹"),
        "menu.check_for_updates": ("Check for Updates", "检查更新"),
        "menu.quit_completely": ("Quit Completely", "完全退出"),
        "menu.paused_for": ("Dayflow paused for ", "Dayflow 已暂停 "),
        "menu.duration.15min": ("15 Min", "15 分钟"),
        "menu.duration.30min": ("30 Min", "30 分钟"),
        "menu.duration.1hour": ("1 Hour", "1 小时"),
        "menu.duration.indefinite": ("∞", "∞"),
    }

    xcstrings = {
        "sourceLanguage": "en",
        "strings": {},
        "version": "1.0"
    }

    # Add existing translations first
    for key, (en, zh) in existing.items():
        xcstrings["strings"][key] = {
            "extractionState": "manual",
            "localizations": create_string_unit(en, zh)
        }

    # Process all extracted strings
    for text in strings:
        # Skip if already in existing
        if any(en == text for en, _ in existing.values()):
            continue

        # Generate key
        key = generate_key(text)

        # Check if we have a translation
        zh_translation = TRANSLATIONS.get(text)

        xcstrings["strings"][key] = {
            "extractionState": "manual",
            "localizations": create_string_unit(text, zh_translation)
        }

    # Write to file
    with open('Localizable.xcstrings', 'w', encoding='utf-8') as f:
        json.dump(xcstrings, f, ensure_ascii=False, indent=2)

    print(f"Generated Localizable.xcstrings with {len(xcstrings['strings'])} strings")

    # Count translations
    translated = sum(1 for v in xcstrings["strings"].values()
                    if v["localizations"].get("zh-Hans", {}).get("stringUnit", {}).get("state") == "translated")
    print(f"Translated: {translated}/{len(xcstrings['strings'])}")

    return xcstrings

if __name__ == "__main__":
    build_xcstrings()
