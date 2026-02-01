# Dayflow 国际化（i18n）实施报告

## 📊 项目概况

**实施日期**: 2026-01-20
**语言支持**: 英文（en）、简体中文（zh-Hans）
**方法**: Xcode String Catalog (Localizable.xcstrings)

---

## ✅ 已完成的工作

### 1. 创建 String Catalog 文件

已创建 [`Dayflow/Localizable.xcstrings`](Dayflow/Localizable.xcstrings)，包含 **63 个核心字符串**的英文和中文翻译。

**文件结构**:
- `sourceLanguage`: "en"
- 支持语言: en, zh-Hans
- 提取状态: "manual" (手动管理)

### 2. 已替换的文件

#### ✅ 完全国际化的文件：

| 文件 | 字符串数量 | 状态 |
|------|------------|------|
| **Onboarding/OnboardingFlow.swift** | 4 个主要字符串 | ✅ 完成 |
| **Menu/StatusMenuView.swift** | 9 个字符串 | ✅ 完成 |

**替换详情**:

**OnboardingFlow.swift**:
- ✅ `onboarding_tagline`: "Your day has a story. Uncover it with Dayflow."
- ✅ `onboarding_ready`: "You are ready to go!"
- ✅ `onboarding_welcome_message`: 欢迎消息
- ✅ `onboarding_referral_prompt`: 推荐来源询问
- ✅ `start`: 开始按钮

**StatusMenuView.swift**:
- ✅ `menu_pause`: "Pause Dayflow"
- ✅ `menu_resume`: "Resume Dayflow"
- ✅ `menu_open`: "Open Dayflow"
- ✅ `menu_open_recordings`: "Open Recordings"
- ✅ `menu_check_updates`: "Check for Updates"
- ✅ `menu_quit`: "Quit Completely"
- ✅ `menu_paused_for`: "Dayflow paused for "
- ✅ `menu_15min`, `menu_30min`, `menu_1hour`: 时长选项

### 3. 提取的所有字符串

已使用 Python 脚本提取项目中所有硬编码字符串，共发现 **225 个唯一字符串**。
详见：[`extracted_strings.txt`](extracted_strings.txt)

---

## 📋 待完成的工作

### 🚧 需要国际化的文件（按优先级）

#### 高优先级（用户最常见）

1. **Onboarding 相关** (未完成部分)
   - `OnboardingLLMSelectionView.swift` - LLM 提供商选择
   - `LLMProviderSetupView.swift` - API 密钥设置
   - `ScreenRecordingPermissionView.swift` - 权限请求
   - `HowItWorksView.swift` - 产品说明

2. **Settings 页面**
   - `SettingsView.swift` - 设置主界面（约 100+ 字符串）
   - 包括：Storage、Providers、Other 三个标签页

3. **Timeline/MainView**
   - `MainView/ActivityCard.swift` - 活动卡片
   - `MainView/Layout.swift` - 主视图布局
   - `MainView/Support.swift` - 支持信息
   - `TimelineReviewOverlay.swift` - 审核界面

#### 中优先级

4. **Dashboard**
   - `DashboardView.swift` - 仪表板

5. **Journal**
   - `JournalView.swift` - 日志主视图
   - `JournalDayView.swift` - 日记详情
   - `JournalReminders.swift` - 提醒设置

6. **Components**
   - `CategoryPickerView.swift` - 分类选择器
   - `DistractionSummaryCard.swift` - 分心摘要卡
   - `LongestFocusCard.swift` - 最长专注卡
   - `DaySummaryView.swift` - 日摘要

#### 低优先级

7. **错误与提示消息**
   - `TimelineFeedbackModal.swift` - 反馈模态框
   - `BugReportView.swift` - 错误报告
   - 各种 Alert 和 Toast 消息

8. **其他**
   - `WhatsNewView.swift` - 新功能介绍
   - `VideoPlayerModal.swift` - 视频播放器

---

## 🔧 如何继续国际化

### 方法 1: 手动逐文件替换（推荐用于关键文件）

```swift
// ❌ 替换前
Text("Select an activity to view details")

// ✅ 替换后
Text("timeline_select_activity")
```

