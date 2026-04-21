# Tire-Modeling-and-Parameter-Fitting

## 輪胎模型包 (`model_for_import`)
在資料夾`model_for_import`中，這裡面有matlab與python兩個版本，可以單純下載這兩個資料夾取得輪胎模型包，按照範例檔案呼叫api接口就可以快速使用。也可以直接用DEMO修改。

## 輪胎分析工具(`other`)
為了方便進行設計與分析另外有一些常用工具可以輪胎分析。

1. 輪胎性能比較 : 
1. 輪胎剛性擬和 : 
1. 摩擦係數解出 :


## 擬和器架構與使用方法
[擬合主控腳本](/introduction/fitting.md) : 執行後馬上會進行所有程序，如果需要擬合其他內容，主要需要更新數據、檔名、路徑位址即可。原先檔案皆使用相對路徑，但並不公開原始資料權限，可以依照說明文件了解檔案位置。

* 擬合 : Fx或Fy
* 執行 : 資料處理>>輪胎模型>>擬合>>驗證>>出tir檔案
### 整體簡介
連接皆可以連接到對應的程式碼位置，這邊僅對資料夾進行大方向說明。
1. model_for_import : 核心輪胎模型包(70%情況只會用到這個)
1. other : 其他常用工具(輪胎分析用工具，車輛設計初期使用)
1. data : 所有數據資料，主要不公開詳細請見 [all data](data/introduction/all_data.md)
1. Figures : png圖片，因為關係數據內容不公開
1. Filebkp : 重要文件保護區(應該無法看到這個資料夾)
1. Filter : 過濾data資料>>給Fitter用
1. Fitter : 用Filter的資料擬合>>出數據給
1. matlab_bridge : matlab橋梁
1. model : 輪胎模型
1. model_matlab : matlab輪胎模型，可與上個模型搭配使用
1. introduction : md介紹文件
1. assets : css網頁設定
1. _layout : html網頁設定

### 1. 資料處理
* [all data](data/introduction/all_data.md) : 所有資料結構

* [mat to csv & excel](data/introduction/mat_to_excel_csv.md) 資料轉換器 : 處理資料轉換成excel和csv

### 2. 資料過濾
> 主要需要更動的檔案 : 
>1. [json檔](Filter/introduction/json.md)過濾條件 : 這裡是用來改清理資料的條件用的
>1. [filter](Filter/introduction/Filter.md) 過濾器 : 過濾資料並整理要用的東西。如果檔名和路徑有改這邊需要更新

* [資料比較圖](Figures/data_comparison.md) : 點下去就可以看，用[data comparator](Filter/introduction/data_comparator.md)可以更新資料，想看什麼自行調整。(但因為數據不外流沒有開放圖形資料，執行後會自動更新)
### 3. 輪胎模型
> 主要需要更動的檔案 : 
> 1. [MF 測試器](/introduction/MF_tester.md) : 可以方便看出不同輪胎參數、輸入輸出，進行比較和分析，用高度模組化的物件出圖。可以很快的了解模型趨勢。
* [MF圖形](/Figures/MF_plt.md) : 測試器出圖之後可以存檔到這邊。(但因為數據不外流沒有開放圖形資料，執行後會自動更新)
* [Magic formula模型](model/introduction/magic_formula_model.md) : 這是 pyhon 版本的模型可以進行 array>>array 的快速運算，可以運用numpy底層會用高度優化的 C 做連續記憶體運算，大幅度拉高CPU運算效能，因為magic formula中有大量三角函數運算不適合GPU分散運算，目前使用這個模型可以在 0.5~1 min內完成大量 data fitting。

* [Magic formula matlab 模型](model_matlab/introduction/magic_formula_matlab.md) : 這是學長的 matlab MF612模型，整個擬合與輪胎模型都是基於這個原始版本建立，擬合與計算的準確性是都有和這個模型比較。如果要也可以套用matlab 模型的API接口進行fitting，但這部分功能目前沒有建立。
### 4. 擬合
> 主要需要更動的檔案 :
> 1. [fitter 擬合器](/Fitter/introduction/MF_fitter.md) : 這是擬合器，實際上的擬合過程是fitting套用這個擬合器。本檔案中有個工具叫```MF_Universal_solver```，這個通用求解器可以快速方便的套用MF模型。
### 5. 輸出資料與驗證的小工具
* [csv >> tir](/introduction/csv_to_tir.md) : 轉檔案工具，主要最後import使用進行檔案轉換。
* [tir tester](/introduction/tir_tester.md) : tir檔案測試器，用實驗數據進行數據比對直接觀察差異。
* [matlab 橋梁](/matlab_bridge/introduction/matlab_bridge.md) : 為了方便用matlab進行測試建立的輸出通道，執行後會更改檔案內容不要直接移走檔案(用複製的)。

## 改進方向總結
### 簡單

* 輪胎模型統一與修改，其中輪胎模型因為我在進行其他設計時不斷更新，盡量讓整個輪胎模型變得更方便，所以產生很多個版本的模型，總之for import的模型一定是最完整好用的，如果可以的話可以統一一下，這會讓整個系統更方便。
* 過濾器 : 斜率過濾器需增加or邏輯提升通用性
* matlab資料轉換器 : 轉換器不夠防呆遇到資料結構複雜的會出錯
* 檔案路徑優化 : 檔案命名抽象化或路徑儲存文字檔自動更新，避免使用者改動程式

### 進階
* matlab模型 : 計算效率不足還需優化計算邏輯
* 多語言通道 : 目前python啟動mathwork的matlab引擎可以使用matlab模型，但版本更新後可以會被淘汰可能小有風險。比較大的問題是目前還未建立python優化計算後較高效的輪胎模型api接口還沒有想好怎麼讓matlab使用
* 主要擬合腳本 : 目前是各個自由度分開擬合，雖然目前資料處理方式讓分開擬合很方便，但還是需要一鍵執行的功能提升大量處理效率。

### 困難
* 資料過濾json : 要是有辦法自動根據數據進行判斷會極大幅度提升處理效率
* 擬和界線與初值 : 要是有辦法導入動態邊界條件進行擬合可以大幅提升效率也許還能提升準確性

### 極難(應該達不到的遠大目標)
* 更多擬和手法 : 加入基因演算法(極度精確模型)、spline擬合(簡單高速模型)、Neural Network(黑箱模型)
* 更多輪胎模型 : Gaussian Process Tire Model(機率模型)、刷子模型(純物理模型)