# STATUS — Cropland Delineator
Updated: 2026-10-13（v0.10.3 修复经她本机验收）

## Current Goal
花花同学（wwhua12128）接手维护；插件 **0.10.3** 已在她本机 QGIS 4.2.2 实测可用。
当前：常态化维护（点选性能＋朋友实机反馈）；发版仍卡在上游权限。

## Just Finished
- **v0.10.3（2026-10-13）**：修「渔网里混进空几何要素 → 工作台打不开」
  （`_cell_id`/`_grid_cells` 跳过空几何 ＋ `setup_ui`/`run_annotate` 兜底弹窗），
  新增回归 T13，六套全绿（ledger 17/lasso 18/snap 6/bae 13/qa/clickseg 14）；
  提交 `6d5da2a` 已推 fork；她现场确认「可以正常打开，版本 v0.10.3」。
  顺带还原 `metadata.txt` 里双重编码的 name 乱码。
- Windows 迁移完成：SAM 环境全链路（py3.11 venv＋torch 2.6.0+cu124 上 RTX 4060，
  真 worker 冒烟 ready:cuda/pong ✓）、QGIS 4.2.2 无头六套全绿。
- 修三只真实 Windows bug：osm_roads.cache_path 判文件图层改 isfile；
  save_roads 撞文件锁退旁路文件（T9b 回归）；clickseg.find_nn_dir 建 realpath
  先行（mklink /J 联接安装找不到 nn/）。tests/win_headless.py 测试入口入仓。
- **fork 完成**：wwhua12128/cropland（原仓库实为 public）；remote fork=花花账号
  （提交已全部推上去，至本次），origin=上游 luohaoran616 便于日后同步。
- **QGIS 插件走联接**：profile（QGIS4/default）`python\plugins\cropland_delineator`
  是联接 → 工作区主线副本（现 0.10.3），改代码重启 QGIS 即生效；同名旧 0.10.1 实体
  副本已移出扫描路径至 `python\_archive_plugins\cropland_delineator_v089_bak`。

## Open Problems
- 发版（plugins.xml 给朋友升级）走上游 release，需 luohaoran616 权限——
  花花侧只能改 fork；要给朋友发新版时需原作者配合或转移插件源到 fork。
- 本机过滤器按映像位置拦 AppData 写入（venv pip 必须 --no-cache-dir＋TMP
  重定向，详见 RUNBOOK 与 knowledge/runbooks/2026-10-08-windows-dev-setup.md）。
- 决策 0021 等旧 knowledge 只在 Linux 旧机，未随仓库走，待补齐。
- 旧遗留 F3/F6 未动。

## Next Actions
1. 「🖱 点选」在她本机实测锁面＋密格性能（尚未实测）。
2. 朋友实机验证 0.10.3（碎块/缝隙/卡顿）。
3. 需发版给朋友时：找原作者推上游，或把朋友插件源切到 fork 的 release。

## Key Paths
- 仓库：工作区 `cropland/`；fork=wwhua12128/cropland；上游=luohaoran616/cropland
- 插件源码 `qgis-plugin/cropland_delineator/`（QGIS 经联接直接跑这份）；
  测试入口 `tests/win_headless.py`
- nn 推理环境 `nn/.venv`＋`nn/ckpt/sam_vit_b_01ec64.pth`；大轮子暂存 `..\..\.wheels\`
- 发版 `tools/publish.sh`（需 gh auth＋上游权限；本机无 gh）
