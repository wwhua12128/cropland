# Cropland Delineator 开发者指引

开工前先读 `.agents/memory/STATUS.md`；更深背景与写回规则见 project-memory 技能。

- 项目：QGIS 4 耕地标注插件（渔网驱动减法勾绘 + SAM 点选锁面），见 README.md。
- 目录法则：`<根>/qgis-plugin/cropland_delineator` 与 `<根>/nn` 必须平级，
  点选按 `../../nn` 相对路径找推理环境，挪位即失联。
- 无头回归：`tests/win_headless.py`（Windows/Linux 通吃，自带 PYTHONPATH 注入）。
- .gitignore 是白名单式：新顶层目录不进去就等于没提交，记得加放行规则。
