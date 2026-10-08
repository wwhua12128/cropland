# Windows 无头回归入口：绕开 QGIS python3.bat 清空 PYTHONPATH 的问题。
# QGIS 的 o4w_env 会串调 etc\ini\python3.bat，其中 `SET PYTHONPATH=` 无条件清空，
# 所以靠环境变量传插件路径在 Windows 上无效；本脚本直接往 sys.path 注入。
# 每个测试用独立子进程跑：测试末尾的 sys.exit/QApp 清理不会波及后续套件。
# 用法（任意 cwd）：
#   & "D:\Program Files\QGIS 4.2.2\bin\python-qgis.bat" tests\win_headless.py test_ledger.py [更多...]
import os
import subprocess
import sys
from pathlib import Path

# tests/ -> cropland_delineator -> qgis-plugin（插件包的导入根）
plugin_root = str(Path(__file__).resolve().parents[2])
env = dict(os.environ)
parts = [p for p in env.get("PYTHONPATH", "").split(os.pathsep) if p]
if plugin_root not in parts:
    parts.insert(0, plugin_root)
env["PYTHONPATH"] = os.pathsep.join(parts)
env.setdefault("QT_QPA_PLATFORM", "offscreen")

failed = []
for name in sys.argv[1:]:
    print(f"===== {name} =====", flush=True)
    r = subprocess.run([sys.executable, str(Path(__file__).with_name(name))], env=env)
    if r.returncode != 0:
        failed.append(name)
if failed:
    print(f"FAILED: {', '.join(failed)}")
    sys.exit(1)
print("ALL SUITES PASSED")
