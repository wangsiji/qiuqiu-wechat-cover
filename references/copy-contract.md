# Copy Contract

封面文字是核心资产，错一字毁一篇。`Copy Lock` 在生成前把**允许出现的所有文字**固化成白名单，Prompt 编译时注入。

## Allowed Text（白名单）

文案在**用户确认**后锁进 `references/cover-brief.md` 的 `copy.allowed_text`（**唯一真相源**；`content.*` 只是给人读的摘要，不参与文字注入）。Compiler 只读它：

```json
{
  "hook": "100件长期好物",
  "title": "戴了6年还在戴",
  "subtitle": "",
  "allowed_text": ["100件长期好物", "戴了6年还在戴"]
}
```

Prompt 里的硬段：

```text
ALLOWED TEXT ONLY
The image may contain ONLY these Chinese strings:
「100件长期好物」
「戴了6年还在戴」
No other Chinese characters. No English. No decorative text.
No fake labels. No UI text. No signs. No packaging text.
```

## 为什么必须白名单

只写 `no unauthorized text` 不够——模型仍会在像素 UI、产品包装、书架标签、电脑屏幕里**偷偷生成**文字。白名单把「允许出现什么」显式约束住，比否定句强得多。

## 规则

- `allowed_text` 只含**确认过的文案**；`待确认` 项不得进白名单。
- 主标题是唯一视觉焦点，整页约 20~35 汉字。
- 生成后逐字核对白名单内文字；出现白名单外的汉字 → 判 F02（中文错字 / 多余文字）。
- 数字（如时间、价格）若在正文确认，可单独加进 `allowed_text`，但要逐字核对。