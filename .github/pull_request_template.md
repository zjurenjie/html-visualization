## 概要

<!-- 这个 PR 改了什么、为什么改？ -->

## 关联 issue

<!-- 关联的 issue，如 Closes #123；没有可删除。 -->

## 变更内容

-

## 验证

<!-- 如何验证的？粘贴关键命令输出或对比截图。 -->

## 检查清单

- [ ] 改动涉及 Python 时：`python -m compileall scripts build eval` 通过
- [ ] `python build/build-skill-zip.py` 构建成功，且两次构建产物逐字节一致（可复现构建）
- [ ] 改动涉及模板 / 渲染时：`python build/build-examples.py` 冒烟渲染 + `eval/check_png.py` 校验通过
- [ ] README / SKILL.md / docs 已同步更新（若行为或用法变化）

> 注：CI 会在 PR 上自动运行 Python 语法检查、zip 可复现构建校验与三个示例的渲染冒烟（html2img + check_png）。
