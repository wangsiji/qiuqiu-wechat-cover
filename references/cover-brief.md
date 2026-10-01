# Cover Brief

`Cover Brief` 是「文章 → Prompt」之间的结构化中间层，也是**数据契约**（schema + validator 见 `tools/validate_brief.py` 与 `references/cover-brief.schema.json`）。一次任务先产出 Brief，再由 Prompt Compiler 编译成给图像后端的提示词。**改布局 / 换后端 / 换模型时只改 Brief 字段，品牌逻辑不重写。**

## 模板（建议存为 .json / .yaml，给 `tools/compile_prompt.py` 消费）

```yaml
cover:
  ratio: 2.35:1
  size: 1880x800

content:
  category: product          # 见 references/layout-system.md
  topic: "随身配饰"          # 文章主题一句话
  hook: "100件长期好物"
  title: "戴了6年还在戴"
  subtitle: ""

copy:                        # Copy Lock —— 唯一文本真相源
  status: locked             # locked | draft
  allowed_text:
    - "100件长期好物"
    - "戴了6年还在戴"

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
    fidelity: 2              # 见 references/asset-contract.md
  - id: bracelet
    kind: real_product
    fidelity: 2

constraints:
  unauthorized_text: false   # Copy Lock，见 references/copy-contract.md
  invented_products: false
  invented_logos: false
```

## Copy Lock：谁是文案唯一真相？

**真源是 `copy.allowed_text`。** Compiler 只读这张白名单，**绝不**再从 `content.hook / content.title` 推导文字。这样避免经过 review 确认 A → 后面 AI 又从正文推出 B → Prompt 偷偷变掉。

- 提案阶段：`content.hook_candidates` 候选，用户挑。
- 用户确认后：`copy.status = locked` 且把**最终确认的文案**写进 `copy.allowed_text`（含标题、钩子、补充）。`content.*` 只是**人读的摘要**，不参与文字注入。
- 生成前 `validate_brief.py` 强制：`status == locked` 且 `allowed_text` 非空。

## 字段填写规则

| 字段 | 谁填 | 依据 |
|---|---|---|
| `content.*` | LLM 分析 | 必须来自正文，标题/钩子/补充有据 |
| `copy.allowed_text` | 用户确认 | **唯一**注入 Prompt 的文案；不重复从 content 推导 |
| `identity.*` | 默认 | 内置资产；只当用户点名替换才改 `reference` |
| `style.*` | 默认 | 内置风格；只当用户点名才改 |
| `layout.template` | LLM | 按 `content.type` 映射（见 layout-system） |
| `assets.*` | 用户提供 | 每个真实素材必须列出，缺失则用文字名 / 留白 |
| `constraints.*` | 固定 | 默认全部 `false`（禁用未授权文字 / 虚构产品 / 虚构 Logo） |

## 硬约束

- Brief 必须通过 `tools/validate_brief.py`，否则拒绝编译。
- 任何正文依据缺失的字段 → 标记 `待确认`，不得靠猜。
- 生成后 Brief 与本次产物放一起存档（版本化）。

## 下一层

把这个 Brief（JSON / YAML）交给 `tools/compile_prompt.py` → 得到最终 prompt.txt → 调 Lovart → `validate_output.py` 机器验收 → PASS 再人工验 F01/F02 等。