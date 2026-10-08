# Windows 开发机环境排障（2026-10-07/08，huahua 主机）
Updated: 2026-10-08

## 症状链（全因同源）
1. `nn/setup.bat` 里 pip 装torch：阿里云/官方两个索引都报 "versions: none"，随后挂死。
2. faulthandler 抓栈：挂死点在 `pip/_internal/network/cache.py _write → tempfile.NamedTemporaryFile`
   （往 AppData\Local\pip\cache 写 HTTP 缓存时）。
3. 直接复测：venv 的 python 写 %TEMP%/pip-cache 报 EACCES 或挂死；写工作区正常。
   同一用户下 cmd / pwsh(.NET) / E:\Program Files\Python311 写这些目录全秒过。
   ACL 无 DENY 项（huahua 是 Full Control；目录里有 CodexSandboxUsers 遗迹 ACE）。

## 结论
本机存在按**进程映像位置**过滤的组件：映像在用户目录下
（Documents 工作区里的 venv python.exe，或 AppData\Local\Python 的 store 版）
→ 写 AppData\Local\* 被拒/挂；映像在 Program Files/System32 → 不受限。
未深挖是哪个驱动（疑与 Codex 沙箱/Defender 有关），绕开方案已足够稳。

## 绕开方案（建 venv 装 pip 包的标准姿势）
- 解释器选可信位置：`py -3.11 -m venv nn/.venv`（E 盘正式安装；torch 2.6 完全支持 3.11）。
- pip 永远带 `--no-cache-dir`（或 PIP_NO_CACHE_DIR=1），并把 `$env:TMP/$env:TEMP`
  指到工作区内目录（pip 解包临时文件也躲开 AppData）。
- store 版 pythoncore-3.12（AppData\Local\Python\pythoncore-3.12-64）在本机**不要**用来建 venv。

## 下载源实测（2026-10-08）
- aliyun pytorch-wheels 的索引页 pip 认不出（"No matching distribution"，1.3s 秒败，
  但文件直链 curl 可下）；且该 CDN 对 torch 大轮子限速 ~0.2MB/s。
- download.pytorch.org 直连实测 4MB/s —— 大轮子直接走官方 + `curl -C -` 断点续传，
  下完本地 `pip install <whl>`。
- SAM 权重 dl.fbaipublicfiles.com 直连可下（375MB，sha256 见 setup.bat）。

## QGIS Windows 无头测试两个坑
1. `bin\o4w_env.bat` 串调 `etc\ini\python3.bat`，其中无条件 `SET PYTHONPATH=` 清空
   ——给 python-qgis.bat 传 PYTHONPATH 无效，走 tests/win_headless.py（sys.path 注入
   + 每套独立子进程，防 sys.exit 带走后续套件）。
2. 杀 pwsh 后台任务不会杀 python 子进程（job_kill 只到包装层），会留僵尸
   python 挂着句柄——排障时记得 Get-Process python 核对。

## 本机环境快照
- QGIS 4.2.2：D:\Program Files\QGIS 4.2.2（另有 3.40.5/3.44.12 旧版）。
- GPU：RTX 4060 Laptop 8GB（cu124）。Python：py 启动器下 2.7~3.14 多版本。
- 旧副本 D:\software\cropland（v0.8.9 + 一个本地提交 dd057fd，其 sam_click 自愈
  修复已随 v0.9 线并入主线）；用户 QGIS 会话可能开着它 → %TEMP%\osm_道路.gpkg
  可能长期被锁（save_roads 已有锁退让，见 2026-10-08-osm-roads-windows 修复）。
