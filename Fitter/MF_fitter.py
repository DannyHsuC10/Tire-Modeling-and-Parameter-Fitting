# MF_fitter
from model._common import CalculationInput
from model.Fx_models import MF612_Fx
from model.Fy_models import MF612_Fy
from model.Mx_models import MF612_Mx
from model.Mz_models import MF612_Mz
from model.RRT_models import MF612_RRT_MF
from scipy.optimize import least_squares
import numpy as np

def MF_Universal_solver(out,MF):# 通用求解器選擇
    if out =="FX":
        result = MF612_Fx.calculate(MF)
    if out =="FY":
        result = MF612_Fy.calculate(MF)
    if out =="MZ":
        result = MF612_Mz.calculate(MF)
    if out =="MX":
        result = MF612_Mx.calculate(MF)
    if out =="RRT":
        result = MF612_RRT_MF.calculate(MF)
    
    # 純量與向量輸出兼容：
    '''
    - 若為 0 維或單一元素陣列，回傳純標量 (item)
    - 若為一般 1 維/多維陣列，直接回傳 ndarray
    '''
    if isinstance(result, np.ndarray):
        if result.ndim == 0 or result.size == 1:
            return result.item()
        return result
    return result

class MF_Fitter:# 擬合器
    def __init__(self, out , fit_params,):# 定義
        """
        fit_params:
            dict
            key   = 參數名稱(例如 'PCY1')
            value = {'x0': 初始值, 'lb': 下限, 'ub': 上限}

        out:(Fx,Fy,Mx,Mz,RRT(需要額外輸入 V and Ro ))
        """
        self.out = out
        self.fit_params = fit_params

    def pack(self, active_keys, stage_params):# 打包
        """
        只把 active_keys 的參數打包給 optimizer
        非 active_keys 的參數保持不動
        """
        x0, lb, ub = [], [], []

        for k in active_keys:
            info = self.fit_params[k]
            xi = float(stage_params[k])  # 現在值
            lbi = info.get("lb", xi)     # 沒設定下限，就用 xi（固定）
            ubi = info.get("ub", xi)     # 沒設定上限，就用 xi（固定）

            # 保證 xi 落在 bounds
            if xi < lbi: xi = lbi
            if xi > ubi: xi = ubi

            x0.append(xi)
            lb.append(lbi)
            ub.append(ubi)

        return np.array(x0), np.array(lb), np.array(ub)

    def unpack(self, x, active_keys, stage_params):# 解包
        """
        只更新 active_keys 對應的參數值
        非 active_keys 不動
        """
        for i, k in enumerate(active_keys):
            stage_params[k] = float(x[i])

    def residual(self, x, F_meas, active_keys, stage_params, MF_inputs):# MF計算殘餘
        """
        residual 計算時：
        - stage_params 是完整參數 dict
        - 先用 x 更新 active_keys
        - MF 計算使用完整參數
        """
        # 只把 active_keys 的值更新到 stage_params
        self.unpack(x, active_keys, stage_params)

        res = np.zeros_like(F_meas, dtype=float)

        # 處理未傳入參數
        if "RL" not in MF_inputs:
            Ro = [stage_params["UNLOADED_RADIUS"]]*len(MF_inputs["FZ"])
        else :
            Ro = MF_inputs["RL"]
        if "V" not in MF_inputs:
            V = [stage_params["LONGVL"]]*len(MF_inputs["FZ"])
            
        # 向量化計算：一次建立整組輸入並呼叫 MF 模型
        MF_all = CalculationInput(
            FZ=MF_inputs["FZ"],
            SA=MF_inputs["SA"],
            SL=MF_inputs["SL"],
            IA=MF_inputs["IA"],
            pressure=MF_inputs["pressure"],
            Ro = Ro,
            V = V,
            tir_params=stage_params,  # 傳完整參數
        )

        F_pred = MF_Universal_solver(self.out, MF_all)
        F_pred = np.asarray(F_pred, dtype=float).reshape(-1)
        F_meas_arr = np.asarray(F_meas, dtype=float).reshape(-1)

        return F_pred - F_meas_arr

    def fit(self, F_meas, stage_params, active_keys, MF_inputs):# 擬合
        """
        執行擬合：
        - stage_params: 完整參數 dict
        - active_keys: optimizer 可調參數
        """
        x0, lb, ub = self.pack(active_keys, stage_params)

        result = least_squares(
            self.residual,
            x0 = x0,
            bounds = (lb, ub),
            args = (F_meas, active_keys, stage_params, MF_inputs),
            method = "trf",
            verbose = 2,
            jac="3-point",
            loss="soft_l1",
            x_scale = "jac",
            ftol = 1e-6,
            xtol = 1e-6,
            gtol = 1e-6,
            max_nfev = 100,
        )

        # 把 active_keys 的最佳結果寫回 stage_params
        self.unpack(result.x, active_keys, stage_params)
        return result
    