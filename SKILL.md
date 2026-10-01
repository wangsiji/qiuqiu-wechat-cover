---
name: qiuqiu-wechat-cover
description: >
  为「秋秋」制作微信公众号文章封面：先读取文章，提炼一个可点击的主题钩子，
  再用内置的暖木色复古像素工作台、内置真人秋秋身份图和用户提供的真实素材，
  生成 2.35:1 横版封面。
  适用于好物分享、AI 工具测评、旅行、学习效率、数码体验和桌面改造；不适用于泛用海报或脱离正文的装饰图。
---

# 秋秋微信公众号封面

这是一套可复用的品牌封面工作流。每次只替换文章主题、封面文案和真实主体，保持固定的视觉识别。

## 首次使用：先完成一次初始化

新用户第一次使用本 Skill 时，**不要直接进入文章分析**。先确认两件事：

1. **人物身份**：使用 Skill 内置的默认「秋秋」人物，还是替换成用户自己的真人身份图。
2. **图片生成后端**：是否使用 Lovart.ai；如果使用，当前运行环境是否已经配置 Lovart 密钥。

推荐运行：

```bash
python3 tools/init.py
```

初始化只保存非敏感配置到 `~/.qiuqiu-wechat-cover/config.json`。Lovart 密钥**永远不写入该文件、仓库或日志**，只从环境变量读取：

```bash
export LOVART_ACCESS_KEY="ak_..."
export LOVART_SECRET_KEY="sk_..."
```

自定义人物可直接运行：

```bash
python3 tools/init.py --identity custom --identity-path /path/to/identity.jpg --lovart yes
```

暂不配置 Lovart：

```bash
python3 tools/init.py --identity default --lovart no
```

初始化完成后，不再重复询问；只有用户明确要求替换人物或重新配置生成后端时才重新运行。

## 工作流

按 [references/workflow.md](references/workflow.md) 执行以下阶段。核心是把每次任务的判断先落成 **Cover Brief**（结构化中间层，见 [references/cover-brief.md](references/cover-brief.md)），再编译成提示词——换后端/换模型时品牌逻辑不重写：

1. **初始化（仅首次）**：确认人物身份与 Lovart 配置；未初始化先暂停。\n2. **收集**：先要完整文章（正文、Markdown 内容或可读取的本地路径），再确认需要的图片。
3. **分析**：从正文提取主题、点击理由、一个核心数字/结果/冲突，以及必须真实呈现的对象，产出 Cover Brief（`content.*`、`copy.allowed_text`、`layout.template` 与 `assets.*`）。用 `python3 tools/validate_brief.py <brief.json>` 校验契约（Copy Lock 必须 `confirmed`、fidelity 0–3、layout 合法）。
4. **提案**：给出 3 个短钩子和 1 个构图建议；用户确认后才把最终文案锁进 `copy.allowed_text`（`copy.status = confirmed`）；用户未确认文案时不生成图片。
5. **编译与生成**：`python3 tools/compile_prompt.py <brief.json> -o prompt.txt` 编译出提示词（Copy Lock 只读 `copy.allowed_text`）；调用 Lovart 前先 `resolve_assets.py` 加载内置资产；用户明确说“生成/跑图”才调用图像工具；局部修改遵守最小变更。
6. **验收**：`python3 tools/validate_output.py <out.png>` 过机器项（存在/可解码/尺寸/比例 F09），再加人工验收（比例、中文文字、人物身份、真实素材、明度和正文一致性），报告不确定项。

文章路径不可读取、正文不完整或关键事实缺失时，暂停在当前阶段并标记「待确认」，不要凭标题或常识补写。

## 内置品牌资产协议

本 Skill 自带一个固定风格资产；身份图由首次初始化选择。默认身份资产属于 Skill 自身，不是每次任务需要用户重复提供的输入：

- `references/assets/qiuqiu-face-reference.jpg`，角色：图 1（身份），用途：秋秋真人身份参考（当前为其一版经确认的封面裁切人脸，生成/编辑时必须保持不变——不得换脸、美颜、改年龄或改发型）
- `references/assets/qiuqiu-style-reference.png`，角色：图 2（风格），用途：公众号封面整体视觉风格参考

### 生成前必须真实加载

调用任何图像生成或编辑工具前，先验证这两个文件真实存在、可读取且文件头正确：

```bash
python3 tools/resolve_assets.py
```

必须得到 `ok: true` 和两个资产的 `absolute_path`。若当前运行时不能直接把本地路径作为图片输入，可加 `--data-uri` 得到可传递的 data URI。

**在 Prompt 里写文件名、相对路径或“参考图 1”，不等于图像模型真的看到了图。** 只有图片以当前工具支持的 image attachment / file reference / image bytes / data URI 等真实输入传给模型，才可认定“已使用参考图”。

### Fail-closed

如果身份图或风格图无法真实传入图像工具，则：

1. 不继续生成带人物版本封面，直接停止。
2. 不得让模型凭文字描述编一个“像秋秋”的女生。
3. 不得搜索互联网、用户历史对话、历史生成图或个人素材库找替代真人图。
4. 不得要求用户重新上传本 Skill 已内置且本地可读取的品牌资产。
5. 先依次尝试相对路径、绝对路径、file 引用、bytes、data URI；全部失败后报告“当前运行时不支持把 Skill 内置图片传给图像工具”，标记「待确认」。

