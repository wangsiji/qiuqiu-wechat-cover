# Failure Codes

`validate_output`（机器）或 人工验收 给封面判 PASS / FAIL，失败项统一编 F 码，**只修对应层**，不重写整张 prompt。`prompt-checklist.md` 的验收项对应到这里。

| Code | 失败 | 归因层 | 只修 |
|---|---|---|---|
| F01 | 人物身份漂移 | identity | Image 1 + 冻结特征 |
| F02 | 中文错字 / 多余文字 | copy | allowed_text 白名单 |
| F03 | 产品变形 | asset | fidelity 升到 2/3 |
| F04 | Logo 失真 | asset | fidelity 升到 3 |
| F05 | 构图拥挤 / 比例失衡 | layout | layout 模板 / category |
| F06 | 主题不明确 | content | content.category / topic |
| F07 | 画面过暗 | style | style-guide 光线段 |
| F08 | 未授权文字 | copy | NEGATIVE + allowed_text |
| F09 | 比例错误 | ratio | validate_output 拦截（机器判定）|
| F10 | 风格漂移 | style | style-guide 固定段 |

## 使用流程

```
生成 v1
  ↓
validate_output（机器项 F09 + 尺寸可读）
  ↓
人工验收（人脸 / 中文 / 构图）
  ↓
FAIL → 判 F##
  ↓ 只改 F## 对应层（compile 覆盖该段）
生成 v2（同 brief + 改动后的 prompt）
  ↓
回归检查（F01–F10 全过）→ FINAL
```

## 规则

- `tools/compile_prompt.py` 支持 `--failure F0X` 只覆盖对应段，其它段不变 → 真"定向补丁"，不是全重写。
- F02/F08 的一次根因在 `copy.allowed_text`；compile 只读 `copy.allowed_text`，不从 content 推导。
- 一个 F 码对应一层；多个 F 码同时出现时逐层分开修，别混进同一份 prompt。
