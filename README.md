<p align="center">
  <img src="examples/cover-japan-12days.png" alt="qiuqiu-wechat-cover 示例封面" width="820"/>
</p>

<h1 align="center">qiuqiu-wechat-cover</h1>

<p align="center"><b>把一篇公众号文章，稳定地变成一张统一的品牌封面</b></p>
<p align="center">Article → Brief → Prompt → Generate → Validate → Retry</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href=".github/workflows/validate.yml"><img alt="CI" src="https://img.shields.io/badge/CI-GitHub%20Actions-brightgreen.svg"></a>
</p>

---

## ✨ 这是什么

**qiuqiu-wechat-cover** 是一个面向微信公众号封面制作的 Agent Skill。

它把「读文章 → 定文案 → 定人物 → 定素材 → 生成 → 验收 → 修正」整理成一套可重复执行的流程。

它的目标不是让 AI 偶尔生成一张好看的图，而是：

> **连续做几十篇、上百篇封面，仍然保持人物、风格、文案和真实素材的一致性。**

核心链路：

```text
公众号文章
   ↓
Cover Brief
   ↓
文案 / 人物 / 素材 / 构图锁定
   ↓
Prompt Compiler
   ↓
图像生成
   ↓
机器 + 人工 / 视觉验收
   ↓
PASS → 发布
FAIL → Failure Patch → Retry
```

---

## 🎯 适合谁

### 如果你只是想使用

你只需要：

1. 第一次运行初始化
2. 提供文章
3. 确认封面文案
4. 提供需要保真的人物 / 产品 / Logo / 照片
5. 让 Skill 完成生成与验收

**不需要先理解 JSON Schema、Prompt Compiler 或 F01～F10。**

### 如果你要二次开发

再去看：

- `SKILL.md`
- `references/`
- `tools/`
- `examples/`

---

# 🚀 5 分钟开始

## 1. 获取 Skill

```bash
git clone https://github.com/wangsiji/qiuqiu-wechat-cover.git
cd qiuqiu-wechat-cover
```

如果你的 Agent 有自己的 Skill 目录，把整个目录放进去即可。

例如：

```bash
cp -r . ~/.hermes/skills/qiuqiu-wechat-cover
```

---

## 2. 第一次使用：先初始化

第一次使用时运行：

```bash
python3 tools/init.py
```

初始化只需要回答两个问题。

### ① 人物身份

```text
1. 使用默认「秋秋」人物
2. 换成我自己的身份图
```

如果选择自定义，可以指定：

```bash
python3 tools/init.py \
  --identity custom \
  --identity-path /path/to/identity.jpg
```

默认人物素材：

```text
references/assets/qiuqiu-face-reference.jpg
```

默认风格参考：

```text
references/assets/qiuqiu-style-reference.png
```

### ② 是否使用 Lovart

```text
1. 配置 Lovart
2. 暂时跳过
```

也可以直接：

```bash
python3 tools/init.py --identity default --lovart yes
```

或者暂时不配置：

```bash
python3 tools/init.py --identity default --lovart no
```

查看当前初始化状态：

```bash
python3 tools/init.py --check
```

> **初始化只在首次使用时做。**
>
> 后续生成封面不需要反复询问人物和 API Key。

---

## 3. 配置 Lovart（可选）

如果你选择 Lovart，需要配置：

```bash
export LOVART_ACCESS_KEY="ak_..."
export LOVART_SECRET_KEY="sk_..."
```

然后检查：

```bash
python3 tools/init.py --check
```

### 🔐 安全规则

API Key：

- 只从环境变量读取
- 不写入 `config.json`
- 不写入 Git
- 不写入 Prompt
- 不写入日志

**不要把真实 Key 放进 README、Brief、代码或仓库。**

---

# 🧩 你真正需要准备什么

一次封面任务通常只需要四样东西：

### 1. 文章

最好提供完整正文，而不是只给标题。

### 2. 封面文案

Skill 会先提出候选文案，确认后才锁定。

最终画面允许出现的文字，只认：

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

### 3. 人物 / 真实素材

例如：

- 真人身份图
- 产品照片
- Logo
- 旅行照片
- App / 网页截图

真实素材不是普通「参考图」，而是需要保护的输入资产。

### 4. 文章主题

例如：

- 产品 / 好物
- 旅行
- AI
- 个人生活
- 教程
- 对比测评

Skill 会根据主题选择合适的构图模板。

---

# 🔄 完整工作流

## Step 1：读文章

先提炼：

- 文章真正主题
- 核心卖点 / 信息
- 最值得放到封面的内容
- 必须出现的真实对象
- 是否需要人物
- 是否需要产品 / Logo / 照片

