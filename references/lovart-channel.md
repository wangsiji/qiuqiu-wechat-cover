# Lovart 出图通道

Lovart 是本 Skill 的默认执行后端：一个把 CDN 参考图 + 提示词交给云端 Agent 生图并下载回本地的 API 通道。脚本已内置在 `tools/lovart-agent.py`，**零第三方依赖（纯 Python 标准库）**，无外装需求。

本文件是操作细节；品牌/文案/验收规则见 [SKILL.md](../SKILL.md) 与 [prompt-template.md](prompt-template.md)。

## 前置

```bash
export LOVART_ACCESS_KEY="ak_..."     # 用户提供，勿写入日志/提交
export LOVART_SECRET_KEY="sk_..."
```

首次会自动保存在 `~/.lovart/state.json`（项目与线程），一般无需手动建项目。

## 免费跑通（关键顺序）

```bash
SC=python3 tools/lovart-agent.py
# 1. 免费无限区：排队换额度，零扣费。必须先切，否则报 Insufficient credits。
python3 tools/lovart-agent.py set-mode --unlimited
python3 tools/lovart-agent.py query-mode          # 确认 unlimited:true
```

`--mode` 只能传 `{thinking,fast}`，**没有 unlimited**；无限模式用 `set-mode --unlimited` 全局开启，chat 时不要传 `--mode`。

## 跑一张封面

```bash
# 1. 内置身份图 + 风格图各 upload 成 CDN URL（每次新会话都要重新 upload，旧 URL 会失效）
python3 tools/lovart-agent.py upload --file <身份图绝对路径>   # → URL_1
python3 tools/lovart-agent.py upload --file <风格图绝对路径>   # → URL_2
# 2. 真实素材（如有）也 upload → URL_3 ...

# 3. 发起生成
python3 tools/lovart-agent.py chat \
  --project-id <从 projects --json 取准确ID> \
  --prompt "$(cat <提示词文件>)" \
  --attachments URL_1 URL_2 [URL_3...] \
  --json --download --output-dir /tmp/out
```

- `--project-id` 必须 `projects --json` 精确取值（手打必错）。
- `--attachments` 只认 CDN URL，本地路径无效。
- 不带 `--thread-id` = 新对话；续改带上一次返回的 `thread_id`。

## 常用命令

| 用途 | 命令 |
|---|---|
| 查项目/取准确 ID | `python3 tools/lovart-agent.py projects --json` |
| 续上次上下文 | chat 加 `--thread-id <id>` |
| 查进度 / 取结果 | `status --thread-id <id>` / `result --thread-id <id> --json --download` |
| 直接下载已有 URL | `download --urls URL1 URL2 --output-dir /tmp/out --prefix cover` |
| 高额度工具确认 | `confirm --thread-id <id> --json --download`（先给用户估费） |

## 已知坑（实测）

- **`Insufficient credits`** → 先 `set-mode --unlimited`（免费队列）。
- **`Project '<id>' does not exist`** → project-id 手打错，用 `projects --json`。
- **`generation_succeeded: false`** → 上游拒绝/超时；换 `--prefer-models` 或简化 prompt、或 `--include-tools` 换工具。
- **HTTP 429** → 限流，等约 60 秒重试。
- **HTTP 409 (2011)** → 同线程有任务在跑，等完成或换新线程。

## 验收

生成后按主协议用 PIL 量尺寸确认 2.35:1：

```bash
python3 -c "from PIL import Image; im=Image.open('结果.png'); print(im.size, im.size[0]/im.size[1])"
```

1880×800 → 2.350；1888×800 → 2.360（均达标）。中文逐字与人物轮廓若本机模型无 vision，须报「待确认」由用户亲眼核对。