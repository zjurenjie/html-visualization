# Implementation Plan: chart-eval-suite

**Input**: Feature specification from `spec/chart-eval-suite/spec.md`

## Summary

为 html-visualization skill 构建 14 图型评测基准：在 `eval/` 下沉淀评测数据集（14 个基准场景用例，差异化覆盖 4 主题 × 4 类长宽比），由 Agent 按 SKILL.md 六步工作流逐场景生成 HTML+PNG，逐例执行硬指标核验与 AI 视觉评分（0-10 四维度），最终产出评分报告与用户复评表，形成「生成 → 评分 → 用户复评 → 修正」的质量闭环。

## Technical Context

**Language/Version**: Python 3.8+（渲染脚本）、HTML/JS（ECharts 5.5.1 图表）  
**Primary Dependencies**: Pillow（PNG 尺寸校验）、Chrome/Edge headless（截图）、本地 `assets/echarts.min.js`（离线兜底）  
**State Management**: N/A（无前端状态管理，纯静态产物）  
**Storage**: 仓库内文件系统（`eval/` 目录，markdown + HTML + PNG）  
**Testing**: 评测即测试——每例以硬指标（渲染 ok + 像素比例一致）+ 视觉评分代替自动化测试  
**Target Platform**: Windows 本机执行，产物为跨平台可查看的 HTML/PNG  
**Project Type**: 现有 skill 仓库的评测资产扩展（非应用代码）  
**Performance Goals**: 单图渲染 < 90s（脚本默认超时），14 例全流程可在一个会话内完成  
**Constraints**: 不修改 skill 现有模板/脚本，除非评分发现缺陷；评测数据不虚构为真实统计（标注虚构）  
**Scale/Scope**: 14 个用例、14 套 HTML+PNG 产物、1 份评分报告、1 份复评表

## Project Structure

### Documentation (this feature)

```text
spec/chart-eval-suite/
├── spec.md              # 需求规格
├── plan.md              # 本文件
└── tasks.md             # 任务清单（Phase 3 生成）
```

### Source Code (repository root)

```text
eval/                          # 评测资产根目录（本次新增，skill 仓库一部分）
├── README.md                  # 评测集说明：结构、如何再执行、如何复评
├── dataset.md                 # 评测数据集：14 个基准场景用例（唯一输入源）
├── cases/                     # 逐例产物目录（每例一个子目录）
│   ├── 01-line/
│   │   ├── chart.html         # 按 SKILL.md 工作流生成的图表 HTML
│   │   └── chart.png          # 按用例指定比例渲染的 PNG
│   ├── 02-stacked-line/
│   │   └── ...
│   └── 14-gantt/
│       └── ...
├── scores.md                  # 评分报告：硬指标 + AI 视觉评分 + 问题清单（逐例）
└── review.md                  # 用户复评表：AI 评分 + 缩略图引用 + 用户复评列（留空待填）
```

**Structure Decision**: 遵循现有仓库结构（`templates/`、`scripts/`、`assets/`、`examples/`、`references/`）。本次不新建代码模块，只新增 `eval/` 评测资产目录与 `spec/` 流程文档目录；产物按「一例一目录」组织，便于逐例复评与重渲染。关键路径约束：`eval/cases/<id>/chart.html` 距 `assets/` 有三级，离线兜底路径须写为 `../../../assets/echarts.min.js`（模板默认 `../assets/` 需在生成时修正）。

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 一例一目录（14 个子目录）而非全部平铺 `eval/` | 逐例复评时需精确定位某例的 HTML+PNG 并重渲染，互不干扰 | 平铺会让 28+ 个文件混杂，复评与修正难以定位 |

## Research & Decisions

### D1: 评测数据集载体用单个 markdown 文件

- **Decision**: `eval/dataset.md` 单文件承载全部 14 个用例（矩阵总览 + 逐例结构化小节）
- **Rationale**: Agent 逐场景执行，单文件即单一输入源，可读性与可维护性最佳；评分要点与场景描述天然适合 markdown
- **Alternatives considered**: JSON（机器友好但场景描述可读性差，且 runner 已排除在本次范围外）；每例一个文件（14 个文件碎，总览困难）

