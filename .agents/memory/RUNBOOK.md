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

## QGIS 实跑开发版
```bat
mklink /J "%AppData%\QGIS\QGIS\profiles\default\python\plugins\cropland_delineator" C:\...\cropland\qgis-plugin\cropland_delineator
```

## 发版
`bash tools/publish.sh`（改 metadata.txt 版本后；需 gh auth login，本机暂无 gh）。
