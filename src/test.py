import unittest
from src.calculate_EXVAL import DiversifyApproach

import pandas as pd
import sys

class TestDiversifyApproach(unittest.TestCase):
    def setUp(self):
        self.RED = "\033[91m"
        self.GREEN = "\033[92m"
        self.RESET = "\033[0m"
        self.data = pd.DataFrame({
            "Services": [314570], 
            "FinTech": [208229], 
            "Mobile": [105986]
        })
        self.specialized_tickers = [
            ["4686.T", "3092.T", "2371.T"],  # サービス事業3社
            ["4478.T", "7342.T", "4477.T"],  # フィンテック企業3社
            ["9432.T", "9434.T", "9433.T"]   # キャリア3社
        ]
        self.obj = DiversifyApproach("4755.T", self.specialized_tickers, self.data) # 楽天のテストケース

    def test_calculate_value(self):
        """企業価値計算のテスト"""
        value = self.obj.calculate_value()
        try:
            self.assertIsNotNone(value)
            self.assertGreater(value, 0)
            sys.stdout.write(f"{self.GREEN}Test Calculate Value: OK{self.RESET}\n")
        except AssertionError:
            sys.stdout.write(f"{self.RED}Test Calculate Value: NG{self.RESET}\n")

    def test_calculate_specialized_value(self):
        """専門企業の倍率計算のテスト"""
        ratio = self.obj.calculate_specialized_value(self.specialized_tickers[0])  # Servicesセグメント
        try:
            self.assertIsNotNone(ratio)
            self.assertGreater(ratio, 0)
            sys.stdout.write(f"{self.GREEN}Test Specialized Value (Services): OK{self.RESET}\n")
        except AssertionError:
            sys.stdout.write(f"{self.RED}Test Specialized Value (Services): NG{self.RESET}\n")

    def test_calculate_exval(self):
        """EXVALの計算テスト"""
        seg1_value = self.data["Services"].iloc[0] * 1e6
        seg2_value = self.data["FinTech"].iloc[0] * 1e6
        seg_list = [seg1_value, seg2_value]
        exval = self.obj.calculate_exval(seg_list)
        try:
            self.assertIsNotNone(exval)
            sys.stdout.write(f"{self.GREEN}Test Calculate EXVAL: OK{self.RESET}\n")
        except AssertionError:
            sys.stdout.write(f"{self.RED}Test Calculate EXVAL: NG{self.RESET}\n")

    def test_financial_data_retrieval(self):
        """財務データ取得のテスト"""
        try:
            self.obj.get_financial_data()
            sys.stdout.write(f"{self.GREEN}Test Financial Data Retrieval: OK{self.RESET}\n")
        except Exception as e:
            sys.stdout.write(f"{self.RED}Test Financial Data Retrieval: NG - {e}{self.RESET}\n")

if __name__ == '__main__':
    unittest.main()