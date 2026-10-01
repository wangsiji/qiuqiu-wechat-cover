<p align="center">
  <img src="examples/cover-japan-12days.png" alt="qiuqiu-wechat-cover 示例封面" width="820"/>
</p>

<h1 align="center">qiuqiu-wechat-cover</h1>

<p align="center"><b>把一篇公众号文章，稳定地变成一张统一的品牌封面</b></p>
<p align="center">文章 → Cover Brief → Prompt → 生成 → 验收 → Failure Patch → Retry</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href=".github/workflows/validate.yml"><img alt="CI" src="https://img.shields.io/badge/CI-GitHub%20Actions-brightgreen.svg"></a>
</p>

---

## 这是什么

qiuqiu-wechat-cover 是一个面向「秋秋很开心」公众号的 **Agent Skill + Prompt Compiler + Cover Brief 数据契约 + 验收系统**。

它解决的不是“让 AI 随便生成一张好看的图”，而是：

> **同一个账号，连续做几十篇、上百篇文章后，封面依然像同一个品牌。**

核心思路是把原本依赖模型发挥的封面制作过程，拆成一条可验证的执行链：

```text
文章
  ↓
文章事实 / 主题提炼
  ↓
Cover Brief
  ↓
validate_brief
  ↓
Prompt Compiler
  ↓
图像生成后端
  ↓
validate_output
  ↓
人工 / 视觉验收
  ↓
PASS ─────────────→ FINAL
  ↑
  └── FAIL → F01~F10 → Failure Patch → Retry
```

最重要的不是某一段 Prompt，而是 **中间层数据契约 + 单一真相源 + 定向修复 + 回归测试**。

## 你可以用它做什么

- 从真实公众号文章提炼封面主题。
- 在生成前锁定最终中文文案。
- 固定人物身份与品牌视觉。
- 让产品、Logo、旅行照片等真实素材按保护等级使用。
- 用 Cover Brief 把文章事实、文案、素材、构图结构化。
- 用 Prompt Compiler 将 Brief 编译成可执行 Prompt。
- 生成失败后，只针对对应问题注入 F01～F10 Patch，而不是推翻整张图。
- 用机器校验检查文件、格式、尺寸和 2.35:1 比例。
- 用 GitHub Actions 对 Skill 结构、Brief、Prompt Compiler 和 Failure Patch 做回归测试。

---

## 核心设计原则

### 1. Brief 是中间层

不要让“文章 → Prompt”直接发生。

先把任务写成结构化 Brief：

```text
Article
  ↓
Cover Brief
  ↓
Prompt
```

这样换模型、换生成后端、调整视觉规则时，不需要重新设计整个工作流。

核心文件：

- [references/cover-brief.md](references/cover-brief.md)
- [references/cover-brief.schema.json](references/cover-brief.schema.json)
- [tools/validate_brief.py](tools/validate_brief.py)

### 2. Copy Lock 是唯一文案真相源

封面最终允许出现哪些文字，只认：

```json
{
  "copy": {
    "status": "confirmed",
    "allowed_text": [
      "100件长期好物",
      "戴了6年还在戴"
    ]
  }
}
```

content 负责描述文章事实，copy.allowed_text 负责描述**画面允许出现的文字**。

因此：

> 没确认文案，不生成；生成后出现白名单之外的文字，判 FAIL。

详见 [references/copy-contract.md](references/copy-contract.md)。

### 3. 真实素材优先

产品、Logo、旅行照片等不是“灵感参考”，而是**受保护的输入资产**。

每个资产绑定一个机器可识别的 input：

```json
{
  "id": "necklace",
  "input": "image_3",
  "kind": "real_product",
  "fidelity": 2
}
```

fidelity 越高，模型可修改的空间越小：

| 等级 | 含义 | 典型素材 |
|---|---|---|
| 0 | 可近似 / 可风格化 | 装饰元素 |
| 1 | 尽量保持 | 普通参考素材 |
| 2 | 权威真实素材 | 产品、真人主体、旅行照片、截图 |
| 3 | 严格不可改 | Logo、品牌资产 |

详见 [references/asset-contract.md](references/asset-contract.md)。

### 4. Failure Patch 是增量修复，不是重写

如果 F03 判断“产品变形”，正确做法不是重新编译一套完全不同的 Prompt。

而是：

```text
原始 asset_fidelity section
        +
F03 patch
        ↓
重新生成
```

原始的 image_3、image_4、fidelity 等信息必须保留。

当前 F01～F10 的归因与 Patch 定义见 [references/failure-codes.json](references/failure-codes.json)。

