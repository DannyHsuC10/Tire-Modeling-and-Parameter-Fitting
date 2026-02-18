"""
MF 6.1.2 輪胎模型 - 統一接口
Magic Formula 6.1.2 Tire Model - Unified API

提供統一的接口函數和便利函數：
- create_calculation_input_from_config() - 從配置建立計算輸入
- calculate_* 便利函數 - 簡化的計算函數
- 測試和日誌
"""

import numpy as np
from typing import Union, Dict
import logging

from ._common import (
    CalculationInput
)

from .Mx_models import MF612_Mx
from .Mz_models import MF612_Mz
from .RRT_models import MF612_RRT_SAE
from .Fy_models import MF612_Fy
from .Fx_models import MF612_Fx


logger = logging.getLogger(__name__)

def create_calculation_input_from_config(
    *,
    FZ: Union[float, np.ndarray],
    SA: Union[float, np.ndarray],
    SL: Union[float, np.ndarray],
    IA: Union[float, np.ndarray],
    pressure: Union[float, np.ndarray],
    tir_params: Dict[str, float],
    V: Union[float, np.ndarray] = None,
    Ro: Union[float, np.ndarray] = None,
    Fx: Union[float, np.ndarray] = None,
    Fy: Union[float, np.ndarray] = None,
) -> CalculationInput:
    """
    建立 CalculationInput（工況為主，TIR 參數完整注入）
    """

    calc_input = CalculationInput(
        FZ=FZ,
        SA=SA,
        SL=SL,
        IA=IA,
        pressure=pressure,
        V=V,
        Ro=Ro,
        Fx=Fx,
        Fy=Fy,
        tir_params=tir_params,
    )

    return calc_input

# ============================================================================
# 混合工況便利函數
# ============================================================================

def calculate_fx(calc_input: CalculationInput) -> np.ndarray:
    """便利函數: 計算混合縱向力
    
    Args:
        calc_input: CalculationInput 對象
        Rx: 混合滑移相互作用係數向量 (7個)
    Returns:
        Fx: 混合縱向力 [N]
    """
    return MF612_Fx.calculate(calc_input)


def calculate_fy(calc_input: CalculationInput) -> np.ndarray:
    """便利函數: 計算混合橫向力
    
    Args:
        calc_input: CalculationInput 對象
        Ry: 混合滑移相互作用係數向量 (15個)
    Returns:
        Fy: 混合橫向力 [N]
    """
    return MF612_Fy.calculate(calc_input)


def calculate_mz(calc_input: CalculationInput) -> np.ndarray:
    """便利函數: 計算混合回正力矩
    Args:
        calc_input: CalculationInput 對象
        Py: 側向力係數向量 (27個)
        Ry: 混合滑移相互作用係數向量 (15個)
        Sz: 混合滑移力矩移位係數向量 (4個)
    
    Returns:
        Mz: 混合回正力矩 [N·m]
    """
    return MF612_Mz.calculate(calc_input)


# ============================================================================
# 可選公式便利函數
# ============================================================================

def calculate_mx(calc_input: CalculationInput) -> np.ndarray:
    """便利函數: 計算顛覆力矩 (可選)
    Args:
        calc_input: CalculationInput 對象 (需要 Fy)
    Returns:
        Mx: 顛覆力矩 [N·m]
    """
    return MF612_Mx.calculate(calc_input)

def calculate_rrt(calc_input: CalculationInput) -> np.ndarray:
    """便利函數: 計算滾動阻力(可選)
    Args:
        calc_input: CalculationInput 對象 (需要 Fx)
    Returns:
        RRT: 滾動阻力矩 [N·m]
    """
    return MF612_RRT_SAE.calculate(calc_input)

# ============================================================================
# 模組初始化和測試
# ============================================================================

def _print_module_info():
    logger.info("="*70)
    logger.info("MF612 公式模組已載入")
    logger.info("="*70)

    logger.info("\n📚 支援的公式類型:")
    logger.info("  • Fy0  - Pure side slip lateral force")
    logger.info("  • Fx0  - Pure longitudinal slip force")
    logger.info("  • Mz0  - Pure aligning torque")
    logger.info("  • Fx   - Combined slip longitudinal force")
    logger.info("  • Fy   - Combined slip lateral force")
    logger.info("  • Mz   - Combined slip aligning torque")
