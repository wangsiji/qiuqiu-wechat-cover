# Cover Brief

Cover Brief 是「文章 → Prompt」之间的结构化中间层，也是数据契约。Schema 定义字段、类型、枚举和格式；tools/validate_brief.py 在此基础上执行零依赖的业务规则与跨字段校验。

## 模板

```yaml
cover:
  ratio: 2.35:1
  size: 1880x800

content:
  category: product
  topic: "随身配饰"

copy:                        # Copy Lock —— 唯一文本真相源
  status: confirmed
  allowed_text:
    - "100件长期好物"
    - "戴了6年还在戴"

identity:
  enabled: true
  reference: references/assets/qiuqiu-face-reference.jpg
  mask: true

style:
  reference: references/assets/qiuqiu-style-reference.png
  pixel_ratio: 0.2

layout:
  template: L02

assets:
  - id: necklace
    input: image_3
    kind: real_product
    fidelity: 2

constraints:
  unauthorized_text: false
  invented_products: false
  invented_logos: false
```

## Copy Lock

唯一视觉文案真源是 copy.allowed_text。
- content 只描述文章事实：category + topic。
- 用户确认后把最终文案写进 copy.allowed_text，并设置 copy.status = confirmed。
- Compiler 只读取 copy.allowed_text，绝不从其他字段推导或改写视觉文案。

## 硬约束
- Brief 必须通过 tools/validate_brief.py，否则拒绝编译。
- copy.status 必须为 confirmed。
- copy.allowed_text 必须非空且不能重复。
- 每个 asset 必须有唯一 id 和唯一 input；input 采用 image_3、image_4… 的机器绑定格式。
- 正文依据缺失时标记「待确认」，不得靠猜。
