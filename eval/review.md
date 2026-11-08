# 用户复评闭环（review）

> 复评流程：**生成 → 硬指标核验 → 模型视觉检查 → 用户复评 → 归档 / 打回**。
> 硬指标口径见 [`scores.md`](scores.md)；模型检查结果见 [`reports/inspect-*.json`](reports/)。

## 一、流程说明

1. **生成**：Agent 按 `SKILL.md` 六步工作流逐例生成 `cases/<id>-<type>/chart.html` 并渲染 `chart.png`。
2. **硬指标核验**：`check_png.py` + 像素尺寸校验（H1-H3，见 `scores.md`），失败直接打回重渲染。
3. **模型视觉检查**：多模态模型按各例 focus_points 逐项检查，结果归档 `reports/inspect-<id>.json`。
4. **用户复评**：用户按下表逐例目检，填写复评结论（`通过` / `打回`）与备注。
5. **归档 / 打回**：
   - 全部 `通过` → 本轮评测归档，更新下表状态；
   - 任一 `打回` → 在备注记录问题 → 修复 `chart.html` → 重渲染 → 重跑硬指标与视觉检查 → 用户再次复评。

## 二、复评状态表

> 状态取值：`待复评` / `通过` / `打回`。模型检查列指 `reports/` 中对应报告；最终结论以用户复评为准。

| ID | 用例 | 图型 | 硬指标（scores.md） | 模型检查报告 | 用户复评 | 备注 |
|----|------|------|--------------------|--------------|----------|------|
| 01 | 01-line | 折线图 | PASS | `reports/inspect-01.json` | 通过 | |
| 02 | 02-stacked-line | 堆叠折线图 | PASS | `reports/inspect-02.json` | 通过 | |
| 03 | 03-bar | 柱状图 | PASS | `reports/inspect-03.json` | 通过 | |
| 04 | 04-horizontal-bar | 横向条形图 | PASS | `reports/inspect-04.json` | 通过 | |
| 05 | 05-stacked-bar | 堆叠柱状图 | PASS | `reports/inspect-05.json` | 通过 | |
| 06 | 06-pie | 饼图 | PASS | `reports/inspect-06.json` | 通过 | |
| 07 | 07-donut | 环形图 | PASS | `reports/inspect-07.json` | 通过 | |
| 08 | 08-scatter | 散点图 | PASS | `reports/inspect-08.json` | 通过 | |
| 09 | 09-distribution-scatter | 分布散点图 | PASS | `reports/inspect-09.json` | 通过 | |
| 10 | 10-linear-regression | 线性回归图 | PASS | `reports/inspect-10.json` | 通过 | |
| 11 | 11-radar | 雷达图 | PASS | `reports/inspect-11.json` | 通过 | |
| 12 | 12-funnel | 漏斗图 | PASS | `reports/inspect-12.json` | 通过 | |
| 13 | 13-gauge | 仪表盘 | PASS | `reports/inspect-13.json` | 通过 | |
| 14 | 14-gantt | 甘特图 | PASS | `reports/inspect-14.json` | 通过 | |

## 三、复评检查清单（每例目检时逐项过一遍）

- [ ] 图表区非空白，ECharts 正常渲染
- [ ] 无方块字 / 乱码，中文显示正常
- [ ] 标题、副标题、脚注完整，无裁切
- [ ] 该例 focus_points 逐条满足（见 `dataset.md` 对应 CASE）
- [ ] 整体留白、配色与所选主题一致

## 四、轮次记录

| 轮次 | 日期 | 范围 | 结果 |
|------|------|------|------|
| R1 | 2026-11-08 | 全部 14 例 | 硬指标 14/14 PASS，模型检查完成，用户复评进行中 |
