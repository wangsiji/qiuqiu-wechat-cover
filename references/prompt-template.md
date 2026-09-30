# 秋秋微信公众号封面提示词模板

复制后替换方括号内容。生成前先确认文章、文案和每张参考图的角色，并确认内置资产真的加载过（见 [workflow.md](workflow.md) 内置资产部分）。

```text
Create a 2.35:1 horizontal WeChat Official Account article cover for creator QIUQIU, recommended canvas 1880x800.

IMPORTANT INPUT CONTRACT:
- Image 1 and Image 2 are actual attached image inputs supplied by the Skill runtime.
- Do not infer them from filenames or textual descriptions.
- Do not invent, approximate, or generate a replacement QIUQIU face if Image 1 is not actually available.
- Stop instead when any required reference cannot be passed to the image tool.

ARTICLE: [用一句话说明正文主题和点击理由]
COPY (Chinese, reproduce character by character, no extra text):
- Hook: "[小钩子]"
- Main title: "[主标题]"
- Optional subtitle: "[补充说明；没有就删除这一行]"

REFERENCE ROLES:
- Image 1: QIUQIU identity only. Reproduce the EXACT same face as this reference (the approved cover face): same facial features, mask, black hair and hairstyle, skin tone, age impression. Do NOT restyle, beautify, change hairstyle or age. Do not copy its background, pose or text.
- Image 2: overall style only. Use its warm wood pixel-game workspace, palette, lighting, typography hierarchy and desk relationships. Do not copy its text, person, logo or specific product.
- Image 3+: real supplied product/logo/screenshot/travel photos. Use each as-is for [用途]; do not redraw, recolor, replace brand or invent objects.

STYLE: warm wooden study/workspace, retro pixel-game UI, bright cream window light, purple/pink/cream-yellow accents, cozy and lively, realistic person and real objects integrated with pixel atmosphere.
LAYOUT: headline on the left 55-65%; QIUQIU or clean space on the right 30-40%; real subject/product/route along the bottom. Keep headline, key number, person and product unobstructed.
TYPOGRAPHY: bold square pixel display type, main title largest, clear outline/shadow, Chinese characters exact.
NEGATIVE: no unauthorized words, no invented logos/products, no cartoon or doll-like face, no fully pixel person, no dark cyber-tech mood, no unrelated decorations, no aspect-ratio change.
```

## 多产品

把真实 Logo 或文字名牌放在标题下方横排；每个产品最多一句短标签。空间不足时先删标签，再删补充说明，不缩小主标题。

## 旅行

把真实旅行照作为路线节点或 Polaroid 组图；只有文章或图片确认的地点/年份/路线才能出现。

## 生成后

逐字检查中文。若比例、中文、真实素材或身份特征不符合，保留文案和参考图角色，只针对失败项重跑；重跑仍失败则保留说明。