### D2: 主题 × 长宽比分配矩阵

- **Decision**: 按下表分配，4 主题各 ≥2 例、16:9 / 1:1 / 9:16 全覆盖，并顺带覆盖 4:3
- **Rationale**: 在 14 例内最大化参数覆盖；场景业务语义与主题气质匹配（如漏斗+营销用 warm+9:16，散点+技术用 dark）
- **Alternatives considered**: 全部 light+16:9（无法评测主题与竖屏适配，已否决）；每图型 4 主题全排列（56 例，超出本次规模）

| # | 图型 | 场景 | 主题 | 比例 |
|---|------|------|------|------|
| 01 | 折线图 | 2026 年月度活跃用户趋势 | light | 16:9 |
| 02 | 堆叠折线图 | 四大渠道月度访问量累计 | business | 16:9 |
| 03 | 柱状图 | 六大区季度销售额对比 | light | 16:9 |
| 04 | 横向条形图 | 10 大编程语言流行度排行 | warm | 4:3 |
| 05 | 堆叠柱状图 | 三渠道季度销售额构成 | business | 16:9 |
| 06 | 饼图 | 五类健身课程受欢迎度占比 | warm | 1:1 |
| 07 | 环形图 | 四端流量构成（中心总计） | light | 1:1 |
| 08 | 散点图 | 30 款车型马力 vs 百公里加速 | dark | 16:9 |
| 09 | 分布散点图 | 食品营养成分分布（4 类 ×150 点） | dark | 16:9 |
| 10 | 线性回归图 | 广告投入 vs 销售额（标注公式与 R²） | light | 16:9 |
| 11 | 雷达图 | 两款产品六维能力对比 | dark | 1:1 |
| 12 | 漏斗图 | 电商购买转化漏斗五阶段 | warm | 9:16 |
| 13 | 仪表盘 | 年度 KPI 完成率 | business | 1:1 |
| 14 | 甘特图 | 产品 v2.0 发布排期（4 车道） | light | 16:9 |

主题计数：light×5、business×3、dark×3、warm×3；比例计数：16:9×8、4:3×1、1:1×4、9:16×1。

### D3: 评分方案（硬指标 + AI 视觉四维度）

- **Decision**: 两层评分。① 硬指标（通过/失败）：渲染 `ok:true`、像素尺寸与比例精确一致、PNG 非空白；② AI 视觉评分 0-10 分，四维度加权：可读性 4 分（无溢出/裁切/重叠/方块字）+ 布局留白 2 分 + 主题一致性 2 分（配色符合主题令牌）+ 数据表达 2 分（图型合理、标签与单位规范）。≥9 优；7-8.9 良；<7 必须修正重渲染
- **Rationale**: 硬指标客观可自动判定；四维度把「效果好」拆解为可对照图片复核的检查项，用户复评时有共同语言
- **Alternatives considered**: 单一总分（无问题清单，无法定位修正点）；百分制（颗粒度虚假，14 例规模无意义）

### D4: 用户复评表与修正闭环机制

- **Decision**: `eval/review.md` 表格：每例一行，含缩略图引用、AI 评分、问题摘要、留空的「用户复评」与「处理结果」列。用户以 ✅/❌+批注复评；❌ 例由 Agent 修正 HTML → 重渲染 → 更新 scores.md 与 review.md「处理结果」列
- **Rationale**: 表格化复评把用户二次评价成本降到最低（逐行打勾/打叉），处理结果列让修正可追溯
- **Alternatives considered**: 对话式逐图确认（14 轮对话效率低）；JSON 评分文件（用户不便填写）

### D5: 逐例生成沿用 SKILL.md 工作流，产物命名固定

