# Agent Bootstrap：首次使用强制初始化

这份文档定义 Agent 调用本 Skill 时的 Bootstrap Gate，优先于普通封面工作流。

## 核心规则

**首次触发 Skill，必须先完成 Bootstrap；未完成 Bootstrap，不得分析文章、生成 Cover Brief、编译 Prompt 或调用图像工具。**

Agent 不应假设“用户安装 Skill”就等于“已经初始化”。

每次新会话首次准备执行本 Skill 时：
1. 读取 `tools/init.py --check`（或 `--bootstrap`）获取状态。
2. 如果 `initialized=false`，立即进入初始化对话。
3. 如果 `initialized=true` 且 Lovart 已启用但 `credentials_status != configured`，先处理 Lovart 配置。
4. 只有 `next_action=continue_workflow` 才能进入正文工作流。

如果当前 Agent 无法执行 Python 或读取本地配置，仍必须执行同样的对话 Gate：把初始化状态视为 unknown，先询问人物与生成后端，不得假设已经配置。

## 第一次对话

### ① 人物身份

询问：

> 第一次使用这个封面 Skill，先设置一下长期人物身份：
>
> **A.** 使用 Skill 内置的「秋秋」人物
> **B.** 上传你自己的真人照片，作为以后长期使用的人物参考
>
> 如果选择 B，请现在上传一张你希望长期保持一致的人物参考图。

普通产品图、旅行照、截图、旧封面不能自动当人物图。只有用户明确指定“这张作为长期人物参考”时，才保存为 identity。

### ② 图片生成后端

紧接着询问：

> **图片生成要使用 Lovart 吗？**
>
> **A.** 使用 Lovart
> **B.** 暂时不用，先完成 Brief / Prompt 工作流

如果用户选择 A：
1. 检查当前运行环境是否有 `LOVART_ACCESS_KEY` 和 `LOVART_SECRET_KEY`。
2. 两者都存在 → 告知“Lovart 已配置”，继续。
3. 缺少任意一个 → **不要要求用户把密钥发到聊天里**；告诉用户使用当前 Agent 支持的安全 Secret / 环境变量配置，然后再次检查。
4. 两者都存在后，才写入非敏感配置并继续。

如果用户选择 B：保存 `provider=lovart, enabled=false`，不要求配置 Lovart 密钥。

## 未完成时不要偷偷默认

用户只回答一个问题时，继续问另一个问题；不要因为有默认人物或已有环境变量就替用户完成另一个选择。

自定义人物必须先获得用户确认，才设为长期 identity。

## Lovart 密钥安全

允许保存 provider、enabled、credentials_source、credentials_status。
禁止保存 LOVART_ACCESS_KEY、LOVART_SECRET_KEY、完整请求头、Authorization token 或响应中的密钥字段。
日志和最终回复中也不要回显密钥。

## 初始化完成状态

建议结构：

```json
{
  "initialized": true,
  "identity": {"mode": "default", "reference": "references/assets/qiuqiu-face-reference.jpg"},
  "generation": {
    "provider": "lovart",
    "enabled": true,
    "credentials_source": "environment",
    "credentials_status": "configured"
  }
}
```

如果用户选择 Lovart 但尚未配置，状态必须停在 Bootstrap，不得继续调用 Lovart。

## Agent 能力差异

- 能执行工具：使用 `tools/init.py --check` 读取状态。
- 只能读 Skill 文档：严格执行本文件的对话 Gate。
- 无法持久化状态：至少在当前会话保持初始化结果，并在下一次会话重新确认。
- 无法安全配置 Secret：不要要求用户在聊天中提供密钥。

Bootstrap 完成后才进入：`收集 → 分析 → 提案 → 生成/编辑 → 验收`。