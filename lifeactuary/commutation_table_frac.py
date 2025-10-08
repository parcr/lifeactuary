__author__ = "PedroCR"

import numpy as np
import pandas as pd
from lifeActuary.commutation_table import CommutationFunctions


class CommutationFunctionsFrac(CommutationFunctions):
    """
    Extension of CommutationFunctions to fractional ages.
    Instantiates, for a specific mortality table and interest rate, all the usual commutation functions:
    Dx, Nx, Sx, Cx, Mx, Rx, at fractional ages.

    :param i: Interest rate (annual effective).
    :param g: Growth rate (default 0).
    :param data_type: Type of mortality data ('q' by default).
    :param mt: Mortality table.
    :param perc: Percentage scaling for mortality rates.
    :param frac: Number of fractional intervals per year (e.g., 2 for semiannual).
    :param method: Interpolation method for fractional ages ('udd' by default).
    """

    def __init__(
        self,
        i: float = None,
        g: float = 0,
        data_type: str = 'q',
        mt=None,
        perc: float = 100,
        frac: int = 2,
        method: str = 'udd'
    ):
        """
        Initialize fractional commutation functions.

        :param i: Interest rate.
        :param g: Growth rate.
        :param data_type: Mortality data type.
        :param mt: Mortality table.
        :param perc: Percentage scaling.
        :param frac: Number of fractional intervals per year.
        :param method: Interpolation method.
        """
        super().__init__(i, g, data_type, mt, perc, app_cont=False)
        if method not in self.methods:
            return
        if frac <= 0 or not isinstance(frac, int):
            return

        self.__method: str = method
        self.__frac: int = frac

        self.__ages: np.ndarray = np.linspace(0, self.w + 1, (self.w + 1) * self.frac + 1)

        radical: float = 100000.

        self.__lx_frac: np.ndarray = np.array([self.npx(x=0, n=x, method=self.__method) for x in self.__ages])
        self.__lx_frac *= radical
        self.__px_frac: np.ndarray = np.array([self.npx(x=x, n=1 / self.__frac, method=self.__method) for x in self.__ages])
        self.__qx_frac: np.ndarray = 1 - self.__px_frac
        self.__dx_frac: np.ndarray = self.__lx_frac[:-1] - self.__lx_frac[1:]
        self.__dx_frac = np.append(self.__dx_frac, 0)

        # Commutation Functions
        self.__Dx_frac: np.ndarray = self.__lx_frac[:] * np.power(self.d, self.__ages)
        self.__Nx_frac: np.ndarray = np.array([np.sum(self.__Dx_frac[x:]) for x in range(len(self.__ages))])
        self.__Sx_frac: np.ndarray = np.array([np.sum(self.__Nx_frac[x:]) for x in range(len(self.__ages))])
        self.__Cx_frac: np.ndarray = self.dx_frac * np.power(self.d, self.__ages + 1 / self.__frac)
        self.__Mx_frac: np.ndarray = np.array([np.sum(self.__Cx_frac[x:]) for x in range(len(self.__ages))])
        self.__Rx_frac: np.ndarray = np.array([np.sum(self.__Mx_frac[x:]) for x in range(len(self.__ages))])

    def __repr__(self) -> str:
        """
        String representation of the object.
        """
        return (
            f"{self.__class__.__name__}"
            f"{self.i, self.g, self.data_type, self.mt, self.perc, self.frac, self.method} "
        )

    def df_commutation_table_frac(self) -> pd.DataFrame:
        """
        Returns a pandas DataFrame containing the fractional commutation table.

        :return: DataFrame with columns for ages, lx, dx, qx, px, Dx, Nx, Sx, Cx, Mx, Rx.
        """
        data1 = {
            'x': self.__ages,
            'lx': self.__lx_frac[:],
            'dx': self.__dx_frac,
            'qx': self.__qx_frac,
            'px': self.__px_frac
        }
        data2 = {
            'Dx': self.__Dx_frac,
            'Nx': self.__Nx_frac,
            'Sx': self.__Sx_frac,
            'Cx': self.__Cx_frac,
            'Mx': self.__Mx_frac,
            'Rx': self.__Rx_frac
        }
        data = {**data1, **data2}
        df = pd.DataFrame(data)
        return df

    # getters and setters
    @property
    def method(self) -> str:
        """
        Interpolation method for fractional ages.
        """
        return self.__method

    @method.setter
    def method(self, m: str):
        """
        Set interpolation method.
        """
        self.__method = m

    @property
    def frac(self) -> int:
        """
        Number of fractional intervals per year.
        """
        return self.__frac

    @frac.setter
    def frac(self, f: int):
        """
        Set number of fractional intervals per year.
        """
        self.__frac = f

    @property
    def ages(self) -> np.ndarray:
        """
        Array of fractional ages.
        """
        return self.__ages

    @property
    def lx_frac(self) -> np.ndarray:
        """
        Array of lx values at fractional ages.
        """
        return self.__lx_frac

    @property
    def px_frac(self) -> np.ndarray:
        """
        Array of px values at fractional ages.
        """
        return self.__px_frac

    @property
    def qx_frac(self) -> np.ndarray:
        """
        Array of qx values at fractional ages.
        """
        return self.__qx_frac

    @property
    def dx_frac(self) -> np.ndarray:
        """
        Array of dx values at fractional ages.
        """
        return self.__dx_frac

    @property
    def Dx_frac(self) -> np.ndarray:
        """
        Array of Dx values at fractional ages.
        """
        return self.__Dx_frac

    @property
    def Nx_frac(self) -> np.ndarray:
        """
        Array of Nx values at fractional ages.
        """
        return self.__Nx_frac

    @property
    def Sx_frac(self) -> np.ndarray:
        """
        Array of Sx values at fractional ages.
        """
        return self.__Sx_frac

    @property
    def Cx_frac(self) -> np.ndarray:
        """
        Array of Cx values at fractional ages.
        """
        return self.__Cx_frac

    @property
    def Mx_frac(self) -> np.ndarray:
        """
        Array of Mx values at fractional ages.
        """
        return self.__Mx_frac

    @property
    def Rx_frac(self) -> np.ndarray:
        """
        Array of Rx values at fractional ages.
        """
        return self.__Rx_frac

    def age_to_index(self, age_int: int, age_frac: float) -> int | float:
        """
        Get the index for a specific age (integer part and fractional part)
        to use with the fractional commutation vectors.

        :param age_int: Integer part of age.
        :param age_frac: Fractional part of age (0 <= age_frac < 1).
        :return: Index in the fractional age arrays, or np.nan if invalid.
        """
        parts = np.round(age_frac * self.frac, 5)
        if int(parts) == parts and age_int == int(age_int):
            return int((age_int + age_frac) * self.__frac)
        return np.nan
