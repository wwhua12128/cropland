# STATUS — Cropland Delineator
Updated: 2026-10-08

## Current Goal
Windows 开发机全量开发测试能力恢复（六套回归全绿达成）；等推送凭据与 torch 尾工。

## Just Finished
- Windows 迁移完成：仓库克隆（2268f75、f1c2e49）、SAM 环境全链路（py3.11 venv＋
  torch 2.6.0+cu124 上 RTX 4060＋权重 sha256 ✓，真 worker 冒烟 ready:cuda/pong ✓）、
  QGIS 4.2.2 无头六套全绿（ledger 17/lasso 17/snap 6/bae 12/qa/clickseg 14）。
- 大轮子下载经验：官方源单连接会被掐（56）且限速；**分 4 块 -r 并行 + 流追加**
  10 分钟收完 2.4GB（脚本思路见 daily/2026-10-08）。
- 修三只真实 Windows bug（Linux 从未暴露，均测试移植后现形）：
  ①osm_roads.cache_path 的 startswith("/") 判文件图层 → os.path.isfile；
  ②save_roads 撞文件锁 PermissionError → 旁路文件退让（T9b 回归）；
  ③clickseg.find_nn_dir 在 mklink /J 联接安装下词法折叠找不到 nn/ → realpath 先行。
- tests/win_headless.py 入仓（PYTHONPATH 注入＋每套子进程隔离）；T2/T6b/T7 测试
  可移植性适配；README 补 Windows 无头用法；.agents 记忆四件套＋AGENTS.md 入仓。

## Open Problems
- 推送受阻：本机 git 凭据 wwhua12128 对私库只读，需 luohaoran616 身份重新认证
  后 push（2268f75＋f1c2e49 在本地 main）。
- 用户 QGIS（开着）挂的是 D:\software\cropland v0.8.9 旧线——无锁面修复，建议
  升级到主线 release 或把 QGIS profile 插件目录联接到工作区副本（mklink /J）。
- 本机过滤器按映像位置拦 AppData 写入（venv pip 必须 --no-cache-dir＋TMP 重定向，
  详见 RUNBOOK 与 knowledge/runbooks/2026-10-08-windows-dev-setup.md）。
- 决策 0021 等旧 knowledge 只在 Linux 旧机，未随仓库走，待补齐。

## Next Actions
1. 用户换凭据后 `git -C cropland push`（两个提交在本地 main）。
2. QGIS 实机点选冒烟：profile plugins 里 `mklink /J cropland_delineator
   <工作区>\cropland\qgis-plugin\cropland_delineator`，控制台设
   QSettings nn_dir 后开「🖱 点选」实测锁面。
3. 朋友实机验证 v0.10.1（碎块/缝隙/卡顿）。
4. 旧遗留 F3/F6 未动。

## Key Paths
- 插件源码 `qgis-plugin/cropland_delineator/`；测试入口 `tests/win_headless.py`
- nn 推理环境 `nn/.venv`＋`nn/ckpt/sam_vit_b_01ec64.pth`；大轮子暂存 `..\..\..\.wheels\`
- 发版 `tools/publish.sh`（需 gh auth；本机无 gh）