**步骤**:
1. 在 `Localizable.xcstrings` 中添加新的 key
2. 在 Swift 文件中替换硬编码字符串为 key
3. 测试确保显示正确

### 方法 2: 使用 Xcode 自动提取（部分工作）

1. 在 Xcode 中打开项目
2. **Product** → **Export Localizations...**
3. 选择导出语言（en, zh-Hans）
4. Xcode 会自动扫描 `Text("...")` 并提取到 .xcloc 文件
5. 翻译后重新导入：**Product** → **Import Localizations...**

> ⚠️ 注意：自动提取可能不完整，建议结合手动检查。

### 方法 3: 批量脚本替换

使用 Python 脚本批量替换（需谨慎测试）：

```python
# 示例：批量替换 Settings 页面字符串
import re

def add_to_xcstrings(key, en, zh):
    # 添加到 Localizable.xcstrings
    pass

def replace_in_file(file_path, old, new):
    # 替换文件中的字符串
    pass
```

---

## 📝 xcstrings 文件扩展指南

### 添加新字符串

在 `Localizable.xcstrings` 中添加：

```json
{
  "settings_storage_subtitle": {
    "extractionState": "manual",
    "localizations": {
      "en": {
        "stringUnit": {
          "state": "translated",
          "value": "Recording status and disk usage"
        }
      },
      "zh-Hans": {
        "stringUnit": {
          "state": "translated",
          "value": "录制状态和磁盘使用"
        }
      }
    }
  }
}
```

### 使用 Plural (复数形式)

对于需要复数的字符串（如 "1 card" vs "5 cards"）：

```json
{
  "cards_count": {
    "extractionState": "manual",
    "localizations": {
      "en": {
        "variations": {
          "plural": {
            "one": {
              "stringUnit": {
                "state": "translated",
                "value": "%lld card"
              }
            },
            "other": {
              "stringUnit": {
                "state": "translated",
                "value": "%lld cards"
              }
            }
          }
        }
      },
      "zh-Hans": {
        "stringUnit": {
          "state": "translated",
          "value": "%lld 张卡片"
        }
      }
    }
  }
}
```

在代码中使用：
```swift
Text("cards_count", count: cardCount)
```

---

## 🚨 需要人工检查的术语列表

### 产品与技术术语

| 英文 | 当前中文翻译 | 备注 |
|------|--------------|------|
| **Dayflow** | Dayflow | ✅ 保持英文（产品名） |
| **Timeline** | 时间轴 | ⚠️ 或"时光轴"？ |
| **Activity Card** | 活动卡片 | ✅ |
| **Dashboard** | 仪表板 | ⚠️ 或"概览"、"总览"？ |
| **Journal** | 日志 | ⚠️ 或"日记"？需确认语境 |
| **Gemini** | Gemini | ✅ 保持英文（Google产品名） |
| **LLM** | LLM | ⚠️ 是否译为"大语言模型"？ |
| **Provider** | 提供商 | ✅ |
| **API key** | API 密钥 | ✅ |
| **Screen Recording** | 屏幕录制 | ✅ |
| **Distraction** | 分心 | ⚠️ 或"干扰"？ |
| **Focus** | 专注 | ✅ |

### 长文案（需人工润色）

1. **引导流程欢迎语**:
   ```
   EN: "Welcome to Dayflow! Let it run for about 30 minutes to gather
        enough data, then come back to explore your personalized timeline..."

   ZH: "欢迎来到 Dayflow！让它运行约 30 分钟以收集足够的数据，
        然后回来探索你的个性化时间轴..."
   ```
   ⚠️ 语气是否合适？是否过于直译？

2. **隐私说明**:
   ```
   EN: "Your privacy is guaranteed: All recordings stay on your Mac.
        With local AI models, even processing happens on-device..."

   ZH: "你的隐私得到保障：所有录制都保留在你的 Mac 上。
        使用本地 AI 模型，甚至处理也在设备上进行..."
   ```
   ⚠️ "得到保障"是否足够有力？

