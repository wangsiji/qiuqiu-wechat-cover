# qiuqiu-wechat-cover

把公众号文章变成可发布封面的一套可复用工作流。AI 负责从「读文章 → 提钩子 → 出图 → 逐轮改」的完整链路，并收敛到一套统一的视觉身份：**暖木像素 × 温馨明亮 × 2.35:1 横版**。

**不绑定任何 Agent 平台。** 这是一个纯 Python 标准库的独立命令行工具集：只要你的智能体（Claude Code / Gemini CLI / Cursor / Hermes / 原生 LLM）能读文件、执行 `python3`、传图片给图像 API，就跑得动同一套流程。Agent 只是「搬运工+验收员」，数据和品牌逻辑沉淀在仓库里。

**一次配置，长期复用。** 人物、风格、文案与排版规则沉淀为长期约束，而不是每次重新表达。

---

## Examples

同一套方法，可以用于好物、生活方式、旅行等不同类型的公众号内容。

<p align="center">
  <img src="examples/cover-case-01.jpg" alt="好物封面案例" width="32%"/>
  <img src="examples/cover-case-02.jpg" alt="生活方式封面案例" width="32%"/>
  <img src="examples/cover-japan-12days.png" alt="日本十二日旅行封面" width="32%"/>
</p>

---

## Core Capabilities

- **文章理解** —— 从正文提炼主题、点击钩子与真实主体，而不是拿到就生成。
- **文案锁定（Copy Lock）** —— 生成前先确认封面标题，`copy.allowed_text` 是唯一文本真相源，杜绝「图对了、字不对、字被改」。
- **真实素材保护** —— 人物与产品图保持原样，不做不必要的重绘或变形；缺素材就 fail-closed，不编造。
- **统一视觉身份** —— 内置品牌资产（身份图 + 风格图 + 版式模板），也允许一键替换为自有品牌。
- **阶段校验** —— 每一步都有检查点（brief 校验、prompt 编译、输出机器验收、人工终检），而不是等最终出图兜底。
- **最小变更** —— 局部修改 / 修复（删除一句话、换 Logo、调脸）只动点名区域，不推翻重来。
- **多密钥兜底** —— 主 key 积分不足时自动按备用 key 依次重试、并自动切到免费队列（`--unlimited`），不因积分中断。

---

## Quick Start（框架无关，不用 Hermes）

> 首次使用会先跑一次**启动配置**，确认两个问题就完事，之后不再重复询问。

```bash
git clone https://github.com/wangsiji/qiuqiu-wechat-cover
cd qiuqiu-wechat-cover

# ① 配置图片生成后端（可选：不配也能先跑文案/校验部分）
export LOVART_ACCESS_KEY="ak_..."    # 主 key
export LOVART_SECRET_KEY="sk_..."
export LOVART_BACKUP_ACCESS_KEY="ak_..."   # 备用 key（可选，多把用 BACKUP2/3/4）
export LOVART_BACKUP_SECRET_KEY="sk_..."

# ② 首次初始化：确认「人物身份」与「是否用 Lovart」
python3 tools/init.py --identity default --lovart yes
```

之后，平时只需要一句话 + 文章：

> 帮我把这篇公众号文章做一张封面。

产品图、人物图、旅行照片可以顺手放进去；不传也没关系，会走「内置身份+文字」方案。

> **密钥纪律**：`LOVART_*` 只从环境变量读取，绝不写入 `config.json`、Git 或聊天记录。要临时给 agent 用，放进它的安全 Secret / env，而不是把 API Key 发到对话里。

---

## Production Pipeline

封面不是一步生成的，而是分阶段完成、每阶段可验收：

1. 读取文章，提取主题、点击钩子与真实主体
2. 产出结构化的 **Cover Brief**（标题、文案、版式、素材）
3. 与你确认文案，锁定到 `copy.allowed_text`
4. 编译成图像 Prompt，注入内置身份图 / 风格图与真实素材
5. 调用生成后端出图
6. 过机器校验（尺寸、比例、可解码）与人工验收（文字、人物、真实素材）

未通过就进入下一轮**只重跑未通过项**；已确认的文案与提示词不被重写。

---

## Architecture

把每次任务拆成可复用的层次：

