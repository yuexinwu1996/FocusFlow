#!/usr/bin/env python3
import json

# Read existing xcstrings
with open("Localizable.xcstrings", "r", encoding="utf-8") as f:
    data = json.load(f)

# New translations for SettingsView
new_translations = [
    # Tab titles and headers
    ("settings_tab_storage", "Storage", "存储"),
    ("settings_tab_providers", "Providers", "提供商"),
    ("settings_tab_other", "Other", "其他"),
    ("settings_title", "Settings", "设置"),
    ("settings_subtitle", "Manage how Dayflow runs", "管理 Dayflow 运行方式"),

    # Storage tab
    ("storage_adjust_limit", "Adjust storage limit", "调整存储限制"),
    ("storage_lower_limit_title", "Lower %@ limit?", "降低 %@ 限制？"),
    ("storage_lower_limit_msg", "Reducing the %@ limit to %@ will immediately delete the oldest %@ data to stay under the new cap.", "将 %@ 限制降低到 %@ 将立即删除最旧的 %@ 数据以保持在新的上限以下。"),
    ("confirm", "Confirm", "确认"),
    ("ok", "OK", "确定"),

    # Providers tab
    ("provider_edit_config", "Edit configuration", "编辑配置"),
    ("provider_reset_defaults", "Reset to Dayflow defaults", "重置为 Dayflow 默认值"),
    ("provider_switch", "Switch", "切换"),
    ("provider_overrides_note", "Overrides apply only when their toggle is on. Unchecked sections fall back to Dayflow's defaults.", "覆盖仅在其开关打开时应用。未选中的部分将回退到 Dayflow 的默认值。"),
    ("provider_customize_local", "Customize the local model prompts for summary and title generation.", "自定义本地模型的摘要和标题生成提示。"),
    ("provider_gemini_model", "Gemini model", "Gemini 模型"),
    ("provider_gemini_downgrade", "Dayflow automatically downgrades if your chosen model is rate limited or unavailable.", "如果你选择的模型受到速率限制或不可用，Dayflow 会自动降级。"),
    ("provider_diagnostics_soon", "Dayflow Pro diagnostics coming soon", "Dayflow Pro 诊断即将推出"),

    # Model upgrade
    ("upgrade_to_model", "Upgrade to %@", "升级到 %@"),
    ("upgrade_qwen3_desc", "Upgrade to Qwen3VL for a big improvement in quality.", "升级到 Qwen3VL 以显著提高质量。"),
    ("upgrade_keep_qwen25", "Keep Qwen2.5", "保留 Qwen2.5"),
    ("upgrade_now", "Upgrade now", "立即升级"),
    ("upgrade_follow_steps", "Follow the steps below, run a quick test, and Dayflow will switch you over automatically.", "按照以下步骤操作，运行快速测试，Dayflow 将自动为你切换。"),
    ("upgrade_runtime_question", "Which local runtime are you using?", "你在使用哪个本地运行时？"),
    ("upgrade_runtime_ollama", "Ollama", "Ollama"),
    ("upgrade_runtime_lmstudio", "LM Studio", "LM Studio"),
    ("upgrade_runtime_custom", "Custom", "自定义"),
    ("upgrade_test_success", "Once the test succeeds, Dayflow updates your settings to %@ automatically.", "测试成功后，Dayflow 将自动更新你的设置到 %@。"),
    ("close", "Close", "关闭"),

    # Other tab - many keys already exist from previous work
    ("settings_launch_login", "Launch Dayflow at login", "登录时启动 Dayflow"),
    ("settings_launch_subtitle", "Keeps the menu bar controller running right after you sign in so capture can resume instantly.", "在你登录后立即保持菜单栏控制器运行，以便捕获可以立即恢复。"),
    ("settings_share_analytics", "Share crash reports and anonymous usage data", "共享崩溃报告和匿名使用数据"),
    ("settings_show_journal_debug", "Show Journal debug panel", "显示日志调试面板"),
    ("settings_show_dock_icon", "Show Dock icon", "显示 Dock 图标"),
    ("settings_dock_icon_subtitle", "When off, Dayflow runs as a menu bar–only app.", "关闭时，Dayflow 作为仅菜单栏应用运行。"),
    ("settings_version", "Dayflow v%@", "Dayflow v%@"),
    ("settings_release_notes", "View release notes", "查看发布说明"),
    ("settings_last_checked", "Last checked %@", "上次检查 %@"),

    # Export
    ("export_start_date_label", "Export start date", "导出开始日期"),
    ("export_end_date_label", "Export end date", "导出结束日期"),
    ("export_includes_note", "Includes titles, summaries, and details for each card.", "包括每张卡片的标题、摘要和详细信息。"),
    ("export_date_error", "Start date must be on or before end date.", "开始日期必须在结束日期之前或相同。"),

    # Step numbering (dynamic)
    ("step_number", "%@.", "%@."),
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
with open("Localizable.xcstrings", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_translations)} new translations for SettingsView")
print(f"Total strings: {len(data['strings'])}")
