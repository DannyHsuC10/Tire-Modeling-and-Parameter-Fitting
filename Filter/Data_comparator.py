"""
資料關係
magic_formula/
├─ filter/
│  └─ Data_comparator.py   ← 這個檔案
├─ data/
│  └─ csv/B2356run23.csv← 要載入的資料
│  └─ csv/B2356run57.csv← 要載入的資料
├─ data/
│  └─ Filtered_data/B2356run23_processed.csv← 存檔資料
│  └─ Filtered_data/B2356run23_processed.csv← 存檔資料
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

class DataComparator:
    def __init__(self, raw_filename: str, cleaned_filename: str, save_fig: bool = False, fig_dir: str = "Figures"):
        # 基於這個檔案的相對路徑
        base_dir = Path(__file__).resolve().parent.parent  # magic_formula/
        self.raw_path = base_dir / "data" / "csv" / raw_filename
        self.cleaned_path = base_dir / "data" / "Filtered_data" / cleaned_filename

        self.save_fig = save_fig
        self.fig_dir = base_dir / fig_dir
        if save_fig:
            self.fig_dir.mkdir(exist_ok=True)

        # 讀取資料
        self.df_raw = pd.read_csv(self.raw_path)
        self.df_cleaned = pd.read_csv(self.cleaned_path)

        # 找出共同欄位
        self.common_columns = list(set(self.df_raw.columns) & set(self.df_cleaned.columns))
        self.common_columns.sort()

    def compare_columns(self):
        for col in self.common_columns:
            fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
            
            axes[0].plot(self.df_raw[col], marker='o', color='tab:blue')
            axes[0].set_title(f"{col} - Raw")
            axes[0].set_xlabel("Index")
            
            axes[1].plot(self.df_cleaned[col], marker='o', color='tab:orange')
            axes[1].set_title(f"{col} - Cleaned")
            axes[1].set_xlabel("Index")
            
            plt.suptitle(f"Comparison for column: {col}", fontsize=14)
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            
            if self.save_fig:
                fig_path = self.fig_dir / f"{col}_comparison.png"
                plt.savefig(fig_path)
                plt.close(fig)
                print(f"Saved figure: {fig_path}")
            else:
                plt.show()


if __name__ == "__main__":

    comparator = DataComparator(
        raw_filename="B2356run23.csv",# 原先資料檔案
        cleaned_filename="B2356run23_processed234.csv",# 處理後資料檔案
        save_fig=True# 除存到magic_formula\Figures
    )
    comparator.compare_columns()
