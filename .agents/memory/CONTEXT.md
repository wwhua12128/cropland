# CONTEXT — 稳定事实
Updated: 2026-10-07

## 项目是什么
QGIS 4 插件「耕地标注工作台」：5m 卫星影像耕地逐格标注（减法勾绘）。
渔网格驱动，整格建底板后用笔刷做减法/补画，最终耕地 = 底板＋补块 − 扣除。
全程操作台账 JSONL 可重放、可单步删除。朋友侧经 plugins.xml 自动升级。

## 模块地图（qgis-plugin/cropland_delineator/）
- annotate.py：标注工作台主控 AnnotationController（格导航/笔刷/收尾 QA）
- clickseg.py：SAM 点选分割客户端。find_nn_dir() 查找顺序：环境变量
  CROPLAND_NN_DIR → QSettings `cropland_delineator/nn_dir` → 开发布局 `../../nn`；
  service_argv() 拼 venv python ＋ sam_click.py 启动参数（Windows 认 .venv/Scripts/python.exe）
- 磁力走线（切分/道路/补画）：A* 沿影像梯度，可选 NN 边界证据增强
- 台账：几何＋参数进 JSONL，回退任意步/删单步/改道路宽度重放；🥞 分层视图拆底板/补块/扣除

## SAM worker 协议（nn/sam_click.py）
stdio JSON 行协议：启动后回 `{"ok":true,"event":"ready","device":...}`；
`embed`（影像窗 npy → 编码缓存）→ `predict`（正/负点 → 掩码）。测试用 stub_worker 冒充。

## 点选锁面（v0.10.0 起，决策 0021）
掩码不是无约束识别：挖除锁点中地块（影像窗同步裁过去），掩码裁进地块/空隙，
补画只落空隙且贴边零缝零叠；误点拦截；`3` 键开关锁面。
v0.10.1 密格性能：空间索引框选＋unaryUnion 一次差集＋点哪补哪（3000 地块 1051ms→28ms）。

## 测试（tests/，无头 offscreen，Fake canvas/iface）
test_ledger 17 组 / test_lasso 17 / test_clickseg 14（含锁面/密格回归，T1 要真实 nn 布局）
/ test_snap 6 / test_workbench_bae 12 / test_qa。

## 版本与发版
metadata.txt 版本号 → `bash tools/publish.sh`（gh auth；产 dist/ 并推 release，plugins.xml 供给朋友升级）。
版本史：v0.10.0 锁面 → v0.10.1 密格修复（均 2026-10 上旬，朋友实测卡死驱动）。

## 遗留
F3/F6 旧遗留未处理（详情在 Linux 旧机记忆/会话史）。