| 层次 | 职责 |
| --- | --- |
| Agent 交互层 | 收集、确认、回报（你用什么 agent 都行） |
| Workflow 层 | 内容理解 → 提案 → 生成 → 验收 |
| 资产层 | 内置身份图 + 风格图 + 本次素材 |
| 生成层 | Lovart Agent Channel（默认） |
| 质检层 | Brief 校验、Prompt 编译、输出机器验收、人工终检 |

核心价值不在「出图」本身，而在于中间的 **Cover Brief**：内容 / 文案 / 版式 / 素材先结构化成一个可复用的中间产物，再交给生成层。想换生成后端 / 模型，不用重写品牌逻辑。

---

## 命令行入口（给不用 agent 或用别的 agent 的人）

只要你能执行这些脚本，就能独立驱动整条链路（全为 Python 标准库，零第三方依赖）：

```bash
# ① Cover Brief：先想清楚内容与文案
python3 tools/init.py --check                          # 状态探针（next_action 应=continue_workflow）
python3 tools/validate_brief.py my-brief.json          # 校验契约（必须通过）
python3 tools/compile_prompt.py my-brief.json -o prompt.txt   # 编译成图像 Prompt

# ② 生成：Lovart 通道（需要密钥）
python3 tools/lovart-agent.py set-mode --unlimited            # 免费队列（排队换额度）
python3 tools/lovart-agent.py upload --file references/assets/qiuqiu-face-reference.jpg
python3 tools/lovart-agent.py upload --file references/assets/qiuqiu-style-reference.png
python3 tools/lovart-agent.py chat \
  --project-id <从 projects --json 取> \
  --prompt "$(cat prompt.txt)" \
  --attachments URL1 URL2 \
  --download --output-dir out/

# ③ 验收
python3 tools/validate_output.py out/xxx.png --expect-ratio 2.35   # 尺寸/比例机器门禁
```

> 想用别的图后端？`resolve_assets.py` 可把内置图导出为 data URI 或绝对路径，喂给任意能收图片的 API（Stable Diffusion / Gemini / MiniMax…）。品牌数据固化在仓库，不绑定 Lovart。

---

## Project Structure

```text
.
├── SKILL.md                 # Skill 定义与触发规则
├── references/              # 领域规则
│   ├── agent-bootstrap.md   # 首次使用强制初始化
│   ├── workflow.md          # 工作流
│   ├── style-guide.md       # 视觉参数
│   ├── layout-system.md     # 版式模板
│   ├── identity-contract.md # 人物身份
│   ├── asset-contract.md    # 素材保护
│   ├── copy-contract.md     # 文案锁定
│   ├── prompt-template.md   # Prompt 模板
│   ├── prompt-checklist.md  # 验收清单
│   └── lovart-channel.md    # Lovart 出图通道（详细）
├── tools/                   # 实现（纯标准库）
│   ├── init.py              # 首次初始化
│   ├── resolve_assets.py    # 资产校验/导出
│   ├── validate_brief.py    # Cover Brief 校验
│   ├── compile_prompt.py    # Prompt 编译
│   ├── validate_output.py   # 输出校验
│   └── lovart-agent.py      # Lovart 出图（含多 key 兜底）
├── examples/                # 案例
└── agents/                  # Agent 配置
```

---

## Security

- Lovart API Key 只从环境变量读取，从不落盘、不写库、不回显。
- 自带的身份 / 风格素材是本 Skill 的隐私边界：不检索外部人物，不替换默认形象。
- 密钥进环境变量或用 Agent 的 Secret 管理，不要把 Key 直接发到对话。

---

## Development

```bash
python3 tools/validate_skill.py          # 完整性 + 链接 + 必需文件
python3 tools/test_agent_fallback.py     # 多 key 兜底回归
python3 tools/test_init.py               # 首次引导回归
```

CI 已把上面的都接线进 `.github/workflows/validate.yml`，每次 push 自动回归。

---

## Documentation

一套仓库，几层读者：

- **想直接用**：看上面的 **Quick Start**。
- **想了解内部**：`SKILL.md` → `references/workflow.md` → `references/style-guide.md`。
- **想扩展 / 换后端**：`tools/compile_prompt.py` + `references/prompt-template.md` 是起点,`references/lovart-channel.md` 是出图通道细节。

---

## License

本项目采用 MIT License。其中 `tools/lovart-agent.py` 基于 [lovartai/lovart-skill](https://github.com/lovartai/lovart-skill)，具体归属见 NOTICE。