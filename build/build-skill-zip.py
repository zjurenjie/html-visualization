#!/usr/bin/env python3
"""把 Agent Skill 相关可发布内容打包为 zip。

产出 dist/html-visualization-skill.zip，解压得到 html-visualization/ 目录，
可直接放入兼容 Agent 的 skills 目录使用。

用法（在项目根目录执行）：

    python build/build-skill-zip.py              # 构建 dist/html-visualization-skill.zip
    python build/build-skill-zip.py --list       # 只查看将打入 zip 的文件
    python build/build-skill-zip.py --out x.zip  # 指定输出路径

zip 只包含技能运行所需文件（SKILL.md、3 个模板、渲染脚本、离线 ECharts、
参考文档、LICENSE），不含 README、examples、docs 展示截图等项目文件。
仅依赖 Python 标准库（zipfile）；固定时间戳打包，同一份源码多次构建产物一致。
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

ZIP_ROOT = "html-visualization"  # zip 内顶层目录名（即安装后的 skill 目录名）
FIXED_DATE = (2026, 1, 1, 0, 0, 0)  # 固定时间戳，保证构建可复现

# 技能运行所需文件（相对项目根目录，顺序即 zip 内排列顺序）
SKILL_FILES = [
    "SKILL.md",
    "LICENSE",
    "assets/echarts.min.js",
    "references/chart-design.md",
    "scripts/html2img.py",
    "templates/echarts-template.html",
    "templates/gantt-template.html",
    "templates/gallery.html",
]

DEFAULT_OUT = ROOT / "dist" / "html-visualization-skill.zip"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="打包 Agent Skill zip")
    parser.add_argument(
        "--out",
        default=None,
        help="输出 zip 路径（默认 dist/html-visualization-skill.zip）",
    )
    parser.add_argument(
        "--list", action="store_true", help="列出将打入 zip 的文件后退出"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.list:
        for rel in SKILL_FILES:
            print(f"{ZIP_ROOT}/{rel}")
        return 0

    # 1. 校验源文件齐全，缺一个都拒绝打包
    missing = [rel for rel in SKILL_FILES if not (ROOT / rel).is_file()]
    if missing:
        print(f"缺少文件，无法打包：{'、'.join(missing)}", file=sys.stderr)
        return 1

    out = (pathlib.Path(args.out) if args.out else DEFAULT_OUT).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    # 2. 打包（ZipInfo 固定时间戳 → 可复现构建）
    total = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel in SKILL_FILES:
            data = (ROOT / rel).read_bytes()
            info = zipfile.ZipInfo(f"{ZIP_ROOT}/{rel}", date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data)
            total += len(data)

    # 3. 汇总
    try:
        out_display = out.relative_to(ROOT)
    except ValueError:
        out_display = out
    print(f"已打包 {len(SKILL_FILES)} 个文件 -> {out_display}")
    print(f"原始 {total / 1024:.0f} KB -> 压缩后 {out.stat().st_size / 1024:.0f} KB")
    print(f"安装：解压到 Agent 的 skills 目录，得到 skills/{ZIP_ROOT}/SKILL.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
