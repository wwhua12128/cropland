# RUNBOOK — 常用命令与排障
Updated: 2026-10-07

## 无头回归测试
Windows（本仓库入口，自动注入 sys.path、每套独立子进程）：
```powershell
cd qgis-plugin/cropland_delineator
& "D:\Program Files\QGIS 4.2.2\bin\python-qgis.bat" tests\win_headless.py test_ledger.py test_lasso.py test_clickseg.py ...
```
Linux：
```bash
QT_QPA_PLATFORM=offscreen PYTHONPATH=/usr/share/qgis/python:../../ python3 tests/test_ledger.py
```
注意：Windows 下直接给 python-qgis.bat 传 PYTHONPATH 无效（o4w_env 串调
etc\ini\python3.bat 无条件 `SET PYTHONPATH=` 清空）——必须走 win_headless.py。

## SAM 推理环境（nn/.venv + nn/ckpt）
标准：`nn/setup.bat`（py -3.12；自动判 GPU→cu124/CPU；权重 358MB 断点续传+sha256）。
本机（huahua）已验证可用且更快的替代流程：
1. `py -3.11 -m venv nn/.venv`（3.12 是 store 映像被本机过滤器拦，见下）
2. 轮子直下再本地装（阿里云 pytorch-wheels 的索引页 pip 认不出，但文件直链没问题）：
   `curl.exe -L -o torch.whl "https://mirrors.aliyun.com/pytorch-wheels/cu124/torch-2.6.0%2Bcu124-cp311-cp311-win_amd64.whl"`（torchvision 同理）
3. `nn/.venv/Scripts/python.exe -m pip install --no-cache-dir <两个whl> segment-anything numpy`
   —— **必须 --no-cache-dir**，且 TMP/TEMP 重定向到工作区（`.tmp`），原因见过滤器条目
4. 权重：`curl.exe -L -C - -o nn/ckpt/sam_vit_b_01ec64.pth https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth`
   （sha256 ec2df627…c912，setup.bat 内有完整校验命令）

## 本机过滤器（映像在用户目录下的进程禁写 AppData）
症状：venv pip 拉索引"versions: none"后挂死在 cachecontrol 写缓存；直接 open() 报 EACCES。
规律：映像在 Documents 工作区（venv python.exe）→ 写 AppData\Local 任何处被拒/挂；
写工作区本身正常。cmd / Program Files 下的 exe（含 E:\Python311）不受影响。
绕开：pip 永远 `--no-cache-dir`；`$env:TMP/$env:TEMP` 指到工作区；解释器用 E 盘正式安装。

## pwsh 写文件纪律（2026-10-08 实机事故）
`Set-Content -Encoding utf8` 会带 BOM（PS5.1），QGIS 的 metadata.txt 遇 BOM 直接
"元数据读取错误 → 插件破损"（e47548f 修复）；`-Encoding ascii` 写中文全变问号
（污染提交标题）。**仓库内任何文件与 git 提交信息一律用 write/edit 工具**（UTF-8
无 BOM）；pwsh 兜底 `[IO.File]::WriteAllText($p,$s,[Text.UTF8Encoding]::new($false))`。
自查：读文件头 3 字节是否为 239,187,191。
同一坑的反面（2026-10-13）：PS 5.1 **读** UTF-8 无 BOM 的 `.ps1` 时按 ANSI 解码，
带中文的临时脚本会直接 ParserError → 临时 `.ps1` 一律写纯 ASCII 内容（日志文案用
英文），或用 pwsh 7 执行。

## QGIS 实跑开发版
```bat
mklink /J "%AppData%\QGIS\QGIS4\profiles\default\python\plugins\cropland_delineator" C:\...\cropland\qgis-plugin\cropland_delineator
```
本机现状（2026-10-13）：已联接至工作区主线副本；插件设置存在 `QGIS4.ini` 的
`[cropland_delineator]` 段（`nn_dir=D:\software\cropland\nn`，实测 torch 2.6.0+cu124
/CUDA 可用）；没有 `nn_dir` 时回落到相对路径 `../../nn`。
改代码后**重启 QGIS 即生效**（无需重装）；metadata.txt 改动尤其要重启才重读。

**卸载后装回（2026-10-13 实机）**：在插件管理器点"卸载"会同时删掉联接目录和
`QGIS4.ini [PythonPlugins]` 里的 `cropland_delineator` 键（`[cropland_delineator]`
段的设置保留）。手工装回两步：
1) 重建联接 `New-Item -ItemType Junction -Path "...\plugins\cropland_delineator" -Target <工作区副本>`；
2) 给 `QGIS4.ini` 的 `[PythonPlugins]` 段补一行 `cropland_delineator=true`。
   **QGIS 开着时改 ini 会被它退出时覆盖**，必须先关 QGIS；改写走
   `[IO.File]::WriteAllText($p,$s,(New-Object Text.UTF8Encoding($false)))` 保无 BOM，
   并先备份 `QGIS4.ini.bak-<时间戳>`。
验收：`python-qgis.bat -c "import cropland_delineator"` 能打印 `classFactory` 即会被加载；
在 GUI 里看 插件 → 管理插件 → 已安装 是否勾上。
雷区：`cropland_delineator_v089_bak` 是 0.10.1 的实体副本、插件显示名与主线**完全相同**，
留在 plugins 目录里会与主线撞名（QGIS 记成 `cropland_delineator-0`，两条工具栏打架），
2026-10-13 已移出扫描路径到 `profiles\default\python\_archive_plugins\`。

## 发版
`bash tools/publish.sh`（改 metadata.txt 版本后；需 gh auth login，本机暂无 gh）。
