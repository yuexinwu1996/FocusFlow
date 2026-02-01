#!/usr/bin/env python3
import json

# Read existing xcstrings
with open("Localizable.xcstrings", "r", encoding="utf-8") as f:
    data = json.load(f)

# New translations for HowItWorksView
new_translations = [
    # Main title
    ("how_it_works_title", "How Dayflow Works", "Dayflow 工作原理"),

    # Card 1 - Install and Forget
    ("how_card1_title", "Install and Forget", "安装即忘"),
    ("how_card1_body", "Dayflow takes periodic screen captures to understand what you're working on, all stored privately on your device. You can toggle this whenever you like.", "Dayflow 定期捕获屏幕以了解你正在做什么，所有内容都私密存储在你的设备上。你可以随时切换此功能。"),

    # Card 2 - Privacy by Default
    ("how_card2_title", "Privacy by Default", "默认隐私保护"),
    ("how_card2_body", "Dayflow can run entirely on local AI models, which means your data never leaves your computer. You can also find the source code below - please consider giving it a star on Github!", "Dayflow 可以完全在本地 AI 模型上运行，这意味着你的数据永远不会离开你的电脑。你还可以在下方找到源代码 - 请考虑在 Github 上给它一个星标！"),

    # Card 3 - Understand your Day
    ("how_card3_title", "Understand your Day", "理解你的一天"),
    ("how_card3_body", "Knows the difference between YouTube tutorials and YouTube rabbit holes. Dayflow actually gets what you're working on.", "能区分 YouTube 教程和 YouTube 兔子洞。Dayflow 真正理解你在做什么。"),

    # Buttons
    ("star_on_github", "Star Dayflow on GitHub", "在 GitHub 上为 Dayflow 加星"),
    # "back", "next" already exist
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

print(f"Added {len(new_translations)} new translations for HowItWorksView")
print(f"Total strings: {len(data['strings'])}")