**不确定的事实不猜。**

---

## Step 2：确定封面方案

先确定：

1. 封面主题
2. 短标题 / Hook
3. 构图方向
4. 需要哪些真实素材

用户确认文案后，进入 Copy Lock。

---

## Step 3：建立 Cover Brief

Cover Brief 是这次任务的**单一事实源**。

它统一记录：

- 画布
- 文章主题
- 最终文案
- 人物身份
- 风格
- 构图
- 真实素材
- 约束

因此后面的 Prompt、生成和验收都围绕同一份 Brief。

详细说明：

- [references/cover-brief.md](references/cover-brief.md)
- [references/cover-brief.schema.json](references/cover-brief.schema.json)

---

## Step 4：校验

```bash
python3 tools/validate_brief.py examples/sample-brief.json
```

不通过就不要进入生成阶段。

---

## Step 5：编译 Prompt

```bash
python3 tools/compile_prompt.py \
  examples/sample-brief.json \
  -o prompt.txt
```

Prompt 会按照固定结构生成：

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

---

## Step 6：检查真实素材

```bash
python3 tools/resolve_assets.py
```

这一步确保 Skill 知道：

> **哪些图片是真正要传给生成模型的输入，而不是只在 Prompt 里写一句“参考图”。**

---

## Step 7：生成

当前仓库提供 Lovart Agent 通道。

具体 Lovart 使用方式见：

- [references/lovart-channel.md](references/lovart-channel.md)

---

## Step 8：验收

先做机器检查：

```bash
python3 tools/validate_output.py path/to/generated.png
```

然后再进行视觉验收。

重点检查：

- 2.35:1 比例
- 中文是否逐字正确
- 人物身份是否一致
- 产品是否变形
- Logo 是否失真
- 真实照片是否被错误重绘
- 构图是否清晰
- 风格是否统一
- 是否准确表达文章主题

---

## Step 9：失败就分类修复

不要简单地「再生成一张」。

先判断问题属于哪一类：

| Code | 问题 |
|---|---|
| F01 | 人物身份漂移 |
| F02 | 中文错字 / 多余文字 |
| F03 | 产品变形 |
| F04 | Logo 失真 |
| F05 | 构图拥挤 / 比例失衡 |
| F06 | 主题不明确 |
| F07 | 画面过暗 |
| F08 | 未授权文字 |
| F09 | 比例错误 |
| F10 | 风格漂移 |

例如产品变形：

```bash
python3 tools/compile_prompt.py \
  examples/sample-brief.json \
  --failure F03 \
  -o retry.txt
```

Failure Patch 的原则是：

```text
保留原 Prompt
     +
只追加对应问题的修复指令
     ↓
重新生成
```

这样可以尽量避免「修了产品，又把人物修坏」。

完整规则：

- [references/failure-codes.md](references/failure-codes.md)
- [references/failure-codes.json](references/failure-codes.json)

---

# 🎨 当前品牌基线

当前内置示例以「秋秋很开心」的视觉体系为基准：

| 项目 | 基线 |
|---|---|
| 比例 | **2.35:1** |
| 推荐尺寸 | **1880×800** |
| 主视觉 | 暖木色 × 复古像素 × 温馨工作台 |
| 氛围 | 明亮、温暖、生活化 |
| 人物 | 保持身份连续，不随意换脸 |
| 产品 / Logo | 优先使用真实素材 |
| 文案 | 最多 3 组，以 Copy Lock 为准 |
| 构图 | L01～L05 |
| 禁止 | 换脸、美颜、虚构产品、虚构 Logo、未经确认的文字 |

具体规则不在 README 重复维护，统一放在：

- [references/identity-contract.md](references/identity-contract.md)
- [references/style-guide.md](references/style-guide.md)
- [references/layout-system.md](references/layout-system.md)
- [references/copy-contract.md](references/copy-contract.md)
- [references/asset-contract.md](references/asset-contract.md)

---

# 🛠️ 常用命令

### 初始化

```bash
python3 tools/init.py
```

### 查看初始化状态

```bash
python3 tools/init.py --check
```

### 检查 Skill

```bash
python3 tools/validate_skill.py .
```

### 检查 Brief

```bash
python3 tools/validate_brief.py examples/sample-brief.json
```

### 编译 Prompt

```bash
python3 tools/compile_prompt.py \
  examples/sample-brief.json \
  -o prompt.txt
```

### 生成失败后的定向修复

```bash
python3 tools/compile_prompt.py \
  examples/sample-brief.json \
  --failure F03 \
  -o retry.txt
```

### 检查内置素材

```bash
python3 tools/resolve_assets.py
```

### 检查生成图片

