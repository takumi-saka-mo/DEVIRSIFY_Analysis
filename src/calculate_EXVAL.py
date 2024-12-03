import pandas as pd
import yfinance as yf
import math

class DiversifyApproach:
    def __init__(self, ticker, specialized_tickers, data):
        self.ticker = ticker
        self.specialized_tickers = specialized_tickers
        self.data = data
        self.segment_data = None
        self.value = None

        self.RED = "\033[91m"
        self.GREEN = "\033[92m"
        self.YELLOW = "\033[93m"
        self.RESET = "\033[0m"

    def calculate_value(self):
        """対象企業の企業価値を算出"""
        try:
            stock = yf.Ticker(self.ticker)
            balance_sheet = stock.balance_sheet
            total_debt = balance_sheet.loc["Total Debt"].iloc[0] if "Total Debt" in balance_sheet.index else 0

            market_cap = stock.info.get("marketCap", 0)  # 時価総額が見つからなかった場合, 0を返す
            self.value = market_cap + total_debt  # 企業価値の算出
            return self.value
        except KeyError:
            print(f"{self.YELLOW}Error: 証券コードが無効のため None を変えす {self.ticker}.{self.RESET}")
            return None
        except Exception as e:
            print(f"{self.RED}Error : 期待しない企業価値が算出されたため None を返す {self.ticker}: {e}{self.RESET}")
            return None

    def get_financial_data(self):
        """対象企業の財務データを取得"""
        try:
            stock = yf.Ticker(self.ticker)
            balance_sheet = stock.balance_sheet
            income_statement = stock.income_stmt

            total_revenue = income_statement.loc["Total Revenue"].iloc[0] if "Total Revenue" in income_statement.index else 0
            total_assets = balance_sheet.loc["Total Assets"].iloc[0] if "Total Assets" in balance_sheet.index else 0
            operating_income = income_statement.loc["Operating Income"].iloc[0] * 1000 if "Operating Income" in income_statement.index else 0

            print(f"証券コード : {self.ticker}")
            print(f"\n総資産 : {total_assets} \n売上高 : {total_revenue} \n営業利益 : {operating_income}")
        except Exception as e:
            print(f"{self.RED}Error retrieving financial data for {self.ticker}: {e}{self.RESET}")

    def calculate_specialized_value(self, specialized_tickers):
        """関連企業の中央値を計算"""
        try:
            data = []
            for ticker in specialized_tickers:
                company = yf.Ticker(ticker)
                try:
                    market_cap = company.info.get("marketCap", 0)  # 時価総額
                    balance_sheet = company.balance_sheet
                    total_revenue = company.financials.loc["Total Revenue"].iloc[0] if "Total Revenue" in company.financials.index else 0

                    data.append({"ticker": ticker, "Market Cap": market_cap, "Revenue": total_revenue})
                except Exception as e:
                    print(f"{self.YELLOW}Error processing {ticker}: {e}{self.RESET}")

            if data:
                df = pd.DataFrame(data)
                df["Market Cap / Revenue"] = df["Market Cap"] / df["Revenue"]
                median_ratio = df["Market Cap / Revenue"].median()
                return median_ratio
            else:
                print(f"{self.RED}No valid data for specialized tickers.{self.RESET}")
                return 0
        except Exception as e:
            print(f"{self.RED}Error calculating specialized value: {e}{self.RESET}")
            return 0

    def calculate_exval(self, seg_list):
        """EXVALを算出"""
        try:
            total_iv = 0
            for i, seg_value in enumerate(seg_list):
                ratio = self.calculate_specialized_value(self.specialized_tickers[i])
                total_iv += seg_value * ratio

            if self.value is None:
                self.value = self.calculate_value()

            if total_iv > 0:
                exval = math.log(self.value / total_iv)
                return exval
            else:
                print(f"{self.RED}Total_IV is 0 or negative. Cannot calculate EXVAL.{self.RESET}")
                return None
        except Exception as e:
            print(f"{self.RED}Error calculating EXVAL: {e}{self.RESET}")
            return None
        

# モジュールとして使用可能にする
if __name__ == "__main__":

    # テスト用データ
    file = "./csv/APPL_category.csv"
    data = pd.read_csv(file, encoding="UTF-8").set_index("Category")
    data["Devices"] = data["iPhone"] + data["Mac"] + data["iPad"] + data["Wearables, Home and Accessories"]
    data = data.drop(columns=["iPhone", "Mac", "iPad", "Wearables, Home and Accessories"])

    # セグメントごとの売上
    seg1_value = data["Services"].iloc[0] * 1e6
    seg2_value = data["Devices"].iloc[0] * 1e6
    seg_list = [seg1_value, seg2_value]

    # 専門企業リスト
    services_companies = ["NFLX", "DBX", "SPOT"]
    devices_companies = ["HPQ", "DELL", "LNVGY"]
    specialized_tickers = [services_companies, devices_companies]

    # クラスインスタンス作成
    div_approach = DiversifyApproach(
        ticker="AAPL",
        specialized_tickers=specialized_tickers,
        data=data
    )

    # 企業価値の計算
    value = div_approach.calculate_value()
    print(f"企業価値: {value}")

    # EXVAL（超過価値）の計算
    exval = div_approach.calculate_exval(seg_list)
    print(f"超過価値 (EXVAL): {exval}")
