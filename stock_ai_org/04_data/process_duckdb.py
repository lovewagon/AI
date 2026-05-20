import os
import numpy as np
import pandas as pd

class DataPipeline:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.processed_dir = os.path.join(base_dir, "04_data", "processed")
        os.makedirs(self.processed_dir, exist_ok=True)

    def run_feature_engineering(self):
        print("[DataPipeline] Generating features...")
        dates = pd.date_range(start="2026-01-01", periods=100, freq="D")
        df = pd.DataFrame({
            "date": dates.strftime("%Y-%m-%d"), 
            "close_price": np.random.randn(100),
            "volume": np.random.randint(1000, 5000, 100)
        })
        target_tsv = os.path.join(self.processed_dir, "features.tsv")
        try:
            df.to_csv(target_tsv, sep="\t", index=False)
            print(f"[Success] TSV形式で保存完了: {target_tsv}")
            return True
        except Exception as e: print(e); return False

if __name__ == "__main__":
    pipeline = DataPipeline("C:\\Users\\User\\Desktop\\AI\\stock_ai_org")
    pipeline.run_feature_engineering()