# Layout System

把「构图」从每次自由发挥升级成**编号模板**。`cover-brief.md` 的 `layout.template` 选择一张，模型不自行决定整体构图，只做内部填充。

`文章类型 (content.category)` → `Layout ID` → Prompt 里的 LAYOUT 段。

## 模板

| ID | 名称 | 占比 | 适合 |
|---|---|---|---|
| L01 | 人物主视觉 | 标题 45 · 人物 40 · 装饰 15 | 生活 / 观点 / 个人故事 |
| L02 | 产品陈列 | 标题 35 / 产品 45 / 人物 20 | 好物 / 收纳 / 数码 |
| L03 | 旅行地图 | 标题 35 / 路线 45 / 人物 20 | 旅行 / 攻略 |
| L04 | 三产品对比 | 标题 40 / 产品 45 / 人物 15 | 横评 / AI 工具对比 |
| L05 | 纯场景 | 标题 40 / 场景 60 / 人物 0 | 教程 / 学习方法 / 桌面改造 |

## 分类 → 模板映射

| content.category | template |
|---|---|
| product / goods / goods-list | L02 |
| comparison / ai-tools | L04 |
| travel / itinerary | L03 |
| personal / opinion / story | L01 |
| tutorial / learning / desk | L05 |

## LAYOUT 注入段（模板内）

```text
LAYOUT (template L02):
headline zone left 35%, product zone center 45% (use real supplied product images intact),
QIUQIU person right 20%, keep headline and products unobstructed.
```

选型后只输出对应模板的 LAYOUT 段，不叠加多条。

## 规则

- **不改整体模板**：人物 / 产品比来自模板，模型只能微调内部元素位置，不能改成另一套模板的比例。
- 同 category 始终同一模板 → 长期稳定，不会越跑越乱。
- 默认 `L02`（好物场景占比最高）；拿不准时选 L02。
- 生成后若出现 F05（构图拥挤 / 比例失衡），回模板查是不是选错 category。