---

## 品牌基线

这是「秋秋很开心」当前封面的固定视觉基线。

| 项目 | 规则 |
|---|---|
| 画布 | **2.35:1**，优先 1880×800 |
| 主视觉 | 暖木色 × 复古像素 × 温馨工作台 |
| 氛围 | 明亮、温暖、生活化 |
| 人物 | 使用内置身份图，保持人物身份连续 |
| 真实主体 | 产品 / Logo / 旅行照片优先使用真实素材 |
| 文案 | 最多 3 组，最终以 Copy Lock 为准 |
| 构图 | 根据文章类型选择 L01～L05 |
| 风格融合 | 真人主体保持真实感，和像素环境融合 |
| 禁止 | 换脸、美颜、虚构产品、虚构 Logo、未经确认的文字 |

完整视觉规则不要在 README 重复维护，统一放在：

- [references/identity-contract.md](references/identity-contract.md)
- [references/style-guide.md](references/style-guide.md)
- [references/layout-system.md](references/layout-system.md)
- [references/copy-contract.md](references/copy-contract.md)
- [references/asset-contract.md](references/asset-contract.md)

README 负责告诉你**怎么用**；references 负责告诉系统**具体怎么执行**。

---

## 快速开始

### 1. 安装

```bash
git clone https://github.com/wangsiji/qiuqiu-wechat-cover.git
cd qiuqiu-wechat-cover
```

如果作为 Agent Skill 使用，以你的 Agent 所支持的 Skill 目录为准。例如 Hermes：

```bash
cp -r . ~/.hermes/skills/qiuqiu-wechat-cover
```

### 2. 检查 Skill 包

```bash
python3 tools/validate_skill.py .
```

检查内容包括必需文件、相对链接、内置资产和后端相关完整性。

### 3. 检查内置品牌资产

```bash
python3 tools/resolve_assets.py
```

必须确认输出包含 ok: true，并确认身份图、风格图都能被当前运行环境真实读取。

> 仅仅在 Prompt 里写“参考图 1 / 参考图 2”不代表模型真的收到了图片。生成前必须把图片作为当前图像工具支持的真实输入传入。

### 4. 准备 Cover Brief

可以直接从 [examples/sample-brief.json](examples/sample-brief.json) 开始。

最小结构：

```json
{
  "cover": {
    "ratio": "2.35:1",
    "size": "1880x800"
  },
  "content": {
    "category": "product",
    "topic": "随身配饰"
  },
  "copy": {
    "status": "confirmed",
    "allowed_text": [
      "100件长期好物",
      "戴了6年还在戴"
    ]
  },
  "identity": {
    "enabled": true,
    "reference": "references/assets/qiuqiu-face-reference.jpg",
    "mask": true
  },
  "style": {
    "reference": "references/assets/qiuqiu-style-reference.png",
    "pixel_ratio": 0.2
  },
  "layout": {
    "template": "L02"
  },
  "assets": [
    {
      "id": "necklace",
      "input": "image_3",
      "kind": "real_product",
      "fidelity": 2
    }
  ],
  "constraints": {
    "unauthorized_text": false,
    "invented_products": false,
    "invented_logos": false
  }
}
```

### 5. 校验 Brief

```bash
python3 tools/validate_brief.py examples/sample-brief.json
```

重点检查：

- copy.status 是否为 confirmed
- copy.allowed_text 是否为空 / 重复
- layout.template 是否合法
- category → template 是否匹配
- asset id 是否唯一
- asset input 是否唯一
- input 是否符合 image_3、image_4… 格式
- fidelity 是否达到素材类型要求
- edit target 是否指向真实 asset

### 6. 编译 Prompt

```bash
python3 tools/compile_prompt.py \
  examples/sample-brief.json \
  -o prompt.txt
```

输出是一份按固定 section 组装的执行 Prompt：

```text
opener
article
copy
ref_roles
asset_fidelity
style
layout
typography
negative
edit
```

### 7. 失败后定向修复

例如产品变形：

```bash
python3 tools/compile_prompt.py \
  examples/sample-brief.json \
  --failure F03 \
  -o prompt-f03.txt
```

F03 只向 asset_fidelity section 注入修复指令，同时保留原有资产绑定和 fidelity 信息。

