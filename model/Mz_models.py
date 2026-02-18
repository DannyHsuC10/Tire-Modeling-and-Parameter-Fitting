import numpy as np
from ._common import MF612, CalculationInput
from .Fy_models import MF612_Fy0,MF612_Fy
from .Fx_models import MF612_Fx


vsign = 1# 假設方向相同不會往回轉
zeta0 = 1
zeta1 = 1
zeta2 = 1
zeta3 = 1
zeta4 = 1
zeta5 = 1
zeta6 = 1
zeta7 = 1
zeta8 = 1

class MF612_Mz(MF612):
    """純側滑回正力矩 Mz0 (Pure Aligning Torque)"""

    @staticmethod
    def calculate(MF: 'CalculationInput') -> np.ndarray:
        # 純側滑力
        Fy0 = MF612_Fy0.calculate(MF)
        dpi, dpi2 = MF612._normalize_pressure(MF)

        # 正規化
        Fzo_prime, dfz = MF612._normalize_load(MF)
        ami, iaMi, iaMi2 = MF612._normalize_angles(MF.SA, MF.IA)

        Ro = MF.Ro
        
        # --- Pneumatic trail parameters (4.E34 ~ 4.E39) ---
        Bt = ((MF.QBZ1 + MF.QBZ2 * dfz + MF.QBZ3 * dfz**2) *
              (1 + MF.QBZ5 * abs(iaMi) + MF.QBZ4 * iaMi) *
              MF.LYKA)

        Ct = MF.QCZ1

        Dr = (MF.FZ * Ro * 
            ((MF.QDZ6 + MF.QDZ7 * dfz) * MF.LMP * zeta2 + ((MF.QDZ8 + MF.QDZ9 * dfz) * 
            (1 + MF.PPZ2 * dfz) * abs(iaMi)) * iaMi * MF.LKYC * zeta0) * MF.LMUY * zeta4 * np.cos(MF.V)
            + zeta8 - 1)
        
        Dt0 = (MF.FZ * Ro /
              (Fzo_prime + MF.EPSILON)) * \
             (MF.QDZ1 + MF.QDZ2 * dfz) * (1-MF.PPZ1 * dpi) * vsign * MF.LRES

        Dt = Dt0 * (1 + MF.QDZ3 * abs(iaMi) + MF.QDZ4 * iaMi2) * zeta5

        Et = ((MF.QEZ1 + MF.QEZ2 * dfz + MF.QEZ3 * dfz**2) *
              (1 + (MF.QEZ4 + MF.QEZ5 * iaMi) *
               (2/np.pi) * np.arctan(Bt * ami)))

        at = ami + MF.QHZ1 + MF.QHZ2 * dfz + (MF.QHZ3 + MF.QHZ4 * dfz) * iaMi

        # Pneumatic trail
        t0 = Dt * np.cos(
            Ct * np.arctan(Bt * at - Et * (Bt * at - np.arctan(Bt * at)))) * np.cos(MF.V)
        
        term = (MF.FZ / Fzo_prime) / (
            (MF.PKY2 + MF.PKY5 * iaMi) * (1 + MF.PPY2 * dpi)
        )

        Kya = (
            MF.PKY1 * Fzo_prime
            * (1 + MF.PPY1 * dpi)
            * (1 - MF.PKY3 * abs(iaMi))
            * np.sin(MF.PKY4 * np.arctan(term))
            * MF.LYKA * zeta3
        )

        muy = (
            (MF.PDY1 + MF.PDY2 * dfz)
            * (1 + MF.PPY3 * dpi + MF.PPY4 * dpi2)
            * (1 - MF.PDY3 * iaMi)
            * MF.LMUY
        )

        Cr = zeta7

        Cy = MF.PCY1 * MF.LCY

        Dy = muy * MF.FZ * zeta2

        By = Kya / (Cy * Dy + MF.EPSILON_Y)

        Br = (MF.QBZ9 * MF.LKZC / MF.LMUY + MF.QBZ10 * By * Cy) * zeta6

        Mzr0 = Dr * np.cos(Cr * np.atan(Br))
        # Pure aligning torque

        MzoPrime = -t0 * Fy0

        Mz0 = MzoPrime + Mzr0

        Fy = MF612_Fy.calculate(MF)
        Fx = MF612_Fx.calculate(MF)

        # 修正側偏角
        alpha_star = np.tan(np.radians(MF.SA))

        # cos(α*) 修正 (4.E71)
        cos_alpha = 1.0 / np.sqrt(1.0 + alpha_star**2)

        Kxk = (MF.FZ * (MF.PKX1 + MF.PKX2 * dfz) *
               np.exp(MF.PKX3 * dfz) *
               (1 + MF.PPX1 * dpi + MF.PPX2 * dpi2) *MF.LKX)

        term = (MF.FZ / Fzo_prime) / (
            (MF.PKY2 + MF.PKY5 * iaMi) * (1 + MF.PPY2 * dpi)
        )

        Kya = (
            MF.PKY1 * Fzo_prime
            * (1 + MF.PPY1 * dpi)
            * (1 - MF.PKY3 * abs(iaMi))
            * np.sin(MF.PKY4 * np.arctan(term))
            * MF.LYKA * zeta3
        )

        s = Ro*(MF.SSZ1+MF.SSZ2 * ( Fy / Fzo_prime) + 
                (MF.SSZ3+ MF.SSZ4 * dfz) * iaMi)*MF.LS 

        KyaPrime = Kya + MF.epsilonK

        KxkKya2 = (Kxk/KyaPrime)**2

        alphatEq = np.sqrt(np.radians(MF.SA)**2 + MF.SL**2 * KxkKya2) * np.sign(np.radians(MF.SA))

        Mzr = Dr * np.cos(Cr * np.atan(Br * alphatEq))
        # 最終回正力矩

        Mz_Fybase =  cos_alpha * (Fy / (MF612_Fy0.calculate(MF) + MF.EPSILON))

        Mz = Mz0 * Mz_Fybase + Mzr + Fx * s**2

        return Mz
