# Identity Contract

把「秋秋是谁」分成四个可独立稳定的层。**层的分离 = 换衣服不改脸、换风格不改身份。**

```
Identity  Layer  → 脸 / 黑发 / 口罩 / 年龄感          ← 只从 Image 1
Character Layer  → 衣着 / 姿势 / 表情 / 体态           ← 可随文章变
Brand     Layer  → 像素 UI / 暖木 / 光线 / 配色 / 排版 ← 只从 Image 2
Content   Layer  → 产品 / 旅行照 / 桌面 / 文章主题      ← 真实素材，图 3+
```

## Identity（只读，不可变）

以下特征一旦在生成时锁进 Brief，就**必须在整张图中保持一致**，不得漂移：

`face_shape / eye_shape / nose_shape / mouth_shape / hair_color / hairstyle / skin_tone / age_impression / mask`

**禁止（无论提示词怎么写都不得触发）：**

- beautification（美颜）
- face_slimming（削下颌 / 瘦脸）
- jaw_sharpening（下巴变尖）
- younger_appearance（变年轻 / 减龄）
- celebrity_like_face（网红脸 / 明星脸）
- anime_face / doll_face（动漫脸 / 娃娃脸）

**可变（可以随文章换）：** pose / clothing / expression / body_position / lighting / background。

## 生成前必读

- 与 `references/assets/qiuqiu-face-reference.jpg` 比对：脸型、五官、发色、肤色、年龄感一致才放行。
- **默认保留口罩**；只有用户明确说「摘口罩」才去掉。
- 身份漂移是评审时最常见的失败项（F01），一旦发现只修 identity 层，不动其他。

## Asset Fidelity

真实素材（产品 / Logo / 旅行照 / 旧封面）的**保护等级**已拆到 **[asset-contract.md](asset-contract.md)** 单独维护，不在这里。「秋秋是谁」才归本文件。