```bash
python3 tools/validate_output.py path/to/generated.png
```

---

# 🧪 测试

本地完整检查：

```bash
python3 tools/validate_skill.py .
python3 tools/validate_brief.py examples/sample-brief.json
python3 tools/compile_prompt.py examples/sample-brief.json -o /tmp/sample-prompt.txt
python3 tools/test_failure_patches.py
python3 tools/test_init.py
```

GitHub Actions 会自动验证：

- Skill 包结构
- Sample Brief
- Prompt 编译
- F01～F10 Failure Patch
- 首次初始化流程

CI：

- [.github/workflows/validate.yml](.github/workflows/validate.yml)

---

# 📁 项目结构

```text
qiuqiu-wechat-cover/
│
├── SKILL.md
├── README.md
├── LICENSE
├── NOTICE
│
├── agents/
│   └── openai.yaml
│
├── references/
│   ├── workflow.md
│   ├── cover-brief.md
│   ├── cover-brief.schema.json
│   ├── identity-contract.md
│   ├── asset-contract.md
│   ├── copy-contract.md
│   ├── layout-system.md
│   ├── style-guide.md
│   ├── prompt-template.md
│   ├── prompt-checklist.md
│   ├── failure-codes.md
│   ├── failure-codes.json
│   ├── lovart-channel.md
│   └── assets/
│       ├── qiuqiu-face-reference.jpg
│       └── qiuqiu-style-reference.png
│
├── tools/
│   ├── init.py
│   ├── test_init.py
│   ├── resolve_assets.py
│   ├── validate_skill.py
│   ├── validate_brief.py
│   ├── compile_prompt.py
│   ├── validate_output.py
│   ├── test_failure_patches.py
│   └── lovart-agent.py
│
├── examples/
│   ├── sample-brief.json
│   └── ai-agent-cover.md
│
└── .github/
    └── workflows/
        └── validate.yml
```

---

# 📚 从哪里开始看

### 只是使用

按这个顺序：

1. **README.md**
2. **SKILL.md**
3. **examples/sample-brief.json**

### 想修改视觉规则

看：

1. `references/identity-contract.md`
2. `references/style-guide.md`
3. `references/layout-system.md`
4. `references/copy-contract.md`
5. `references/asset-contract.md`

### 想修改执行逻辑

看：

1. `tools/validate_brief.py`
2. `tools/compile_prompt.py`
3. `tools/validate_output.py`
4. `tools/test_failure_patches.py`

### 想更换图片生成后端

保留：

```text
Cover Brief
    +
Brand Contracts
    +
Prompt Sections
```

只替换 / 新增后端 Adapter。

**不要把品牌规则重新写进生成后端。**

---

# ❓ FAQ

### 第一次使用一定要换人物吗？

不需要。

默认直接使用内置「秋秋」身份图；如果你做自己的账号，可以在初始化时选择自定义身份图。

### 每次生成都要输入人物图吗？

不需要重复配置。

首次初始化后，人物身份会作为默认配置。

### Lovart 是必须的吗？

不是。

Skill 的核心是 Brief、规则、Prompt 编译和验收体系。Lovart 是当前提供的图片生成通道之一。

### API Key 会不会被保存到仓库？

不会。

Lovart Key 只从环境变量读取。

### 为什么不直接写一个超长 Prompt？

因为单个 Prompt 很难稳定解决：

- 文案锁定
- 人物身份
- 真实素材保护
- 构图约束
- 失败后的局部修复
- 回归测试

所以这里把这些职责拆开：

```text
Brief
Copy Lock
Identity Contract
Asset Contract
Prompt Compiler
Failure Patch
Regression Test
```

### 为什么一定要先确认文案？

因为图片模型生成中文字符并不可靠。

这个 Skill 的策略是：

> **先锁定允许出现的文字，再验收最终图片。**

### 为什么真实产品要有 fidelity？

因为「参考一下产品」和「必须保持这个产品真实外观」是两种不同的任务。

fidelity 越高，对真实外观的保护要求越高。

---

# 📦 示例

- [examples/ai-agent-cover.md](examples/ai-agent-cover.md) — 完整案例
- [examples/sample-brief.json](examples/sample-brief.json) — 最小 Brief
- [examples/cover-japan-12days.png](examples/cover-japan-12days.png) — 实际封面示例

---

# 📄 License

MIT。

`tools/lovart-agent.py` 基于 [lovartai/lovart-skill](https://github.com/lovartai/lovart-skill)，具体归属见 [NOTICE](NOTICE)。

---

<p align="center">
  <sub>qiuqiu-wechat-cover · 从「会生成图片」走向「可持续生产封面」</sub>
</p>
