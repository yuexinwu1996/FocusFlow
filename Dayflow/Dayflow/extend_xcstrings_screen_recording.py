#!/usr/bin/env python3
import json

# Read existing xcstrings
with open("Dayflow/Localizable.xcstrings", "r", encoding="utf-8") as f:
    data = json.load(f)

# New translations for ScreenRecordingPermissionView
new_translations = [
    # Headers
    ("screen_last_step", "Last step!", "最后一步！"),
    ("screen_recording_title", "Screen Recording", "屏幕录制"),

    # Description
    ("screen_recording_desc", "Screen recordings are stored locally on your Mac and can be processed entirely on-device using local AI models.", "屏幕录制存储在你的 Mac 本地，可以使用本地 AI 模型完全在设备上处理。"),

    # Status messages
    ("screen_permission_granted_msg", "✓ Permission granted! Click Next to continue.", "✓ 权限已授予！点击下一步继续。"),
    ("screen_permission_needs_action", "Turn on Screen Recording for Dayflow, then quit and reopen the app to finish.", "为 Dayflow 开启屏幕录制，然后退出并重新打开应用以完成。"),

    # Buttons
    ("checking", "Checking...", "检查中..."),
    ("grant_permission", "Grant Permission", "授予权限"),
    ("open_system_settings", "Open System Settings", "打开系统设置"),
    ("quit_reopen", "Quit & Reopen", "退出并重新打开"),

    # Navigation (reusing existing if available)
    # "back", "next" should already exist from previous work
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

print(f"Added {len(new_translations)} new translations for ScreenRecordingPermissionView")
print(f"Total strings: {len(data['strings'])}")
