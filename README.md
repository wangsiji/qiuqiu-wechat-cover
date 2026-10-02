<div align="center">

# ✨ qiuqiu-wechat-cover

**让公众号文章,拥有品牌级封面。**

从「读文章 → 提钩子 → 出图 → 逐轮改」的一条可复用封面工作流。

**零第三方依赖 · MIT License · 2.35:1 专用横版**

</div>


## 这是什么

给公众号内容做的封面,不再凭空生成、不再每次重排:

- 从你贴的文章**读**出主题、钩子与真实主体,而不是开头就出图;
- 出图前先把封面文案**钉死**成白名单(`copy.allowed_text`),杜绝「图对了、字飘了」;
- **内置品牌资产**(身份图 + 风格图 + 版式),一套「暖木像素 × 温馨明亮」可复用;
- 每阶段有检查点,出图后还要过**机器门禁 + 人工查**;
- 想改封面某一处(删一句话 / 换 Logo / 调脸),**只动那一点**,不推翻重来;
- 主图像 key 积分不够时,**自动切备用 key + 免费队列**,不卡壳中断。

一套仓库,反复出图,而不必每次重建品牌逻辑。

## 案例

同一套流程,可处理好物、生活方式、旅行等不同公众号题材。

<p align="center">
  <img src="examples/cover-case-01.jpg"        alt="好物封面"        width="40%"/>
  <img src="examples/cover-case-02.jpg"        alt="生活方式封面"    width="40%"/>
</p>


## 快速开始(60 秒上手)

> 首次使用,先花 30 秒做一次 **启动配置**——确认两件事:人物身份、是否用 Lovart。之后不再问。

```bash
git clone https://github.com/wangsiji/qiuqiu-wechat-cover
cd qiuqiu-wechat-cover

# ① 配图片后端(可选:不配也能先跑文案/校验部分)
export LOVART_ACCESS_KEY="ak_..."      # 主 key
export LOVART_SECRET_KEY="sk_..."
export LOVART_BACKUP_ACCESS_KEY="ak_..."   # 备用 key(可选,可多把: BACKUP2/3/4)
export LOVART_BACKUP_SECRET_KEY="sk_..."

# ② 启动配置:确认人物身份 + 是否用 Lovart
python3 tools/init.py --identity default --lovart yes
```

然后,日常只需要一句:

> 帮我把这篇公众号文章做一张封面。

顺手把产品图 / 人物图 / 旅行照片丢进去也行;都不放也没关系,会走「内置身份 + 文字」方案。
全部命令都应在仓库根目录运行。

> 🔐 **密钥纪律**:`LOVART_*` 只存在于运行环境(env / Agent 的 Secret),绝不写入 `config.json`、Git 或聊天记录。


## 封面是怎么出来的

封面**不是一次出一张**,而是**一条可验收的流水线**,每步都有检查点:

1. **读** — 提取主题、钩子、真实主体
2. **写** — 写成结构化 Cover Brief(标题、文案、版式、素材)
3. **锁** — 与你确认文案,锁定进 `copy.allowed_text`
4. **编** — 编译成图像 Prompt,注入内置身份图 / 风格图 / 真实素材
5. **生** — 由图后端出图
6. **验** — 机器门禁(尺寸 / 比例 / 可解码)+ 人工终检(文字 / 人物 / 素材)

未通过,下一轮**只修对应项**,已批准的文案和 Prompt 不动。


## 架构

把每次出图任务拆成可复用层次。最关键的——是中间的 **Cover Brief**:
把内容、文案、版式、素材先结构化成一个可复用的中间产物,再交给图后端。将来想换后端 / 模型,不用重写品牌逻辑。

| 层 | 职责 |
| --- | --- |
| Agent 交互层 | 收集、确认、回报(任意 agent 均可) |
| 流程层 | 内容理解 → 提案 → 生成 → 验收 |
| 资产层 | 内置身份图 + 风格图 + 本次素材 |
| 生成层 | Lovart Agent Channel(默认) |
| 质检层 | brief 校验、prompt 编译、输出机器门禁、人工终检 |

```
文章
 │
 ▼
Cover Brief  ──▶ Prompt ──▶ 图后端 ──▶ 封面
 │                │           │
文案锁定        内置资产注入  机器 + 人工验收
```


## 不使用 Agent 的纯命令行用法

仓库主体全是 **Python 标准库**,零第三方依赖——即使你不接任何特别 Agent,也能这样直接推全流程:

```bash
# ① Cover Brief：先想清楚内容与文案
python3 tools/init.py --check                                # 状态探针(应为 continue_workflow)
python3 tools/validate_brief.py my-brief.json                # Cover 契约校验(必须通过)
python3 tools/compile_prompt.py my-brief.json -o prompt.txt  # 编译成图像 Prompt

# ② 出图(Lovart, 需密钥)
python3 tools/lovart-agent.py set-mode --unlimited           # 免费队列(排队换额度)
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

> 想接别的图后端?`resolve_assets.py` 能把内置参考图导出为 `data URI` 或绝对路径,喂给任意能收图的 API(Stable Diffusion / Gemini / MiniMax…)。品牌逻辑固化在仓库,**不绑定 Lovart**。


## 目录结构

```text
.
├── SKILL.md                 # Skill 定义与触发规则
├── references/              # 领域规则(流程、身份、素材、文案、版式、Lovart)
├── tools/                   # 实现主体(纯标准库 CLI)
│   ├── init.py              # 首次初始化 / 状态探针
│   ├── resolve_assets.py    # 资产校验 / 导出
│   ├── validate_brief.py    # Cover Brief 契约校验
│   ├── compile_prompt.py    # Prompt 编译
│   ├── validate_output.py   # 输出机器校验
│   └── lovart-agent.py      # Lovart 出图(含多 key 兜底)
├── examples/                # 完工封面案例
└── agents/                  # Agent 约定
```



## 开发与验证

```bash
python3 tools/validate_skill.py          # 完整性 + 链接 + 必需文件
python3 tools/test_agent_fallback.py     # 多 key 兜底回归
python3 tools/test_init.py               # 首次引导回归
```

以上已接入 CI(`.github/workflows/validate.yml`),每次 push 自动跑。


## 学习路径

| 你想做的事 | 看这里 |
| --- | --- |
| 拿回来直接用 | **快速开始** & 上面的命令 |
| 理解内部设计 | `SKILL.md` → `references/workflow.md` → `references/style-guide.md` |
| 自己想接通到别的图后端 | `tools/compile_prompt.py` + `references/prompt-template.md` |
| 通道细节 / 已知坑 | `references/lovart-channel.md` |

---

## License

MIT License。其中 `tools/lovart-agent.py` 以 [lovartai/lovart-skill](https://github.com/lovartai/lovart-skill) 为基础,归属见 NOTICE。
