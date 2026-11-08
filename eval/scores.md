# 评分口径（scores）

> 本文定义 chart-eval-suite 的统一评分口径：**硬指标核验（自动）→ 视觉核验（模型/人工）→ 评分与等级**。
> 输入源为 [`dataset.md`](dataset.md)（14 例及各自 focus_points），产出见 [`cases/`](cases/) 与 [`reports/`](reports/)，复评结论记录于 [`review.md`](review.md)。

## 一、硬指标核验（自动，全部通过才计入评分）

| 编号 | 检查项 | 工具 / 口径 | 通过标准 |
|------|--------|------------|----------|
| H1 | 尺寸与比例 | `scripts/html2img.py` 输出 | `ok: true`，PNG 像素 = 逻辑视口 × scale(2)，长宽比与 dataset.md 一致 |
| H2 | 非空白渲染 | `check_png.py` `gray_extrema` / `unique_colors_ds` | 灰度极差 > 8 且降采样唯一色数 > 50（防空白/近空白） |
| H3 | 主题背景匹配 | `check_png.py` `bg_match`（四角采样，容差 ±12） | 四角均与该例主题 `--bg` 一致 |

复跑方式：

```bash
# H1：重渲染并校验（每例）
python scripts/html2img.py eval/cases/01-line/chart.html --out eval/cases/01-line/chart.png

# H2 + H3：按例传入该例主题背景色（light #ffffff / business #fffdf8 / dark #0f172a / warm #fffaf5）
python eval/check_png.py eval/cases/01-line/chart.png "#ffffff"
```

任一硬指标失败：该例直接判 **D 级**，不进入视觉核验，修复重渲染后再测。

## 二、视觉核验（按 focus_points 逐项）

对每例按 `dataset.md` 中该例的 4 条 focus_points 逐项判定 pass / fail。

- 模型检查：将 `chart.png` 与 focus_points 交给多模态模型（Qwen3-VL，结果归档于 `reports/inspect-*.json`），输出逐项结论；
- 人工复核：模型结论仅作初筛，最终以人工目检为准（模型可能漏判轻微裁切/重叠）。

通用否决项（任一命中即整例 fail，与 focus_points 并列）：

- 图表区空白（ECharts 未加载成功）
- 中文显示为方块 / 乱码
- 标题、副标题或脚注缺失、被裁切

## 三、评分与等级

每例 4 条 focus_points + 3 条否决项（未命中记 pass）：

```
例分 = 通过项数 / 7 × 100
```

| 等级 | 标准 |
|------|------|
| A | 例分 ≥ 95，且硬指标 H1-H3 全部通过 |
| B | 85 ≤ 例分 < 95，且硬指标 H1-H3 全部通过 |
| C | 70 ≤ 例分 < 85，且硬指标 H1-H3 全部通过 |
| D | 例分 < 70，或任一硬指标失败 |

套件整体结论 = 14 例最低等级；任一 D 级需打回修复后全套重测。

## 四、当前硬指标结果（2026-11-08 实测）

| ID | 用例 | 期望像素 | 实际像素 | H1 | H2 | H3 | 硬指标 |
|----|------|---------|---------|----|----|----|--------|
| 01 | 01-line | 2400×1350 | 2400×1350 | PASS | PASS | PASS | PASS |
| 02 | 02-stacked-line | 2400×1350 | 2400×1350 | PASS | PASS | PASS | PASS |
| 03 | 03-bar | 2400×1350 | 2400×1350 | PASS | PASS | PASS | PASS |
| 04 | 04-horizontal-bar | 2160×1620 | 2160×1620 | PASS | PASS | PASS | PASS |
| 05 | 05-stacked-bar | 2400×1350 | 2400×1350 | PASS | PASS | PASS | PASS |
| 06 | 06-pie | 2160×2160 | 2160×2160 | PASS | PASS | PASS | PASS |
| 07 | 07-donut | 2160×2160 | 2160×2160 | PASS | PASS | PASS | PASS |
| 08 | 08-scatter | 2400×1350 | 2400×1350 | PASS | PASS | PASS | PASS |
| 09 | 09-distribution-scatter | 2400×1350 | 2400×1350 | PASS | PASS | PASS | PASS |
| 10 | 10-linear-regression | 2400×1350 | 2400×1350 | PASS | PASS | PASS | PASS |
| 11 | 11-radar | 2160×2160 | 2160×2160 | PASS | PASS | PASS | PASS |
| 12 | 12-funnel | 2160×3840 | 2160×3840 | PASS | PASS | PASS | PASS |
| 13 | 13-gauge | 2160×2160 | 2160×2160 | PASS | PASS | PASS | PASS |
| 14 | 14-gantt | 2400×1350 | 2400×1350 | PASS | PASS | PASS | PASS |

14/14 硬指标全部通过；视觉核验与用户复评结论见 [`review.md`](review.md)。