| Code | 问题 | Patch 归因 |
|---|---|---|
| F01 | 人物身份漂移 | ref_roles |
| F02 | 中文错字 / 多余文字 | copy |
| F03 | 产品变形 | asset_fidelity |
| F04 | Logo 失真 | asset_fidelity |
| F05 | 构图拥挤 / 比例失衡 | layout |
| F06 | 主题不明确 | article |
| F07 | 画面过暗 | style |
| F08 | 未授权文字 | copy |
| F09 | 比例错误 | opener |
| F10 | 风格漂移 | style |

完整定义见 [references/failure-codes.md](references/failure-codes.md)。

### 8. 机器验收

生成图片后：

```bash
python3 tools/validate_output.py path/to/generated.png
```

当前机器验收负责：

- 文件存在
- 文件非空
- PNG / JPEG 可识别
- 能读取尺寸
- 宽高比例接近 2.35:1

它**不会假装替代视觉判断**。

人物是否像、中文是否逐字正确、产品有没有变形、构图是否舒服，仍然需要人工或视觉模型验收。

---

## 完整生产工作流

### Step 1：读取文章

输入必须是完整正文，不能只凭标题猜。

提炼：

- 文章真正主题
- 用户为什么值得点击
- 一个核心数字 / 结果 / 冲突
- 必须真实呈现的对象
- 是否需要真人
- 是否需要产品 / Logo / 旅行照片

如果关键事实缺失：

> 停在当前阶段，标记「待确认」，不要猜。

### Step 2：提出封面方案

先输出：

1. 主题判断
2. 3 个短钩子
3. 推荐构图
4. 待确认素材

用户确认文案后，才写入：

```json
"copy": {
  "status": "confirmed",
  "allowed_text": [...]
}
```

### Step 3：建立 Brief

把最终决策写进 Cover Brief。

此时 Brief 成为：

> **这一次封面任务的单一事实源。**

### Step 4：校验

```bash
python3 tools/validate_brief.py <brief.json>
```

不通过，不生成。

### Step 5：编译

```bash
python3 tools/compile_prompt.py <brief.json> -o prompt.txt
```

### Step 6：真实加载参考图

```bash
python3 tools/resolve_assets.py
```

确认内置身份图和风格图真正作为图片输入进入生成后端。

### Step 7：生成

当前仓库提供 Lovart Agent 通道实现。

具体 API、项目 / thread、attachment 上传方式和已知限制见：

[references/lovart-channel.md](references/lovart-channel.md)

不要把“Prompt 已生成”描述成“图片已生成”。

### Step 8：验收

先机器验收：

```bash
python3 tools/validate_output.py <generated-image>
```

再进行视觉验收：

- 比例
- 中文文字
- 人物身份
- 产品 / Logo / 旅行照
- 构图层级
- 明度
- 风格一致性
- 与正文主题的一致性

### Step 9：失败就分类

不要一句“这张不太对”重新生成。

先判断：

```text
人物问题 → F01
文字问题 → F02 / F08
产品问题 → F03
Logo 问题 → F04
构图问题 → F05
主题问题 → F06
明度问题 → F07
比例问题 → F09
风格问题 → F10
```

然后：

```bash
python3 tools/compile_prompt.py <brief.json> --failure F03 -o retry.txt
```

这样可以最大限度保持其他已经正确的部分不变。

---

## Prompt Compiler

tools/compile_prompt.py 是整个执行层的关键。

它把 Brief 编译成固定 section：

```text
opener
article
copy
ref_roles
asset_fidelity
style
layout
typography
negative
edit
```

Failure Patch 不直接替换 section，而是：

```text
BASE SECTION
+
FAILURE PATCH
```

因此可以做 section-level regression test，避免“修产品把人物也修坏”的连锁污染。

---

## 测试与 CI

本地完整检查：

```bash
python3 tools/validate_skill.py .
python3 tools/validate_brief.py examples/sample-brief.json
python3 tools/compile_prompt.py examples/sample-brief.json -o /tmp/sample-prompt.txt
python3 tools/test_failure_patches.py
```

GitHub Actions 会自动执行核心验证链：

- Skill package validation
- Sample Cover Brief validation
- Prompt compilation smoke test
- F01～F10 Failure Patch section regression

Workflow：

[.github/workflows/validate.yml](.github/workflows/validate.yml)

Failure Patch regression：

[tools/test_failure_patches.py](tools/test_failure_patches.py)

---

## 项目结构

