# qiuqiu-wechat-cover

把公众号文章变成可发布封面的一套可复用工作流。AI 负责从内容理解到出图、再到逐轮修改的完整链路，并收敛到一套统一的视觉身份。

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
- **文案锁定** —— 生成前先确认封面标题，避免「图对了、字不对」。
- **真实素材保护** —— 人物与产品图保持原样，不做不必要的重绘或变形。
- **统一视觉身份** —— 内置「秋秋很开心」体系（暖木像素、温馨明亮、2.35:1），也允许替换为自有品牌。
- **阶段校验** —— 每个阶段都有明确检查点，边做边查，而不是等最终出图再兜底。
- **最小变更** —— 局部修改 / 修复只动点名区域，不推翻重来。

---

## First Run

通过支持 Agent Skill 的智能体加载本仓库即可。**第一次会先完成一次启动配置**，不会直接开始分析文章 —— 只确认下面两项，之后不再重复询问：

1. **长期人物身份**：使用内置的「秋秋」人物，或上传你自己的真人照片作为长期参考。
2. **图片生成后端**：是否使用 Lovart；如需使用，密钥放进 Agent 的安全 Secret / 环境变量即可，不需要把 API Key 发到聊天里。

装好后，平时只需要一句话 + 文章：

> 帮我把这篇公众号文章做一张封面。

产品图、人物图、旅行照片可以顺手放进去。

---

## Production Pipeline

封面不是一步生成的，而是分阶段完成、每阶段可验收：

1. 读取文章，提取主题、点击钩子与真实主体
2. 产出结构化的 **Cover Brief**（标题、文案、版式、素材）
3. 与你确认文案，锁定到 `copy.allowed_text`
4. 编译成图像 Prompt，注入内置身份图 / 风格图与真实素材
5. 调用生成后端出图
6. 过机器校验（尺寸、比例、可解码）与人工验收（文字、人物、真实素材）

未通过就进入下一轮，只重跑未通过项；已确认的文案与提示词不再重写。

---

## Architecture

把每次任务拆成可复用的层次：

| 层次 | 职责 |
| --- | --- |
| Agent 交互层 | 收集、确认、回报 |
| Workflow 层 | 内容理解 → 提案 → 生成 → 验收 |
| 资产层 | 内置身份图 + 风格图 + 本次素材 |
| 生成层 | Lovart Agent Channel |
| 质检层 | Content 校验、Prompt 编译、人工终检 |

核心价值不在“出图”本身，而在中间的 **Cover Brief** —— 内容、文案、版式、素材先被结构化为可复用的中间产物，再交给生成层。想要更换生成后端 / 模型，不必重写品牌逻辑。

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
│   └── lovart-channel.md    # Lovart 出图通道
├── tools/                   # 实现
│   ├── init.py              # 首次初始化
│   ├── resolve_assets.py    # 资产校验
│   ├── validate_brief.py    # Cover Brief 校验
│   ├── compile_prompt.py    # Prompt 编译
│   ├── validate_output.py   # 输出校验
│   └── lovart-agent.py      # Lovart 出图
├── examples/                # 案例
└── agents/                  # Agent 配置
```

---

## Security

- Lovart API Key 只从环境变量 `LOVART_ACCESS_KEY` / `LOVART_SECRET_KEY` 读取，从不落盘、不写库、不回显。
- 自带的身份 / 风格素材是本 Skill 的隐私边界：不检索外部人物，不替换默认形象。

---

## Development

```bash
python3 tools/validate_skill.py
python3 tools/test_agent_fallback.py
python3 tools/test_init.py
```

相关校验已接入 CI（`.github/workflows/validate.yml`）。

---

## Documentation

一套仓库，几层读者：

- **想直接用**：看 First Run 即可。
- **想了解内部**：`SKILL.md` → `references/workflow.md` → `references/style-guide.md`。
- **想扩展**：`tools/compile_prompt.py` + `references/prompt-template.md` 是起点。

---

## License

本项目采用 MIT License。其中 `tools/lovart-agent.py` 基于 [lovartai/lovart-skill](https://github.com/lovartai/lovart-skill)，具体归属见 NOTICE。