## 输入角色

| 输入 | 来源 | 用途 | 约束 |
| --- | --- | --- | --- |
| 完整文章 | 用户 | 主题和事实依据 | 正文优先于标题和猜测 |
| 身份图（图 1） | 内置 | 秋秋真人身份 | 只参考脸、黑发、口罩、发型、肤色、年龄感；不复制背景、姿势、文字 |
| 风格图（图 2） | 内置 | 品牌视觉风格 | 只参考暖木像素、配色、光线、标题层级和桌面模型；不复制其文案、人物、Logo、电脑或具体产品 |
| 新参考图（图 3+） | 用户按需 | 产品、Logo、截图、旅行照、旧封面 | 在提示词里写明用途；真实图就原位用，不重绘不换色不换牌 |
| 文章 | 用户 | 主题和事实依据 | 正文优先于标题、历史提示词和模型预测 |

**新图不会自动覆盖默认资产。** 只有用户明确说“这张图作为秋秋真人参考 / 替换默认身份图”，才替换 图 1；只有用户明确说“用这张做默认风格”，才替换 图 2。其余新图一律从图 3+ 开始编号，用作当前文章的真实主体素材。没有真人图时不虚构秋秋；没有产品/Logo 图时用文字名或留出干净区域。

## 不可变的品牌约束

- 画布严格 **2.35:1**，优先 1880×800；除非用户明确要其他平台版本，不改比例。
- 视觉是**暖木色 × 复古像素游戏 × 温馨工作台 × 真实主体**，整体明亮温暖，避免暗色科技风。
- 构图按文章类型选 [references/layout-system.md](references/layout-system.md) 的编号模板（L01-L05），人物和道具不得遮挡标题、关键数字、产品或 Logo。
- 文字最多 3 组（小钩子、主标题、可选补充），整张约 20～35 个汉字；主标题是唯一视觉焦点，不塞功能清单。
- 有真人照片时保持约 80% 真实感 + 20% 像素融合，不得换脸、娃娃脸、过度美颜、彻底像素化；**默认保留口罩**，只有用户明确才能摘掉。
- 真实的产品、Logo、旅行照优先原样使用；未提供的未确认事实不得编造。**人物身份**约束见 [references/identity-contract.md](references/identity-contract.md)；**素材保护等级**（产品=2 / Logo=3，见 `assets[].fidelity`）见 [references/asset-contract.md](references/asset-contract.md)。文字只允许确认过的白名单，见 [references/copy-contract.md](references/copy-contract.md) 的 Copy Lock。

详细的视觉参数见 [references/style-guide.md](references/style-guide.md)，Cover Brief 编译成提示词见 [references/prompt-template.md](references/prompt-template.md)，验收与失败分类见 [references/prompt-checklist.md](references/prompt-checklist.md)。

## 新封面与编辑模式

- **新封面**：先完成文章分析和文案确认，再检查一遍内置资产生成（`python3 tools/resolve_assets.py`），然后生成。
- **编辑已有封面**：只改用户指定部分（删一句话、换 Logo、调脸等），保留其余布局、背景、产品和文字；删除区域用周围背景补齐。
- 只处理当前任务相关部分；生成图片一律保存到项目目录之外，不把图片写入或提交到仓库。

## 外部检索禁令

本 Skill 的品牌身份与风格必须来自仓库内置资产，以保证可移植、可复现和隐私独立。执行过程中不得：

- 搜索网页 / 图片引擎 / 用户历史对话找替代真人图
- 从个人素材库或历史生成图找身份参考
- 使用社交媒体头像或陌生人物图替换默认身份

除非用户明确要求外部检索，否则本 Skill 不为品牌身份或风格调用互联网检索。

## 输出协议

- 收集阶段：缺什么问什么。
- 提案阶段：`主题判断`、`3 个钩子`、`推荐构图`、`待确认素材`。
- 生成阶段：`最终文案`、`完整提示词`、`参考图角色`（含是否真正加载内置图）。
- 验收阶段：输出文件、实际尺寸/比例、通过项、待确认项和下一步建议。

生成前后使用 [references/prompt-checklist.md](references/prompt-checklist.md)。不要把“提示词已准备好”说成“图片已生成”，也不要把模型可能出错的中文当成已验证事实。

## Lovart 出图通道（默认执行后端）

本 Skill 的实际出图走 Lovart Agent API。Lovart 密钥只从 `LOVART_ACCESS_KEY` / `LOVART_SECRET_KEY` 环境变量读取，`tools/init.py` 不保存密钥。先用 `tools/compile_prompt.py` 把 Cover Brief 编译成提示词，内置参考图经 `tools/lovart-agent.py`（纯标准库、已随包分发）upload 成 CDN URL 后作为 `--attachments` 注入提示词生图。免费跑通键是 `set-mode --unlimited`（排队换额度，不扣积分）。完整命令、项目/线程、已知坑与验收见 [references/lovart-channel.md](references/lovart-channel.md)。执行顺序：`validate_brief.py` 校验 → `compile_prompt.py` 出提示词 → `resolve_assets.py` 验资产 → 内置两图 upload 拿 URL → `chat --project-id <从 projects --json 取>` → `validate_output.py` 机器验收。

