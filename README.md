# qiuqiu-cover-prompt

「秋秋」微信公众号封面 Skill。它把一篇真实文章转换成统一的 2.35:1 横版封面：先读正文、提炼钩子、确认素材和文案，再生成或编辑图片。

Skill 的规范名称是 `$qiuqiu-wechat-cover`；`qiuqiu-cover-prompt` 是仓库名称。

## 能做什么

- 好物分享、AI 工具测评、旅行、学习效率、数码体验和桌面改造封面
- 固定暖木色复古像素工作台风格，保留真人秋秋和真实产品的辨识度
- 新封面与已有封面局部编辑
- 生成前提炼 3 个钩子，生成后检查比例、文字和素材一致性

它不替代正文策划，也不会在缺少文章、真人照、产品图或 Logo 时自行编造事实。

## 使用方式

把本仓库交给支持加载 Skill 的智能体，然后调用：

> 使用 `$qiuqiu-wechat-cover`，为这篇公众号文章生成封面：`/path/to/article.md`

调用时：

1. 提供完整正文、Markdown 内容或可读取的本地路径。
2. 默认 Image 1 是 Skill 内置的秋秋真人身份参考，默认 Image 2 是内置封面风格参考；Skill 会先验证并真实注入，不依赖你额外上传。
3. 按文章需要补充产品、Logo、截图、旅行照或旧封面；不需要的素材不用提供。
4. 先查看主题判断、3 个钩子和构图建议，确认文案后再明确说“生成/跑图”。

详细输入、阶段输出和失败处理见 [references/workflow.md](references/workflow.md)。

## 自包含品牌资产

本 Skill 是自包含的。安装仓库后已经包括：

- 秋秋真人身份参考
- 微信公众号固定视觉参考
- 工作流、提示词模板、验收规则

使用者无需单独下载秋秋真人照片、从历史对话找素材、连接个人素材库或从互联网搜索参考人物。安装后执行：

```bash
python3 tools/resolve_assets.py
```

正常情况下应返回 `ok: true` 和两个资产的 `absolute_path`；完整结构校验用：

```bash
python3 tools/validate_skill.py .
```

## 什么仍然需要用户提供

Skill 内置的是品牌资产，不是文章事实资产。

通常不需要用户再提供：秋秋真人身份参考、默认公众号视觉风格。仍然可能需要提供：当前文章的真实产品、产品包装、品牌 Logo、软件截图、旅行照片、需要编辑的原封面。内置资产缺失或无法真实注入时，Skill 会停止并说明运行时限制，不会凭空生成一个“像秋秋”的人物。

## 目录

```text
SKILL.md                          入口规则与硬约束
agents/openai.yaml                UI 展示和默认调用提示
references/workflow.md            输入角色、阶段协议、编辑边界
references/style-guide.md         2.35:1 视觉系统
references/prompt-template.md     可复制的生成提示词结构
references/prompt-checklist.md    生成前后验收清单
references/assets/                内置 Image 1、Image 2
tools/resolve_assets.py           查找、验证、暴露内置资产
tools/validate_skill.py           本地与 CI 校验
examples/                         已完成的示例
```

生成的 PNG/JPG/WebP 默认保存到项目目录之外。调用时请提供保存目录；仓库不接收生成图片。

## 校验与 CI

GitHub Actions 会在提交时运行 `python3 tools/validate_skill.py .`。该校验只检查结构、链接与必需资产，不替代生成后的视觉验收。

## 安装

仓库地址：<https://github.com/wangsiji/qiuqiu-wechat-cover>

## 许可

MIT License

