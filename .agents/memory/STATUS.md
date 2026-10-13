# STATUS — Cropland Delineator
Updated: 2026-10-14（v0.10.4：磁力切分收束甩尾修复，全绿待她现场验收）

## Current Goal
花花同学（wwhua12128）接手维护；**0.10.4** 待她本机 QGIS 实测。
当前：常态化维护（点选性能＋朋友实机反馈）；发版仍卡在上游权限。

## Just Finished
- **v0.10.4（2026-10-14）**：修「磁力切分收束后沿终点向外直甩一条线、横切邻块」。
  根因是她台账里量到的外推尾巴 20~2271 m（公里级地块＋旧实现"探到界外再多走
  一整步"＋加速步长一步跨过窄缝/窄条田）。改为射线与所在地块境界线求交、只越
  0.2 m；线端落洞里切不开时退到外环重切一次。lasso 19→20 组，六套全绿；
  详见 `daily/2026-10-14.md`。
- **v0.10.3（2026-10-13）**：修「渔网里混进空几何要素 → 工作台打不开」
  （`_cell_id`/`_grid_cells` 跳过空几何 ＋ `setup_ui`/`run_annotate` 兜底弹窗），
  新增回归 T13，提交 `6d5da2a`；她现场确认「可以正常打开，版本 v0.10.3」。
- Windows 迁移完成：SAM 环境全链路（py3.11 venv＋torch 2.6.0+cu124 上 RTX 4060）、
  QGIS 4.2.2 无头六套全绿；QGIS 插件走**联接**指向工作区源码，改代码重启即生效。

## Open Problems
- 发版（plugins.xml 给朋友升级）走上游 release，需 luohaoran616 权限——
  花花侧只能改 fork；要给朋友发新版时需原作者配合或转移插件源到 fork。
- 本机过滤器按映像位置拦 AppData 写入（venv pip 必须 --no-cache-dir＋TMP
  重定向，详见 RUNBOOK 与 knowledge/runbooks/2026-10-08-windows-dev-setup.md）。
- 决策 0021 等旧 knowledge 只在 Linux 旧机，未随仓库走，待补齐。
- 旧遗留 F3/F6 未动。

## Next Actions
1. 让花花重启 QGIS 用 v0.10.4 复测磁力切分（重点：收束后还有没有多出来的直线）。
2. 「🖱 点选」在她本机实测锁面＋密格性能（尚未实测）。
3. 朋友实机验证 0.10.x（碎块/缝隙/卡顿）。
4. 需发版给朋友时：找原作者推上游，或把朋友插件源切到 fork 的 release。

## Key Paths
- 仓库：工作区 `cropland/`；fork=wwhua12128/cropland；上游=luohaoran616/cropland
- 插件源码 `qgis-plugin/cropland_delineator/`（QGIS 经联接直接跑这份）；
  测试入口 `tests/win_headless.py`
- nn 推理环境 `nn/.venv`＋`nn/ckpt/sam_vit_b_01ec64.pth`；大轮子暂存 `..\..\.wheels\`
- 发版 `tools/publish.sh`（需 gh auth＋上游权限；本机无 gh）
