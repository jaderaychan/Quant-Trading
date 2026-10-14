# A股短线量化选股系统

[English](README.md) | **简体中文**

基于 akshare 日线数据，对 A 股个股进行短线技术面打分、候选筛选与历史回测的分层量化研究项目。

## 目录结构

```
量化分析/
├── data_layer/          # 数据层：行情抓取与本地落库
├── strategy_layer/      # 策略层：打分与信号逻辑
├── selection_layer/     # 选择层：全库扫描、候选排序
├── backtest_layer/      # 回测层：单只/批量回测
├── risk_layer/          # 风控层：待实现
├── database/            # SQLite 数据库（stock.db）
└── .vscode/             # 编辑器配置
```

## 环境依赖

- Python 3.11（conda 环境）
- `akshare`、`pandas`、`numpy`、`sqlalchemy`

## 数据准备

数据库为单文件 SQLite，表结构如下：

| 表名 | 内容 |
| --- | --- |
| `stock_price` | 全市场实时行情快照（含 `代码` 字段） |
| `kline_<code>` | 个股前复权日线，如 `kline_sz300368` |

执行顺序：

```bash
python data_layer/database_test.py         # 抓取全市场行情 → stock_price
python data_layer/download_all_history.py  # 遍历代码批量下载日线（约 0.2s/只）
python data_layer/show_tables.py           # 校验：列出库中所有表
```

## 策略说明

核心为 `strategy_layer/short_strategy.py` 中的 `short_score(data)`，输入单只股票的日线
DataFrame（需含 `close/high/low/volume`），输出 0–90 的整数评分；样本不足 30 根 K 线直接返回 0。

| 因子 | 判定条件 | 分值 |
| --- | --- | --- |
| 5 日涨幅 | 3%–12% / 12%–20% / >20% | +15 / +10 / −10 |
| 均线排列 | MA5 > MA10 > MA20 | +15 |
| 20 日乖离率 | 0–10% / >20% | +10 / −10 |
| 10 日回撤 | −8%–−2%（回踩）/ <−15% | +10 / −10 |
| 量比（对 20 日均量） | 1.3–2.5（温和放量）/ >4（巨量） | +20 / −15 |
| K 线强度 | 收盘处于当日振幅上 25% / 下 25% | +15 / −5 |
| RSI(14) | 45–70 / >80 | +10 / −10 |

评分越高代表短线技术形态越健康；`selection_layer/stock_selector.py` 对库中全部
`kline_*` 表逐一打分并按分数降序输出前 20 只。

## 回测说明

- 规则：评分 ≥ 80 于当日收盘价买入，持有 5 个交易日后收盘卖出；信号未触发则逐日顺延。
- 资金：初始 10000 元，满仓复利滚动，**未计手续费、印花税与滑点**。
- 指标：最终资金、累计收益率、交易次数、胜率。
- 脚本：`backtest_layer/backtest.py`（单只，参数写在文件头部）；
  `backtest_layer/all_stock_backtest.py`（批量，当前仅扫描前 20 张表，需按需放开）。

```bash
python backtest_layer/backtest.py
python backtest_layer/all_stock_backtest.py
```

## 已知限制

1. `risk_layer/risk_control.py` 为空，仓位与止损管理尚未实现。
2. 数据库绝对路径在多个脚本中硬编码，迁移目录后需同步修改；建议后续收敛到统一配置文件。
3. 回测为逐笔独立计算，未做资金占用与并发持仓约束。
4. `data_layer/ma_strategy.py` 为早期均线趋势实验脚本，与当前打分体系无关。

## 免责声明

本项目仅用于量化方法研究与代码练习，所有评分与回测结果不构成任何投资建议。
