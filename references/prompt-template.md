# 提示词编译器（Prompt Compiler）

把 `references/cover-brief.md` 编译成给图像后端的最终提示词。**本文件是「编译器规范」：`tools/compile_prompt.py` 是它的可执行实现**——`python3 tools/compile_prompt.py <brief.json> -o prompt.txt` 直接产出下方「编译产物」的逐段拼接，无需再手拼。手拼只用于没有脚本可用时的后备。

## 编译过程

```
cover-brief.json
  ├─ content.*   (+copy.allowed_text) → COPY + ALLOWED TEXT（copy-contract）
  ├─ identity.*     → REFERENCE ROLES + IDENTITY（identity-contract）
  ├─ style.*        → STYLE（style-guide）
  ├─ layout.template → LAYOUT（layout-system）
  ├─ assets[].fidelity → ASSET FIDELITY（asset-contract）
  └─ constraints.*  → NEGATIVE
          ↓
      Lovart prompt.txt
```

## 输入契约（Fail-closed，先于一切）

编译前必须满足；任一不满足就停，不生成：

```text
IMPORTANT INPUT CONTRACT:
- Image 1 and Image 2 are actual attached image inputs supplied by the Skill runtime.
- Do not infer them from filenames or textual descriptions.
- Do not invent, approximate, or generate a replacement QIUQIU face if Image 1 is not actually available.
- Stop instead when any required reference cannot be passed to the image tool.
```

## 编译产物（逐段拼接）

```text
Create a 2.35:1 horizontal WeChat Official Account article cover for creator QIUQIU, canvas 1880x800.

ARTICLE: [一句话正文主题 + 点击理由，有正文依据]

COPY (Chinese, exact, no extra) —— 仅来自 copy.allowed_text，不重复从 content.* 推导:
- 「allowed_text[0]」
- 「allowed_text[1]」

ALLOWED TEXT ONLY:
The image may contain ONLY these Chinese strings (copy.allowed_text):
「allowed_text[0]」
「allowed_text[1]」
No other Chinese characters. No English. No decorative text.
No fake labels. No UI text. No signs. No packaging text.

REFERENCE ROLES:
- Image 1 (Identity Layer): QIUQIU face only. Reproduce the EXACT same face (features, mask, hairstyle, skin, age). Do NOT restyle, beautify, slim, sharpen jaw, or age-shift. Ignore mask only if removal was confirmed.
- Image 2 (Brand Layer): style only (pixel UI, wood, palette, lighting, typography). Do not copy its text/person/logo/product.
- Image 3+ (Asset Layer): real supplied subjects. Use each as-is per its Asset Fidelity.

ASSET FIDELITY = LEVEL 3   # 每张真实素材按 fidelity 注入；Level 0 不注入
This asset is authoritative. Do not reinterpret, redraw, stylize, recolor, simplify, replace or modify it.

STYLE: [from references/style-guide.md 固定段]

LAYOUT: [from references/layout-system.md，按 content.category 选唯一模板]

TYPOGRAPHY: bold square pixel display type, main title largest, clear outline/shadow, Chinese exact.

NEGATIVE: [默认] no unauthorized, no invented products/logos, no dark cyber-tech, no cartoon/doll/celebrity face, no fully pixel person, no aspect-ratio change, keep 2.35:1.
```

## 使用注意

- **不直接写 "keep same face" 等模糊指令**，直接用上面的 Identity / Asset Fidelity 层表达。
- `ALLOWED TEXT` 里只放确认过的文案；漏了某词不留空位。
- 改稿（编辑已有封面）时在 `LAYOUT` 上方加：

```text
EDIT_SCOPE = TEXT_ONLY    # 或 PRODUCT_ONLY / PERSON_ONLY / BACKGROUND_ONLY
Preserve all unchanged regions as closely as the edit model allows.
```

失败重跑只替换对应段（见 references/prompt-checklist.md 的 Failure Codes），不要整段重写。