#!/usr/bin/env python3
import json

# New translations for remaining issues
new_translations = [
    # Date formatting
    ("today", "Today", "今天"),

    # Timeline review/rating
    ("rate_this_summary", "Rate this summary", "评价此摘要"),

    # Language settings
    ("settings_language", "Language", "语言"),
    ("language_english", "English", "English"),
    ("language_chinese", "简体中文", "简体中文"),
]

def main():
    with open("Localizable.xcstrings", "r", encoding="utf-8") as f:
        catalog = json.load(f)

    for key, en_value, zh_value in new_translations:
        if key not in catalog["strings"]:
            catalog["strings"][key] = {
                "extractionState": "manual",
                "localizations": {
                    "en": {"stringUnit": {"state": "translated", "value": en_value}},
                    "zh-Hans": {"stringUnit": {"state": "translated", "value": zh_value}}
                }
            }
            print(f"Added: {key}")
        else:
            print(f"Skipped (exists): {key}")

    with open("Localizable.xcstrings", "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    print(f"\nTotal strings: {len(catalog['strings'])}")

if __name__ == "__main__":
    main()
