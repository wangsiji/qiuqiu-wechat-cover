# Asset Contract

真实素材（产品 / Logo / 旅行照 / 旧封面）的**保护等级**。与身份无关——它只负责「这张图能不能被重绘、换色、改品牌」。人物身份见 [identity-contract.md](identity-contract.md)。

## 保护等级（`assets[].fidelity`）

越小越可改：

| level | name | 允许改动 |
|---|---|---|
| 0 | decorative | 可重绘 |
| 1 | reference | 可近似 |
| 2 | real_subject | 禁重绘、禁换色、禁换品牌 |
| 3 | brand_asset | 禁重绘 / 禁换色 / 禁改 Logo |

**默认映射**：产品 / 旅行照 = 2；Logo / 品牌图标 = 3；纯装饰 = 0。

## 规则

- `assets[].fidelity` 必须是 **0–3 的整数**；超出 `validate_brief` 直接拒绝。
- 每张真实素材都必须在 Cover Brief 的 `assets[]` 里列出并给等级；缺失的素材用文字名 / 留白代替。
- **等级 2/3 的素材是权威的**：能在图上改的只有它的位置/大小，不能重绘细节、换颜色、换品牌或Logo绕改。

## 在 Prompt 注入

`tools/compile_prompt.py` 按每张素材的 `fidelity` 注入保护段；level 0 不注入：

```text
ASSET FIDELITY = LEVEL 3   # 由 compile 按 assets[].fidelity 填入
This asset is authoritative. Do not reinterpret, redraw, stylize,
recolor, simplify, replace or modify it.
```