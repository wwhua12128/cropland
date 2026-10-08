# STATUS — Cropland Delineator
Updated: 2026-10-07

## Current Goal
在 Windows 开发机上恢复完整开发测试能力（对齐 v0.10.1），等朋友实机反馈点选锁面/密格修复效果。

## Just Finished
- v0.10.0 点选锁面（挖除锁点地块＋影像窗同步裁剪＋空隙补画贴边零缝零叠＋误点拦截，`3` 键开关）。
- v0.10.1 密格卡死修复（空间索引框选＋unaryUnion 一次差集＋点哪补哪 1051ms→28ms，拦截弹消息条）。
- tests/ 六套回归收编进仓库（b76f69a）＋ README 迁移清单。
- 2026-10-07 Windows 机克隆仓库成功；QGIS 4.2.2 无头栈打通（5 套非 nn 测试通过）；SAM 环境重建（torch cu124 + 权重 sha256 已验）。

## Open Problems
- 本机有过滤器按"进程映像在用户目录下"拦截 AppData 写入：工作区 venv 里的 pip 会挂死/EACCES，必须 `--no-cache-dir` ＋ TMP/TEMP 重定向到工作区（详见 RUNBOOK 与 knowledge/runbooks/2026-10-07-windows-dev-setup.md）。
- QGIS Windows 启动链 etc\ini\python3.bat 无条件 `SET PYTHONPATH=` 清空环境变量，测试入口用 tests/win_headless.py 注入 sys.path 解决。
- 决策 0021（点选锁面设计）等旧 knowledge 文件只在 Linux 旧机 `.agents/memory/`，未随仓库走，待补齐。
- 旧遗留 F3/F6 未动。

## Next Actions
1. SAM venv 装完（py3.11＋torch 2.6.0 cu124＋segment-anything）→ `test_clickseg.py` 全绿 → 提交记忆四件套＋win_headless.py＋gitignore 放行并推送。
2. 朋友实机验证 v0.10.1：碎块/缝隙/卡顿是否消失。
3. 处理旧遗留 F3/F6（内容见 Linux 旧机记忆或 git log）。

## Key Paths
- 插件源码 `qgis-plugin/cropland_delineator/`；测试 `tests/`（Windows 入口 `tests/win_headless.py`）
- nn 推理环境 `nn/.venv`＋`nn/ckpt/sam_vit_b_01ec64.pth`（375MB，sha256 已验）
- 发版 `tools/publish.sh`（需 gh auth login；本机无 gh 但 git 凭据可用，可推拉 GitHub）
