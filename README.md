# qiuqiu-wechat-cover

<p align="center"><strong>AI Agent Skill for WeChat Cover Design</strong></p>
<p align="center">从一篇文章，到一张可以直接发布的公众号封面。<br/>让 AI 不只是「生成图片」，而是理解内容、遵循品牌、保护素材，并持续迭代。</p>

<p align="center"><img src="examples/cover-japan-12days.png" alt="qiuqiu-wechat-cover" width="860"/></p>
<p align="center"><strong>Content → Creative Direction → Generation → Validation → Refinement</strong></p>

---

## 为什么做它

公众号封面真正难的，从来不是「画一张图」。

难的是让每一期都保持：

**统一的人物 · 稳定的视觉 · 准确的素材 · 清晰的标题 · 可持续的迭代**

普通的图片生成往往是一次性的：

> 写 Prompt → 生成 → 不满意 → 重写 Prompt → 再生成

qiuqiu-wechat-cover 把这件事变成了一套可以持续复用的 **Agent 工作流**。

它会把文章内容、品牌视觉、人物身份、真实素材和修改反馈组织起来，再交给图像模型执行。

---

## Selected Cases

<p align="center"><img src="examples/cover-case-01.jpg" alt="Cover case 01" width="49%"/> <img src="examples/cover-case-02.jpg" alt="Cover case 02" width="49%"/></p>
<p align="center"><img src="examples/cover-japan-12days.png" alt="Japan travel cover case" width="860"/></p>
<p align="center"><sub>同一套设计系统，可以覆盖好物、生活方式、旅行等不同内容。</sub></p>

---

## Core Capabilities

| 能力 | 解决的问题 |
| --- | --- |
| **Brand Consistency** | 固定人物、视觉风格与版式语言，避免每篇封面「长得不一样」 |
| **Content Understanding** | 从文章中提炼封面主题、标题与视觉重点 |
| **Asset Fidelity** | 保护人物、产品、Logo、截图等真实素材，不让 AI 随意重绘 |
| **Copy Lock** | 先确认封面文案，再进入生成阶段 |
| **Controlled Editing** | 修改时锁定无问题区域，尽量只修复指定问题 |
| **Visual QA** | 对比例、文字、人物、素材、构图与整体风格进行检查 |
| **Failure Patches** | 将常见失败沉淀成可复用的修正规则，而不是每次从零开始 |

---

## The Workflow

整个过程不是「一句 Prompt 生成一张图」，而是一条完整的内容生产链：

```
Article
   ↓
Content Analysis
   ↓
Cover Brief
   ↓
Copy Confirmation
   ↓
Visual Generation
   ↓
Visual QA
   ↓
Targeted Revision
   ↓
Final Cover
```

### 01 · Understand
AI 先理解文章，而不是直接画图。

- 内容主题
- 核心卖点
- 适合展示的元素
- 人物 / 产品 / 场景关系

### 02 · Define
将文章转化成结构化的 **Cover Brief**：文案、人物、素材、构图、风格、版式与输出比例。

### 03 · Generate
使用图像生成模型执行设计，同时遵循已经确定的视觉约束。

### 04 · Validate
生成之后继续检查人物身份、产品 / Logo、额外文字、构图与视觉风格。

### 05 · Refine
如果出现问题，不是「全部推倒重来」。例如：「人物保持不变，只修复产品变形。」Agent 会把修改限定在对应区域。

---

## For Users

### 安装之后，不需要学习任何设计知识

普通用户只需要和 Agent 对话。

第一次使用时，Agent 会通过对话完成初始化：

**① 选择封面人物**
- 使用内置人物
- 或上传自己的照片作为长期身份参考

**② 选择图片生成方式**
- 使用已配置的 Lovart
- 或暂时跳过，先完成内容分析与封面方案

初始化完成后，日常使用只需要一句话：

> **帮我给这篇公众号文章做一个封面。**

如果有真实素材，也一起提供：

> **这个产品必须保持原样。**

如果需要修改：

> **人物保持不变，标题再大一点。**

> **产品变形了，只修产品，其他不要动。**

就够了。

---

## Design System

项目默认内置一套完整的公众号封面视觉系统。

**Visual Direction**
- Warm wooden workspace
- Retro pixel-art aesthetic
- Bright & warm atmosphere
- Cozy lifestyle feeling

**Format**
- Ratio: **2.35 : 1**
- Recommended: **1880 × 800**

**Identity**
人物参考、脸型、五官、发型、年龄感与身份特征作为长期视觉资产管理。

**Real Assets**
产品、Logo、截图、旅行照片等真实素材优先保持原始外观，不让生成模型重新「设计」。

---

## Built for Iteration

真正有价值的不是「一次生成得很好」。

> **每一次使用，都让下一次更稳定。**

项目将失败类型、修改范围和验证结果结构化沉淀。

```
F01  人物身份偏移
F02  产品变形
F03  Logo 改写
F04  额外文字
F05  构图拥挤
...
```

一次修正，可以成为之后所有生成任务的规则。

这让 Skill 从一个 Prompt，逐渐变成一套可以长期复用的 **视觉生产系统**。

---

## Customization

它并不绑定「秋秋很开心」。

你可以替换自己的：
- 人物身份
- 风格参考
- Logo
- 产品素材
- 文案规则
- 构图规则
- 图片生成后端

因此，它既可以作为一个个人公众号工具，也可以作为一个品牌内容团队的封面生产 Skill。

---

## Architecture

如果你只是使用它，到这里就够了。

如果你希望了解内部实现：
- SKILL.md — Agent 执行规则
- references/ — 视觉、身份、文案、版式与失败规则
- tools/ — 初始化、Prompt 编译、Brief / Output 校验
- examples/ — 实际案例与示例 Brief

---

## Philosophy

> **不要让 AI 每次重新猜一遍你的品牌。**
>
> 把品牌、素材、规则和反馈变成 AI 可以长期遵循的系统。

qiuqiu-wechat-cover 的目标，不是让 AI 偶尔生成一张漂亮的图。

而是让：

**「写文章 → 做封面」**

变成一件稳定、可复用、可持续迭代的事情。

---

## License

MIT。

本项目中的 tools/lovart-agent.py 基于 [lovartai/lovart-skill](https://github.com/lovartai/lovart-skill)，具体归属见 [NOTICE](NOTICE)。

<p align="center"><sub>qiuqiu-wechat-cover · AI Agent Skill for WeChat Cover Design</sub></p>