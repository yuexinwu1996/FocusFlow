#!/usr/bin/env python3
import json

# Language settings translations
new_translations = [
    ("settings_language_restart_title", "Restart Required", "需要重启"),
    ("settings_language_restart_msg", "Please restart Dayflow for the language change to take effect.", "请重启 Dayflow 以使语言更改生效。"),
    ("settings_language_restart_now", "Restart Now", "立即重启"),
    ("settings_language_restart_later", "Later", "稍后"),
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