- **Decision**: 每例严格走 SKILL.md 六步：解析数据 → 参数确认（用例已指定，无默认项）→ 选型选主题 → 复制模板生成 HTML（甘特图用 gantt-template）→ `html2img.py` 渲染 → 视觉自检。产物固定命名 `eval/cases/<id>-<type>/chart.html` + `chart.png`
- **Rationale**: 固定命名让评分、复评、重渲染的引用路径稳定；沿用工作流保证评测的是 skill 真实使用方式
- **Alternatives considered**: 批量脚本生成（偏离「真实触发 skill」的评测目的，已否决）

## Data Model

### EvalCase（评测用例，`eval/dataset.md` 逐例小节）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 用例编号 `01`-`14` |
| `chart_type` | string | 目标图型（14 种之一，英文 slug 用于目录名） |
| `scenario` | string | 业务场景一句话描述 |
| `title` / `subtitle` | string | 图表标题 / 副标题（含范围与单位） |
| `data` | structured | 场景数据（字段、类别、数值；标注虚构） |
| `theme` | enum | `light` / `business` / `dark` / `warm` |
| `ratio` | string | 长宽比 `W:H` |
| `logical_width` | number | 逻辑宽（16:9→1200；1:1/9:16/4:3→1080） |
| `focus_points` | string[] | 评分要点（该图型特有的检查项，如回归图必须标注公式与 R²） |

### ScoreRecord（评分记录，`eval/scores.md` 逐例小节）

| 字段 | 类型 | 说明 |
|------|------|------|
| `case_id` | string | 关联用例编号 |
| `hard` | object | 渲染 ok、像素尺寸、比例偏差（必须为 0） |
| `visual_scores` | object | 四维度分项：readability(0-4) / layout(0-2) / theme(0-2) / data_expr(0-2) |
| `total` | number | 视觉总分 0-10 |
| `issues` | string[] | 问题清单（空为无问题） |
| `revision` | number | 修正轮次（初评 0） |

### ReviewEntry（复评表行，`eval/review.md`）

| 字段 | 类型 | 说明 |
|------|------|------|
| `case_id` / `chart_type` | string | 用例标识 |
| `image_ref` | string | `cases/<id>/chart.png` 相对引用（markdown 缩略） |
| `ai_score` | number | AI 视觉总分 |
| `issues_summary` | string | 问题摘要 |
| `user_review` | string | 用户复评（✅ / ❌+批注，初版留空） |
| `resolution` | string | 处理结果（修正说明或「无需修正」，初版留空） |

## Contracts & Interfaces

### C1: `eval/dataset.md` 用例小节格式

每例一个 `## CASE 01: 折线图` 小节，内含固定字段表 + 数据块 + 评分要点列表。该文件是生成阶段的唯一输入源；修改用例参数视同数据集变更，须同步 scores.md 与 review.md。

### C2: 渲染调用契约（复用现有脚本，不改动）

```
python scripts/html2img.py eval/cases/<id>-<type>/chart.html --ratio <用例比例> --width <逻辑宽> --scale 2 --out eval/cases/<id>-<type>/chart.png
```

成功标准：JSON `ok: true` 且 `pixels` 宽高比与用例 `ratio` 精确一致。甘特图用例改用 `templates/gantt-template.html` 复制生成。

### C3: `eval/scores.md` 评分报告格式

顶部 14 行总览矩阵（用例 / 硬指标 / 四维分项 / 总分 / 结论），其后逐例小节含硬指标详情与问题清单。每轮修正后原位更新。

### C4: `eval/review.md` 复评表契约

单表 14 行，列为：用例 | 图型 | 预览 | AI 评分 | 问题摘要 | 用户复评 | 处理结果。用户复评列初版留空；用户回复 ❌ 的行必须回填处理结果。用户可以自由文本形式给出复评意见，Agent 负责转录进表。

### C5: `eval/README.md` 评测说明契约

说明目录结构、再执行方式（按 dataset.md 逐例走 SKILL.md 工作流）、评分口径、复评流程，保证评测集对仓库其他使用者自解释。
