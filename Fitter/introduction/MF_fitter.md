# MF_fitter 
[檔案位置](../MF_fitter.py)
## 1. 擬合概念說明
MF_fitter 的核心是利用 **非線性最小平方法 (Nonlinear Least Squares)** 來進行參數擬合。其基本思想是最小化「模型預測值」與「實際量測值」之間的殘差平方和。

$$
\min_{\mathbf{x}} \; \sum_{i=1}^{n} \left( F_{\text{pred},i}(\mathbf{x}) - F_{\text{meas},i} \right)^2
$$

其中：
- $F_{\text{pred},i}(\mathbf{x})$：模型在第 $i$ 個輸入下的預測值  
- $F_{\text{meas},i}$：量測值  
- $\mathbf{x}$：待擬合的參數向量  

## 2. 殘差函數 (Residual Function)
殘差函數定義為：

$$
r_i(\mathbf{x}) = F_{\text{pred},i}(\mathbf{x}) - F_{\text{meas},i}
$$

整體殘差向量為：

$$
\mathbf{r}(\mathbf{x}) = 
\begin{bmatrix}
r_1(\mathbf{x}) \\
r_2(\mathbf{x}) \\
\vdots \\
r_n(\mathbf{x})
\end{bmatrix}
$$

最小化問題即轉化為：

$$
\min_{\mathbf{x}} \; \|\mathbf{r}(\mathbf{x})\|^2
$$

## 3. 參數打包與解包
在擬合過程中，僅部分參數會被優化。  
- **打包 (pack)**：將 $active\_keys$ 對應的參數組合成向量 $\mathbf{x}$，並設定上下限 $lb, ub$。  
- **解包 (unpack)**：將優化後的 $\mathbf{x}$ 更新回完整的 $stage\_params$ 字典。

## 4. 邊界條件 (Bounds)
為了避免不合理的解，優化器會設定參數的上下限：

$$
lb_j \leq x_j \leq ub_j
$$

其中：
- $lb_j$：第 $j$ 個參數的下限  
- $ub_j$：第 $j$ 個參數的上限  

## 5. 使用的優化方法
MF_fitter 採用 **scipy.optimize.least_squares**，其主要特點包括：
- 方法：Trust Region Reflective (TRF)  
- 損失函數：Soft L1 損失，降低異常值影響  

$$
\text{loss}(r) = 2 \left( \sqrt{1 + \frac{r^2}{2}} - 1 \right)
$$

此損失函數在 $r$ 很大時近似於線性，能減少離群值對結果的影響。

## 6. 模型輸入與輸出
模型輸入包含：
- $FZ$：垂直載荷  
- $SA$：舵角 (Slip Angle)  
- $SL$：滑移率 (Slip Ratio)  
- $IA$：外傾角 (Inclination Angle)  
- $pressure$：胎壓  
- $Ro$：輪胎半徑  
- $V$：速度  

模型輸出依據選擇的 $out$ 類型 (Fx, Fy, Mx, Mz, RRT)，對應不同的力或力矩。

## 7. 擬合流程總結
1. **初始化**：設定待擬合參數及上下限  
2. **打包**：將參數轉換為向量形式  
3. **殘差計算**：比較模型預測與量測值  
4. **優化**：利用最小平方法更新參數  
5. **解包**：將最佳解更新回完整參數字典  

最終得到的參數組合能使模型在給定輸入下，與量測數據的誤差最小化。