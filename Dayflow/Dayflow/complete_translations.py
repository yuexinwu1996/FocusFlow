#!/usr/bin/env python3
"""
Add comprehensive Chinese translations to Localizable.xcstrings
"""

import json

# Complete translation dictionary
COMPLETE_TRANSLATIONS = {
    # Provider Setup Strings
    "Choose your local AI engine": "选择你的本地 AI 引擎",
    "For local use, LM Studio is the most reliable; Ollama has a known thinking bug in onboarding (can't turn thinking off) and performance is unreliable.": "对于本地使用，LM Studio 是最可靠的；Ollama 在入门时有一个已知的思考错误（无法关闭思考）且性能不可靠。",
    "Download LM Studio": "下载 LM Studio",
    "Already have a local server? Make sure it's OpenAI-compatible. You can set a custom base URL in the next step.": "已经有本地服务器？确保它与 OpenAI 兼容。你可以在下一步设置自定义基础 URL。",
    "Install Qwen3-VL 4B": "安装 Qwen3-VL 4B",
    "After installing Ollama, run this in your terminal to download the model (≈5GB):": "安装 Ollama 后，在终端中运行以下命令下载模型（≈5GB）：",
    "Run this command:": "运行此命令：",
    "Downloads Qwen3 Vision 4B for Ollama": "为 Ollama 下载 Qwen3 Vision 4B",
    "After installing LM Studio, download the recommended model:": "安装 LM Studio 后，下载推荐的模型：",
    "Download Qwen3-VL 4B in LM Studio": "在 LM Studio 中下载 Qwen3-VL 4B",
    "This will open LM Studio and prompt you to download the model (≈3GB).": "这将打开 LM Studio 并提示你下载模型（≈3GB）。",
    "Once downloaded, turn on 'Local Server' in LM Studio (default http://localhost:1234)": "下载后，在 LM Studio 中打开'本地服务器'（默认 http://localhost:1234）",
    "Manual setup:": "手动设置：",
    "1. Open LM Studio → Models tab": "1. 打开 LM Studio → 模型标签",
    "2. Search for 'Qwen3-VL-4B' and install the Instruct variant": "2. 搜索 'Qwen3-VL-4B' 并安装 Instruct 变体",

    # API Key & Testing
    "Get your Gemini API key": "获取你的 Gemini API 密钥",
    "Google's Gemini offers a generous free tier that should allow you to run Dayflow ~15 hours a day for free - no credit card required": "Google 的 Gemini 提供了慷慨的免费层，应该允许你每天免费运行 Dayflow 约 15 小时 - 无需信用卡",
    "Visit Google AI Studio": "访问 Google AI Studio",
    "Create a new API key and copy it": "创建一个新的 API 密钥并复制它",
    "Paste your Gemini API key below": "在下方粘贴你的 Gemini API 密钥",
    "Enter API key": "输入 API 密钥",
    "Get API key": "获取 API 密钥",
    "Open Google AI Studio": "打开 Google AI Studio",
    "Test connection": "测试连接",
    "Testing": "测试中",
    "Complete Setup": "完成设置",
    "Test Required": "需要测试",

    # LLM/CLI Setup
    "Connect ChatGPT or Claude": "连接 ChatGPT 或 Claude",
    "Which tool are you using?": "你正在使用哪个工具？",
    "Dayflow can talk to ChatGPT (via the Codex CLI) or Claude Code. You only need one installed and signed in on this Mac. After installing, run `codex auth` or `claude login` in Terminal to connect it to your account.": "Dayflow 可以与 ChatGPT（通过 Codex CLI）或 Claude Code 对话。你只需要在这台 Mac 上安装并登录其中一个。安装后，在终端中运行 `codex auth` 或 `claude login` 以连接到你的账户。",
    "Select ChatGPT or Claude above before running the test.": "在运行测试之前，请在上方选择 ChatGPT 或 Claude。",
    "We'll ask your CLI a simple question to verify it's working and signed in.": "我们会向你的 CLI 提出一个简单的问题来验证它是否正常工作并已登录。",
    "Tip: Once both are installed, you can choose which provider Dayflow uses from Settings → AI Provider.": "提示：一旦两者都安装完成，你可以从设置 → AI 提供商中选择 Dayflow 使用哪个提供商。",

    # Local Model
    "Use any OpenAI-compatible VLM": "使用任何与 OpenAI 兼容的 VLM",
    "Which local runtime are you using?": "你正在使用哪个本地运行时？",
    "LM Studio": "LM Studio",
    "Ollama": "Ollama",
    "Custom": "自定义",
    "Base URL": "基础 URL",
    "Model ID": "模型 ID",
    "API key (optional)": "API 密钥（可选）",
    "Stored locally in UserDefaults and sent as a Bearer token for custom endpoints (LiteLLM, OpenRouter, etc.)": "本地存储在 UserDefaults 中，并作为 Bearer 令牌发送到自定义端点（LiteLLM、OpenRouter 等）",
    "vision-capable": "支持视觉",
    "Advanced users can pick any": "高级用户可以选择任何",
    "LLM, but we strongly recommend using Qwen3-VL 4B based on our internal benchmarks.": "LLM，但根据我们的内部基准测试，我们强烈建议使用 Qwen3-VL 4B。",
    "Make sure your server exposes the OpenAI Chat Completions API and has Qwen3-VL 4B (or Qwen2.5-VL 3B if you need the legacy model) installed.": "确保你的服务器公开了 OpenAI Chat Completions API，并安装了 Qwen3-VL 4B（如果需要旧模型，则为 Qwen2.5-VL 3B）。",
    "This model enables Dayflow to understand what's on your screen": "此模型使 Dayflow 能够理解你屏幕上的内容",

    # Settings - Storage
    "Recording Status": "录制状态",
    "Run status check": "运行状态检查",
    "Checking…": "检查中…",
    "Last checked \\(relativeDate(last))": "上次检查 \\(relativeDate(last))",
    "Recording": "录制中",
    "Recording is off": "录制已关闭",
    "Dayflow recording is currently turned off, so cards aren't being produced.": "Dayflow 录制当前已关闭，因此不会生成卡片。",
    "Access granted!": "已授予访问权限！",
    "macOS will ask for screen recording permission to enable activity tracking.": "macOS 将请求屏幕录制权限以启用活动跟踪。",
    "Ensure Dayflow can capture your screen": "确保 Dayflow 可以捕获你的屏幕",
    "Permission Required": "需要权限",
    "Disk usage": "磁盘使用情况",
    "Open folders or adjust per-type storage caps": "打开文件夹或调整每种类型的存储上限",
    "Record": "录制",
    "Timelapse": "延时摄影",
    "Adjust storage limit": "调整存储限制",
    "Lower \\(categoryName) limit?": "降低 \\(categoryName) 限制？",
    "Reducing the \\(categoryName) limit to \\(option.label) will immediately delete the oldest \\(categoryName) data to stay under the new cap.": "将 \\(categoryName) 限制降低到 \\(option.label) 将立即删除最旧的 \\(categoryName) 数据以保持在新上限之下。",

    # Settings - Providers
    "Active provider and runtime details": "活动提供商和运行时详细信息",
    "Choose which provider Dayflow should use": "选择 Dayflow 应使用的提供商",
    "Provider options": "提供商选项",
    "Switch providers at any time": "随时切换提供商",
    "Choose which Gemini model Dayflow should prioritize": "选择 Dayflow 应优先使用的 Gemini 模型",
    "Gemini model": "Gemini 模型",
    "Gemini model preference": "Gemini 模型偏好",
    "Choose your Gemini model. If you're on the free tier, pick 3 Flash, it's the most powerful model and is completely free to use. If you're on a paid plan, which is not recommended, I recommend 2.5 Flash-Lite to minimize costs.": "选择你的 Gemini 模型。如果你使用免费层，请选择 3 Flash，它是最强大的模型且完全免费使用。如果你使用付费计划（不建议），我建议使用 2.5 Flash-Lite 以最小化成本。",
    "Dayflow automatically downgrades if your chosen model is rate limited or unavailable.": "如果你选择的模型受到速率限制或不可用，Dayflow 会自动降级。",
    "Connection health": "连接健康状况",
    "Run a quick test for the active provider": "为活动提供商运行快速测试",
    "Edit configuration": "编辑配置",
    "Upgrade local model": "升级本地模型",
    "Manage local model": "管理本地模型",
    "Upgrade to Qwen3VL for a big improvement in quality.": "升级到 Qwen3VL 以大幅提高质量。",
    "Upgrade to \\(preset.displayName)": "升级到 \\(preset.displayName)",
    "Upgrade now": "立即升级",
    "Keep Qwen2.5": "保留 Qwen2.5",
    "Dayflow Pro diagnostics coming soon": "Dayflow Pro 诊断即将推出",

    # Prompt Customization
    "Gemini prompt customization": "Gemini 提示自定义",
    "Override Dayflow's defaults to tailor card generation": "覆盖 Dayflow 的默认设置以定制卡片生成",
    "Overrides apply only when their toggle is on. Unchecked sections fall back to Dayflow's defaults.": "覆盖仅在开关打开时应用。未选中的部分将回退到 Dayflow 的默认值。",
    "Reset to Dayflow defaults": "重置为 Dayflow 默认值",
    "Local prompt customization": "本地提示自定义",
    "Customize the local model prompts for summary and title generation.": "自定义本地模型的摘要和标题生成提示。",
    "ChatGPT / Claude prompt customization": "ChatGPT / Claude 提示自定义",
    "Adjust the prompts used for local timeline summaries": "调整用于本地时间轴摘要的提示",
    "TITLE": "标题",
    "SUMMARY": "摘要",
    "DETAILED SUMMARY": "详细摘要",
    "Prompt text": "提示文本",

    # Settings - Other
    "App preferences": "应用偏好设置",
    "General toggles and telemetry settings": "常规开关和遥测设置",
    "Quick utilities": "快速工具",
    "Debug": "调试",
    "Reach out": "联系",
    "Email Jerry": "给 Jerry 发邮件",
    "Join Discord": "加入 Discord",
    "Email works great if you want to drop a quick note, Discord if you want to join the community, and if you'd prefer to chat, find some time on my calendar - I'd love to dig into why Dayflow is or isn't working well for you.": "如果你想快速留言，电子邮件很合适；如果你想加入社区，使用 Discord；如果你更喜欢聊天，在我的日历上找个时间 - 我很想深入了解 Dayflow 对你来说为什么好用或不好用。",
    "Run a command as Dayflow": "以 Dayflow 身份运行命令",
    "Helpful for checking PATH differences. We run using the same environment as the detection step.": "有助于检查 PATH 差异。我们使用与检测步骤相同的环境运行。",
    "Terminal command:": "终端命令：",
    "Copy the code below and try running it in your terminal": "复制下面的代码并尝试在终端中运行",
    "Debug output:": "调试输出：",
    "Copy logs": "复制日志",
    "I'd like to share this log to the developer to help improve the product.": "我想与开发者分享此日志以帮助改进产品。",

    # Timeline & Activity
    "Your day so far": "你到目前为止的一天",
    "Your day so far is a preview of what's to come in Dashboard. This feature is still in beta and may change rapidly.": "你到目前为止的一天是仪表板即将推出功能的预览。此功能仍处于测试阶段，可能会快速变化。",
    "No cards yet": "还没有卡片",
    "Come back after a few timeline cards appear.": "在出现几张时间轴卡片后再回来。",
    "Cards are generated about every 15 minutes. If Dayflow is on and no cards show up within 30 minutes, please report a bug.": "卡片大约每 15 分钟生成一次。如果 Dayflow 已开启，30 分钟内没有卡片出现，请报告错误。",
    "to update your data.": "以更新你的数据。",
    "This data will update every 15 minutes. Check back throughout the day to gain new understanding on your workflow.": "此数据每 15 分钟更新一次。全天定期检查以获得对工作流程的新理解。",
    "Edit categories to calculate distractions.": "编辑分类以计算分心情况。",
    "Edit categories to calculate focus.": "编辑分类以计算专注情况。",

    # Activity Details
    "Edit title and description": "编辑标题和描述",
    "Regenerate summary": "重新生成摘要",
    "Generating summary...": "生成摘要中...",
    "Dayflow summary": "Dayflow 摘要",
    "AI-Powered Insights": "AI 驱动的洞察",
    "If you find that your activities are summarized inaccurately, try editing the descriptions of your categories to improve Dayflow's accuracy.": "如果你发现活动摘要不准确，请尝试编辑类别描述以提高 Dayflow 的准确性。",
    "To help Dayflow organize your activities more accurately, try adding more details to the descriptions in your categories": "为了帮助 Dayflow 更准确地组织你的活动，请尝试在类别描述中添加更多详细信息",

    # Category Examples
    "Professional, school, or career-focused tasks (coding, design, meetings).": "专业、学校或职业导向的任务（编码、设计、会议）。",
    "Research": "研究",
    "Planning": "计划",
    "Break": "休息",
    "Coding session": "编码会话",
    "Brainstorming with Chat GPT": "与 Chat GPT 头脑风暴",
    "Browsing TripAdvisor": "浏览 TripAdvisor",
    "Comparing flights": "比较航班",
    "Email responses": "电子邮件回复",
    "Calendar": "日历",

    # Timeline Review
    "Swipe on each card on your Timeline to review your day.": "在时间轴上的每张卡片上滑动以回顾你的一天。",
    "You've reviewed all your activities so far.\\nThe Timeline right panel will be updated with your rating.": "你已经回顾了到目前为止的所有活动。\\n时间轴右侧面板将根据你的评分更新。",

    # Journal
    "We're slowly letting people into the beta as we iterate and improve the experience. If you choose to participate in the beta, you acknowledge that you may encounter bugs and agree to provide feedback.": "在我们迭代和改进体验时，我们正在慢慢让人们进入测试版。如果你选择参与测试版，你承认可能会遇到错误并同意提供反馈。",
    "Dayflow helps you track your daily and longer term pursuits, gives you the space to reflect, and generates a summary of each day.": "Dayflow 帮助你跟踪每日和长期追求，给你反思的空间，并生成每天的摘要。",
    "Long term goals": "长期目标",
    "Return near the end of your day to reflect on your intentions. Let Dayflow generate a narrative summary based on the activities on your Timeline.": "在一天快结束时回来反思你的意图。让 Dayflow 根据时间轴上的活动生成叙述性摘要。",
    "Set daily intentions and track your progress": "设定每日意图并跟踪你的进度",
    "Set recurring notifications to remind yourself to set your intentions and reflect.": "设置定期通知以提醒自己设定意图并反思。",
    "Repeat on": "重复于",
    "Summary from yesterday": "昨天的摘要",
    "Summarizing your day recorded on your timeline…": "总结你在时间轴上记录的一天…",
    "No journal entry for this day": "这一天没有日记条目",
    "Need at least 1 hour of timeline activity to summarize": "需要至少 1 小时的时间轴活动才能总结",
    "Notes for today": "今天的笔记",
    "Your reflections": "你的反思",
    "Your review": "你的回顾",
    "EARLY ACCESS": "早期访问",

    # Misc UI
    "Before you begin": "在你开始之前",
    "Choose engine": "选择引擎",
    "Check installations": "检查安装",
    "Install model": "安装模型",
    "Setup": "设置",
    "Current configuration": "当前配置",
    "Processing": "处理中",
    "Part 1 of 2": "第 1 部分，共 2 部分",
    "Part 2 of 2": "第 2 部分，共 2 部分",
    "Subtle": "微妙",
    "Count: \\(count)": "计数：\\(count)",
    "Dayflow Pro": "Dayflow Pro",
    "Custom model": "自定义模型",
    "AIza...": "AIza...",
    "Thanks for using Dayflow": "感谢使用 Dayflow",
    "Thank you!": "谢谢！",

    # Privacy & Security
    "Your privacy is guaranteed: All recordings stay on your Mac. With local AI models, even processing happens on-device. Nothing leaves your computer.": "你的隐私得到保证：所有录制内容都保留在你的 Mac 上。使用本地 AI 模型，即使处理也在设备上进行。没有任何东西离开你的计算机。",

    # Errors & Messages
    "If you get stuck here, you can go back and choose the 'Bring your own key' option — it only takes a minute to set up.": "如果你在这里卡住了，可以返回并选择'自带密钥'选项 — 只需一分钟即可设置。",
    "Configure WhatsNewConfiguration.configuredRelease to preview.": "配置 WhatsNewConfiguration.configuredRelease 以预览。",
    "Follow the steps below, run a quick test, and Dayflow will switch you over automatically.": "按照下面的步骤操作，运行快速测试，Dayflow 将自动为你切换。",
    "Once the test succeeds, Dayflow updates your settings to \\(preset.displayName) automatically.": "测试成功后，Dayflow 会自动将你的设置更新为 \\(preset.displayName)。",
    "This will download the \\(LocalModelPreset.qwen3VL4B.displayName) model (about 5GB)": "这将下载 \\(LocalModelPreset.qwen3VL4B.displayName) 模型（约 5GB）",

    # What's New
    "Happy Holidays! Big updates + Gemini Flash 3": "节日快乐！重大更新 + Gemini Flash 3",
    "What's New in \\(releaseNote.version) 🎉": "\\(releaseNote.version) 的新功能 🎉",

    # Other categories
    "This step is optional. You can customize the categories or create new ones anytime while using Dayflow.": "此步骤是可选的。你可以在使用 Dayflow 时随时自定义类别或创建新类别。",
    "This step is optional. You can change the colors anytime while using Dayflow.": "此步骤是可选的。你可以在使用 Dayflow 时随时更改颜色。",
}

def add_translations():
    """Add translations to existing xcstrings file"""
    # Load existing file
    with open('Localizable.xcstrings', 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0

    # Update translations
    for key, entry in data["strings"].items():
        if "localizations" in entry and "zh-Hans" in entry["localizations"]:
            zh_hans = entry["localizations"]["zh-Hans"]["stringUnit"]
            en_value = entry["localizations"]["en"]["stringUnit"]["value"]

            # If marked as needs_translation and we have a translation
            if zh_hans.get("state") == "needs_translation" and en_value in COMPLETE_TRANSLATIONS:
                zh_hans["value"] = COMPLETE_TRANSLATIONS[en_value]
                zh_hans["state"] = "translated"
                updated_count += 1

    # Save updated file
    with open('Localizable.xcstrings', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Count final stats
    total = len(data["strings"])
    translated = sum(1 for v in data["strings"].values()
                    if v.get("localizations", {}).get("zh-Hans", {}).get("stringUnit", {}).get("state") == "translated")

    print(f"Added {updated_count} new translations")
    print(f"Total: {translated}/{total} strings translated ({translated*100//total}%)")

if __name__ == "__main__":
    add_translations()
