# Cover Brief

`Cover Brief` 是「文章 → Prompt」之间的结构化中间层。一次任务先产出 Brief，再由 Prompt Compiler 把 Brief 编译成给图像后端的提示词。**改布局 / 换后端 / 换模型时只改 Brief 的字段，品牌逻辑不重写。**

## 模板

```yaml
cover:
  ratio: 2.35:1
  size: "1880x800"

content:
  category: product          # 见 references/layout-system.md
  topic: "随身配饰"          # 文章主题一句话
  hook: "100件长期好物"
  title: "戴了6年还在戴"
  subtitle: ""               # 可空

identity:
  enabled: true
  reference: references/assets/qiuqiu-face-reference.jpg
  mask: true                 # 默认 true；只有用户明确才 false

style:
  reference: references/assets/qiuqiu-style-reference.png
  pixel_ratio: 0.2

layout:
  template: L02              # 见 references/layout-system.md

assets:                      # 真实素材清单（图 3+）
  - id: necklace
    kind: real_product
    fidelity: 2              # 见 identity-contract.md 的 asset_fidelity
  - id: bracelet
    kind: real_product
    fidelity: 2

constraints:
  unauthorized_text: false   # Copy Lock，见 references/copy-contract.md
  invented_products: false
  invented_logos: false
```

## 字段填写规则

| 字段 | 谁填 | 依据 |
|---|---|---|
| `content.*` | LLM 分析 | 必须来自正文，标题/钩子/补充有据 |
| `identity.*` | 默认 | 内置资产；只当用户点名替换才改 `reference` |
| `style.*` | 默认 | 内置风格；只当用户点名才改 |
| `layout.template` | LLM | 按 `content.category` 映射（见 layout-system） |
| `assets.*` | 用户提供 | 每个真实素材必须列出，缺失则用文字名 / 留白 |
| `constraints.*` | 固定 | 默认全部 `false`（=禁用未授权文字 / 虚构产品 / 虚构 Logo） |

## 硬约束

- **Brief 里没有 `allowed_text` 为什么？** 因为文案可能在确认阶段调整。每个字段在生成前都必须锁定。Copy Lock 只在 Prompt 编译阶段写入。
- 任何字段缺正文依据 → 标记 `待确认`，不得靠猜。
- 生成后 Brief 与本次产物放一起存档（版本化）。

下一步怎么用：把这个 YAML 交给 `references/prompt-template.md` 的编译器，得到最终提示词再调 Lovart。