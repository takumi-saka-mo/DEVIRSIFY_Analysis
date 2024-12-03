# DIVERSIFY_Analysis: 超過価値（EXVAL）

企業のセグメント別売上データをもとに超過価値（EXVAL）を計算するモジュールを作成.
Yahoo Finance を使用し, 企業価値や専門企業の倍率, 対象企業の超過価値算出する.



## 超過価値アプローチモデルについて

Berger/Ofek[1995]の分析モデル


$$ I \left(V \right) = \sum_{i=1}^n AI_i \times \left(Ind_i \left(\frac{V}{AI} \right)_{mf} \right) $$


$$ EXVAL = ln \left( \frac{V}{I(V)} \right)$$

- I(V) : 専業企業データより, 多角化企業の各事業のValue合計額
- AI_i : 多角化企業の事業iの会計数値(総資産, 売上高, 利益)
- Ind_i(V/AI_i)_mf : 産業iに属する専業企業のValueと会計数値の比率の中央値
- EXVAL : 多角化企業の超過企業価値
Value : 株式時価総額 + 薄価負債


## Dir Structure

DEVIRSIFY_Analysis/
├── README.md
├── data/                 # データセット(csvファイル)
│   ├── RAKUTEN.csv
│   ├── template.csv
│   └── etc.
├── notebooks/            # Notebookファイル
│   └── Diversify.ipynb
├── src/
│   ├── init.py
│   ├── calculate_EXVAL.py # 超過価値算出クラス
│   └── test.py            # テストスクリプト

## Usage

1. Requirements
```bash
pip install pandas yfinance
```

2. クラス calculate_EXVAL の用法
(楽天の企業超過価値を算出する場合)
```python
from src.calculate_EXVAL import DiversifyApproach
import pandas as pd

# セグメント別売上データの準備
data = pd.DataFrame({
    "Services": [314570], 
    "FinTech": [208229], 
    "Mobile": [105986]
}) # HPより引用

# 専門企業リストの定義
services_companies = ["4686.T", "3092.T", "2371.T"]  # サービス領域
fintech_companies = ["4478.T", "7342.T", "4477.T"]   # フィンテック領域
mobile_companies = ["9432.T", "9434.T", "9433.T"]    # モバイル領域

specialized_tickers = [services_companies, fintech_companies, mobile_companies]

# DiversifyApproachクラスのインスタンス化
div_approach = DiversifyApproach(
    ticker = "4755.T",  # 楽天
    specialized_tickers = specialized_tickers,
    data = data
)

# 企業価値の計算
value = div_approach.calculate_value()
print(f"企業価値: {value}")

# EXVALの計算
seg_list = [data["Services"].iloc[0] * 1e6, data["FinTech"].iloc[0] * 1e6]
exval = div_approach.calculate_exval(seg_list)
print(f"超過価値 (EXVAL): {exval}")
```

## Data
data/フォルダ内に保存するファイルは次のような形式にする必要がある.


**template.csvを参照**
```csv
Category ,seg1  ,seg2  ,seg3  ,seg4  ,seg5   ,seg6   ,seg7   ,seg8   ,seg9   ,seg10
Sales    ,29984 ,26694 ,37005 ,96169 ,122764 ,157502 ,192239 ,226977 ,261714 ,296452
```



