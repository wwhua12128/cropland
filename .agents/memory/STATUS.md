# STATUS — Cropland Delineator
Updated: 2026-10-14（v0.10.5：端点贴边线/公共边线也能正确切，全绿待她复测）

## Current Goal
花花同学（wwhua12128）接手维护；**0.10.5** 待她本机 QGIS 实测。
她自己实测 0.10.4「功能完全可用，磁力切分没问题了」，并指出她的习惯是把起终点
点在要切地块**边上**（而非两端落在地块外）——v0.10.5 就是照这个习惯堵漏。
当前：常态化维护（点选性能＋朋友实机反馈）；发版仍卡在上游权限。

## Just Finished
- **v0.10.5（2026-10-14）**：判界/量界的"锚点所在地块"改取**线体内侧一点**。
  端点正好压在两块地的公共边线上时，旧口径"与锚点相交的地块"两边都算 →
  并集量到对面边界，尾巴顺着邻块扫到底（实测 1000 m，很可能就是她前期
  观感的来源）。新增 T21，lasso 20→21 组。
- **v0.10.4（2026-10-14）**：修「收束后沿终点向外直甩一条线、横切邻块」——
  尾巴从 10~160 m 多甩改为"射线求交、只越 0.2 m"；线端落洞里切不开时退到
  外环重切一次。新增 T19/T20，lasso 19→20 组；详见 `daily/2026-10-14.md`。
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
