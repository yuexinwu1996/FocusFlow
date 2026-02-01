#!/usr/bin/env python3
import json

# Read existing xcstrings
with open("Localizable.xcstrings", "r", encoding="utf-8") as f:
    data = json.load(f)

# New translations for MainView/Timeline
new_translations = [
    # ActivityCard
    ("activity_no_cards_yet", "No cards yet", "还没有卡片"),
    ("activity_select_to_view", "Select an activity to view details", "选择活动以查看详细信息"),
    ("activity_change_category", "Change category", "更改类别"),
    ("activity_recording_off", "Recording is off", "录制已关闭"),
    ("activity_dayflow_off_msg", "Dayflow recording is currently turned off, so cards aren't being produced.", "Dayflow 录制当前已关闭，因此不会生成卡片。"),
    ("activity_no_cards_msg", "Cards are generated about every 15 minutes. If Dayflow is on and no cards show up within 30 minutes, please report a bug.", "卡片大约每15分钟生成一次。如果 Dayflow 已开启但30分钟内没有显示卡片，请报告错误。"),
    ("activity_processing", "Processing", "处理中"),
    ("activity_summary", "SUMMARY", "摘要"),
    ("activity_detailed_summary", "DETAILED SUMMARY", "详细摘要"),
    ("activity_time_range", "%@ - %@", "%@ - %@"),

    # Layout (Timeline)
    ("timeline_record", "Record", "录制"),
    ("timeline_recording", "Recording", "录制中"),
    ("timeline_copy", "Copy timeline", "复制时间线"),
    ("timeline_copy_tooltip", "Copy timeline to clipboard", "复制时间线到剪贴板"),
    ("timeline_copied", "Copied", "已复制"),
    ("timeline_hours", "%@ hours", "%@ 小时"),

    # MetricRow
    ("metric_percentage", "%@%%", "%@%%"),

    # Common (may already exist)
    # "retry", "tracked this week" should check existing keys
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

print(f"Added {len(new_translations)} new translations for MainView/Timeline")
print(f"Total strings: {len(data['strings'])}")