```text
qiuqiu-wechat-cover/
│
├── SKILL.md                         # Agent Skill 主入口
├── README.md                        # 项目使用入口
├── LICENSE
├── NOTICE
│
├── agents/
│   └── openai.yaml                  # Agent / UI 配置
│
├── references/
│   ├── workflow.md                  # 完整工作流协议
│   ├── cover-brief.md               # Cover Brief 数据契约
│   ├── cover-brief.schema.json      # JSON Schema
│   ├── identity-contract.md         # 人物身份约束
│   ├── asset-contract.md            # 素材保护等级
│   ├── copy-contract.md             # Copy Lock
│   ├── layout-system.md             # L01～L05 构图系统
│   ├── style-guide.md               # 品牌视觉规范
│   ├── prompt-template.md            # Prompt 规范
│   ├── prompt-checklist.md           # 验收清单
│   ├── failure-codes.md              # F01～F10 说明
│   ├── failure-codes.json            # Failure Patch 数据源
│   ├── lovart-channel.md             # Lovart 通道说明
│   └── assets/
│       ├── qiuqiu-face-reference.jpg
│       └── qiuqiu-style-reference.png
│
├── tools/
│   ├── resolve_assets.py             # 内置资产检查
│   ├── validate_brief.py             # Brief / 业务规则校验
│   ├── compile_prompt.py             # Brief → Prompt
│   ├── validate_output.py            # 生成图机器验收
│   ├── validate_skill.py             # Skill 包完整性校验
│   ├── test_failure_patches.py       # F01～F10 回归测试
│   └── lovart-agent.py               # Lovart Agent 通道
│
├── examples/
│   ├── sample-brief.json             # 最小可运行 Brief
│   └── ai-agent-cover.md             # 完整案例
│
└── .github/
    └── workflows/
        └── validate.yml              # CI
```

---

## References 怎么看

如果你只是**使用**这个 Skill：

1. SKILL.md
2. README.md
3. examples/sample-brief.json

如果你要**修改规则**：

1. references/cover-brief.md
2. references/copy-contract.md
3. references/asset-contract.md
4. references/layout-system.md
5. references/style-guide.md

如果你要**修改执行层**：

1. tools/validate_brief.py
2. tools/compile_prompt.py
3. tools/validate_output.py
4. tools/test_failure_patches.py

如果你要**换生成后端**：

1. 保留 Cover Brief
2. 保留品牌 contracts
3. 保留 Prompt Compiler 的 section 结构
4. 替换 / 新增 backend adapter
5. 不要把品牌逻辑重新写进后端代码

核心架构就是：

> **品牌逻辑与生成后端解耦。**

---

## 常见问题

### 为什么不直接写一个超长 Prompt？

因为长 Prompt 解决不了：

- 文案到底哪个是真的？
- 产品输入到底是哪张图？
- 修改产品时是否误伤人物？
- 失败后到底改了哪一层？
- 下一次生成能不能复现？
- 代码修改后有没有回归测试？

所以这里把这些问题分别交给：

```text
Brief
Copy Lock
Asset Contract
Failure Patch
Regression Test
```

### 为什么一定要先确认文案？

因为图片模型对中文字符的生成并不可靠。

这个 Skill 的策略不是“祈祷模型一次写对”，而是：

> **先锁白名单，再验收结果。**

### 为什么产品要有 fidelity？

因为“参考一下产品”和“原样使用这个产品”是两种完全不同的生成要求。

fidelity = 2 表示真实主体必须被保护，模型只能在构图层面调整位置 / 尺寸，而不是重新设计产品。

### 为什么失败后不能直接重新生成？

当然可以，但那样会把已经正确的部分一起重新随机化。

Failure Patch 的目的就是：

> **只修错的地方，尽量不动对的地方。**

### 为什么 README 不写所有视觉细节？

因为 README 是入口，不应该成为第二份规则库。

GitHub 官方建议 README 聚焦项目用途、快速开始和导航；更详细的长期文档应放到独立文档中。citeturn0search0turn0search8

因此这里采用：

```text
README
  ↓
告诉你怎么用
  ↓
references
  ↓
告诉系统具体规则
  ↓
tools
  ↓
真正执行
```

---

## 示例

- [examples/ai-agent-cover.md](examples/ai-agent-cover.md) — 从文章分析到封面生成的完整案例
- [examples/sample-brief.json](examples/sample-brief.json) — 最小 Cover Brief
- [examples/cover-japan-12days.png](examples/cover-japan-12days.png) — 2.35:1 实际封面示例

---

## 许可

[MIT](LICENSE)

tools/lovart-agent.py 基于 [lovartai/lovart-skill](https://github.com/lovartai/lovart-skill)，同样遵循 MIT；具体归属见 NOTICE。

---

<p align="center">
  <sub>qiuqiu-wechat-cover · 从「会生成图片」走向「可持续生产封面」</sub>
</p>
