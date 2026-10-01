# Failure Codes

`validate_output`（机器）或人工验收给封面判 PASS / FAIL，失败项统一编 F 码，**只向对应 section 注入定向补丁**，不重写其他层。

| Code | 失败 | 归因层 | 只修 |
|---|---|---|---|
| F01 | 人物身份漂移 | identity | Image 1 + 冻结特征 |
| F02 | 中文错字 / 多余文字 | copy | allowed_text 白名单 |
| F03 | 产品变形 | asset | fidelity / 资产保护 |
| F04 | Logo 失真 | asset | fidelity / 资产保护 |
| F05 | 构图拥挤 / 比例失衡 | layout | layout 模板 |
| F06 | 主题不明确 | content | article topic |
| F07 | 画面过暗 | style | style 光线段 |
| F08 | 未授权文字 | copy | allowed_text + negative |
| F09 | 比例错误 | ratio | validate_output |
| F10 | 风格漂移 | style | 固定品牌 style |

## Patch 语义

`tools/compile_prompt.py --failure F0X` 保留原 section 的全部内容，然后在该 section 末尾追加 failure-specific instruction。
因此 Brief → Prompt → Failure Patch 仍然可追溯；F03 不会丢掉 image_3 / image_4 / fidelity，F02 不会丢掉真实的文案白名单。

## 使用流程
```
生成 v1 → validate_output → 人工验收 → FAIL F## → 只向对应 section 追加 patch → 生成 v2 → section regression → FINAL
```
