#!/usr/bin/env python3
import json

# Read existing xcstrings
with open("Localizable.xcstrings", "r", encoding="utf-8") as f:
    data = json.load(f)

# New translations for PermissionExplanationDialog
new_translations = [
    ("permission_required", "Permission Required", "需要权限"),
    # Other keys already exist: permission_macos_ask, permission_privacy_guaranteed, grant_permission, cancel
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

print(f"Added {len(new_translations)} new translations for PermissionExplanationDialog")
print(f"Total strings: {len(data['strings'])}")