3. **功能描述**:
   ```
   EN: "Ask and track answers to any question about your day, such as
        'How many times did I check Twitter today?'..."

   ZH: "询问并追踪关于你一天的任何问题的答案，例如
        '今天我查看了多少次 Twitter？'..."
   ```
   ⚠️ 示例是否需要本地化（Twitter → 微博）？

### UI 术语一致性检查

| 上下文 | 英文 | 中文 | 一致性 |
|--------|------|------|--------|
| 按钮文字 | Start | 开始 | ✅ |
| 按钮文字 | Next | 下一步 | ✅ |
| 按钮文字 | Back | 返回 | ✅ |
| 菜单项 | Pause Dayflow | 暂停 Dayflow | ✅ |
| 菜单项 | Resume Dayflow | 恢复 Dayflow | ✅ |
| 菜单项 | Quit Completely | 完全退出 | ✅ |

---

## 📦 文件清单

生成的文件：
1. ✅ `Dayflow/Localizable.xcstrings` - String Catalog 主文件
2. ✅ `extracted_strings.txt` - 提取的所有字符串列表
3. ✅ `build_xcstrings.py` - 生成 xcstrings 的 Python 脚本
4. ✅ `extract_strings.py` - 提取字符串的 Python 脚本

修改的文件：
1. ✅ `Views/Onboarding/OnboardingFlow.swift`
2. ✅ `Menu/StatusMenuView.swift`

---

## 🎯 下一步行动计划

### 立即行动（第1周）

1. ✅ **审核已翻译的 63 个字符串**
   - 检查术语一致性
   - 调整语气和措辞
   - 确认产品名词翻译策略

2. 🚧 **继续国际化高优先级文件**
   - `SettingsView.swift`（最复杂，约 100+ 字符串）
   - `OnboardingLLMSelectionView.swift`
   - `ScreenRecordingPermissionView.swift`

3. 🚧 **添加复数形式支持**
   - 识别所有需要复数的字符串
   - 使用 String Catalog 的 plural 功能

### 中期目标（第2-3周）

4. 🔜 **国际化 Timeline 和 MainView**
5. 🔜 **国际化 Dashboard 和 Journal**
6. 🔜 **国际化 Components 和错误消息**

### 长期目标

7. 🔜 **在 Xcode 中配置项目**
   - 确保 Localizable.xcstrings 已添加到项目
   - 设置项目支持的语言（Project → Info → Localizations）
   - 测试语言切换

8. 🔜 **测试与验证**
   - 在系统语言为中文时测试所有界面
   - 检查文字是否溢出或截断
   - 确保日期、时间、数字格式正确

9. 🔜 **文档化**
   - 编写国际化贡献指南
   - 为新功能添加国际化检查清单

---

## 🛠️ 工具与资源

### 推荐工具

1. **Xcode String Catalog Editor**: 内置编辑器，可视化管理翻译
2. **genstrings** (命令行): `find . -name "*.swift" | xargs genstrings -o .`
3. **String Catalog Validator**: 检查缺失或重复的 key

### 参考资料

- [Apple: Localizing Your App](https://developer.apple.com/documentation/xcode/localizing-your-app)
- [String Catalogs 官方文档](https://developer.apple.com/documentation/xcode/localizing-strings-in-swift-code)
- [Best Practices for iOS Localization](https://developer.apple.com/videos/play/wwdc2021/10220/)

---

## 🏆 总结

### 进度统计

- ✅ **已完成**: 2 个文件，63 个字符串
- 🚧 **进行中**: 设置 xcstrings 基础架构
- 📝 **待完成**: ~53 个文件，~162 个字符串

### 预估工作量

- **高优先级文件**: 8-12 小时
- **中优先级文件**: 6-8 小时
- **低优先级文件**: 4-6 小时
- **测试与验证**: 4 小时
- **总计**: 约 **22-30 小时**

### 建议分工

1. **开发者**: 负责高优先级文件的代码替换
2. **翻译/产品经理**: 审核中文翻译，调整术语和语气
3. **QA**: 进行多语言测试，检查UI适配

---

## 联系与反馈

如有问题或建议，请联系项目维护者。

---

**报告生成时间**: 2026-01-20
**报告版本**: v1.0
