#!/usr/bin/env python3
import json

# Read existing xcstrings
with open("Localizable.xcstrings", "r", encoding="utf-8") as f:
    data = json.load(f)

# New translations for TestConnectionView
new_translations = [
    # Button states
    ("test_connection_testing", "Testing connection...", "连接测试中..."),
    ("test_connection_success_btn", "Test Successful!", "测试成功！"),
    ("test_connection_failed_btn", "Test Failed - Try Again", "测试失败 - 重试"),
    ("test_connection_btn", "Test Connection", "测试连接"),

    # Result messages
    ("test_no_api_key", "No API key found. Please enter your API key first.", "未找到 API 密钥。请先输入你的 API 密钥。"),
    ("test_connection_success_msg", "Connection successful! Your API key is working.", "连接成功！你的 API 密钥工作正常。"),
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

print(f"Added {len(new_translations)} new translations for TestConnectionView")
print(f"Total strings: {len(data['strings'])}")
