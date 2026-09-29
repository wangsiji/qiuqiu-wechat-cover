# qiuqiu-wechat-cover

生成「秋秋」微信公众号封面的一套可迁移 Agent Skill：把一篇真实文章，转成统一 **2.35:1 横版品牌封面** —— 先读正文、提炼钩子、确认文案，再由内置的 Lovart 后端出图，全程内置真人形象与视觉风格，无需外部素材。

规范名 `$qiuqiu-wechat-cover`。

## 特性

- **品牌内置**：秋秋真人身份图 + 暖木复古像素风格图随包分发（图 1 身份、图 2 风格），无需你搜图、传图或连素材库。
- **流程闭环**：收集 → 分析 → 提案 3 钩子 → 生成/编辑 → 验收；文案未确认不出图。
- **真实优先**：真实产品/Logo/旅行照原样使用，绝不凭空编造人物、品牌或事实。
- **可迁移**：Lovart 出图后端（`tools/lovart-agent.py`，纯 Python 标准库）与其他辅助脚本全部随包分发。

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/wangsiji/qiuqiu-wechat-cover

# 2. 挂到智能体 Skill 目录（Hermes 示例）
cp -r qiuqiu-wechat-cover ~/.hermes/skills/

# 3. 配置 Lovart 密钥（出图后端）
export LOVART_ACCESS_KEY="ak_..."
export LOVART_SECRET_KEY="sk_..."

# 4. 验证内置资产与结构
cd ~/.hermes/skills/qiuqiu-wechat-cover
python3 tools/resolve_assets.py       # 应输出 ok:true 和两个 absolute_path
python3 tools/validate_skill.py .

# 5. 让智能体生成
#    → "对这篇公众号文章生成封面：/path/to/article.md"
```

## 用法

1. 提供完整正文 / Markdown / 可读路径。只有标题会被标记「待确认」。
2. 默认 图 1 = 内置秋秋身份，图 2 = 内置封面风格；按文章需要再补 产品/Logo/截图/旅行照（从 图 3+ 编号）。
3. 先看 `主题判断 + 3 个钩子 + 推荐构图`，确认文案后再明确说“生成”。
4. 出图默认走 Lovart（`set-mode --unlimited` 免费队列跑通，详见 [references/lovart-channel.md](references/lovart-channel.md)）。

## 在产案例

「秋秋很开心」公众号近几个月用本 Skill 出封面的文章（真实微信链接，摘自内容资产库）：

| 日期 | 文章 | 链接 |
|---|---|---|
| 2026-09-22 | 我的100件长期好物：头发护理神器来啦！ | https://mp.weixin.qq.com/s/oQ3wi4pJ14ug6QoDsDDDEw |
| 2026-09-21 | 我的100件长期好物：随身配饰来啦！ | https://mp.weixin.qq.com/s/ncwJ6NXK-9eRE3FOLlWqfg |
| 2026-09-11 | 懒人要避开的思维方式！ | https://mp.weixin.qq.com/s/RCbIz2iI9KNyF63zfRaiaw |
| 2026-09-09 | 日常好用，分享7款超可爱的收纳小包！ | https://mp.weixin.qq.com/s/7k8O-D1U2JRUZLmlN4nw9Xg |
| 2026-09-06 | 照片 Skill｜拯救旅行废片，试试这 6 种风格！！！ | https://mp.weixin.qq.com/s/Elf3PrEmMURTfOr2zNohuA |
| 2026-09-04 | 不到 50 块，就能打造高颜值书桌！ | https://mp.weixin.qq.com/s/ul-JXY4gMjH15E1IrPqiig |
| 2026-09-01 | 会无限回购，提高效率的好用本子来啦！ | https://mp.weixin.qq.com/s/Rfnugp22ysYqD8c9PjkRZw |
| 2026-08-30 | 豆包工作、千问办公、WorkBuddy：谁真的能替你干活？ | https://mp.weixin.qq.com/s/sPTTTKvXSQvbNX21u1pDUw |
| 2026-08-28 | 只要3000+，MacBook Neo 值不值得买？ | https://mp.weixin.qq.com/s/Xe3HMYY0NxsDxuKw3ghsqw |

封面例图（在产案例）：

| 封面 | 说明 |
|---|---|
| ![cover-case-01](examples/cover-case-01.jpg) | 案例封面 1 |
| ![cover-case-02](examples/cover-case-02.jpg) | 案例封面 2 |
| ![cover-japan-12days](examples/cover-japan-12days.png) | 日本 12 天攻略（2.35:1，1888×800） |

> 链接与封面图来自内容资产库 [qiuqiu-content-engine](https://github.com/wangsiji/qiuqiu-content-engine) 的 `articles_data.json`；微信链接时有失效，最新以公众号后台为准。

## 目录

```text
SKILL.md                          入口规则与硬约束
agents/openai.yaml                UI 展示与默认提示
references/
  workflow.md                     输入角色、阶段协议、处理边界
  style-guide.md                  2.35:1 视觉系统
  prompt-template.md              可复制的提示词结构
  prompt-checklist.md             生成前后验收清单
  lovart-channel.md               出图后端操作细节（含免费跑通法）
  assets/                         内置 Image 1（身份）与 Image 2（风格）
tools/
  resolve_assets.py               查找、校验、暴露内置资产
  validate_skill.py               本地 & CI 级完整性校验
  lovart-agent.py                 Lovart 出图后端（纯标准库）
examples/                         已完成的示例
```

## 约束（触发器）

- 画布严格 **2.35:1**，优先 1880×800。
- 视觉 = 暖木 × 复古像素 × 温馨工作台 × 真实主体。
- 文案最多 3 组、全页约 20~35 汉字，主标题唯一焦点。
- 保留口罩，真实感约 80% + 像素 20%；不做全像素/卡通/换脸。
- 身份与风格禁止外部检索；缺真人照时不虚构人物。

## 校验与 CI

`tools/validate_skill.py` 覆盖：必需文件、相对链接、资产文件头、Lovart 后端存在且纯标准库、SKILL 关键措辞。GitHub Actions 在每次提交运行：

```bash
python3 tools/validate_skill.py .
```

该校验检查结构，不替代出图后的视觉验收（中文逐字、人物轮廓需人为核对）。

## 许可

[MIT](LICENSE)。内置 `tools/lovart-agent.py` 取自 [lovartai/lovart-skill](https://github.com/lovartai/lovart-skill)（MIT），其归属声明见 [NOTICE](NOTICE)。