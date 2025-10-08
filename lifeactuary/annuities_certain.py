import numpy as np

class Annuities_Certain:
    def __new__(cls, interest_rate: float, m: int):
        if interest_rate < 0 or m < 0 or int(m) != m:
            print("We need a rate of interest non negative and a positive integer frequency")
            return None
        return object.__new__(cls)

    def __init__(self, interest_rate: float, m: int = 1):
        """
        Initialize an Annuities_Certain instance for financial annuity calculations.

        Args:
            interest_rate (float): Annual interest rate as a percentage (e.g., 5 for 5%).
            m (int, optional): Number of payments per year. Defaults to 1.

        Attributes:
            interest_rate (float): Interest rate as a decimal.
            frequency (int): Payment frequency per year.
            v (float): Discount factor per period.
            im (float): Interest rate per payment period.
            vm (float): Discount factor per payment period.
            dm (float): Discount rate per payment period.
        """
        self.interest_rate = interest_rate / 100.
        self.frequency = m

        self.v = 1 / (1 + self.interest_rate)
        self.im = self.frequency * (np.power(1 + self.interest_rate, 1 / self.frequency) - 1)
        self.vm = np.power((1 + self.im / self.frequency), -1)
        self.dm = self.im * self.vm

    def check_terms(func: callable) -> callable:
        """
        Decorator to validate the 'terms' argument for annuity calculation methods.

        Args:
            func (callable): The function to wrap.

        Returns:
            callable: The wrapped function that checks 'terms' before execution.
        """
        def func_wrapper(self, terms: int, *args, **kwargs):
            """
            Wrapper function to check validity of 'terms'.

            Args:
                self: Instance of the class.
                terms (int): Number of years/periods.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                Any: Result of the wrapped function or np.nan if invalid.
            """
            if not terms:
                terms = 0
            if terms < 0 or int(terms) != terms:
                return np.nan
            res = func(self, terms, *args, **kwargs)
            return res
        return func_wrapper

    def check_grow(func: callable) -> callable:
        """
        Decorator to validate the 'grow' and 'terms' arguments for geometric annuity calculation methods.

        Args:
            func (callable): The function to wrap.

        Returns:
            callable: The wrapped function that checks 'grow' and 'terms' before execution.
        """
        def func_wrapper(self, terms: int, payment: float, grow: float) -> float:
            """
            Wrapper function to check validity of 'grow' and 'terms'.

            Args:
                self: Instance of the class.
                terms (int): Number of years/periods.
                payment (float): First payment amount.
                grow (float): Growth rate per period (percentage).

            Returns:
                float: Result of the wrapped function or np.nan if invalid.
            """
            if grow / 100 <= -1 or terms < 0 or int(terms) != terms:
                return np.nan
            res = func(self, terms, payment, grow)
            return res
        return func_wrapper

    @check_terms
    def an(self, terms: int) -> float:
        """
        Present value of an immediate n-term annuity with payments of 1 at end of each period.

        Args:
            terms (int): Number of years.

        Returns:
            float: Present value of the annuity.
        """
        if not terms:
            return 1 / self.im
        return (1 - np.power(self.vm, terms * self.frequency)) / self.im

    @check_terms
    def aan(self, terms: int) -> float:
        """
        Present value of a due n-term annuity with payments of 1 at beginning of each period.

        Args:
            terms (int): Number of years.

        Returns:
            float: Present value of the annuity.
        """
        if not terms:
            return 1 / self.dm
        return (1 - np.power(self.vm, terms * self.frequency)) / self.dm

    @check_terms
    def Ian(self, terms: int, payment: float = 1, increase: float = 1) -> float:
        """
        Present value of an immediate n-term annuity with payments increasing/decreasing arithmetically.

        Args:
            terms (int): Number of years.
            payment (float, optional): First payment amount. Defaults to 1.
            increase (float, optional): Increase per period (positive for increasing, negative for decreasing). Defaults to 1.

        Returns:
            float: Present value of the annuity.
        """
        if payment + increase * terms < 0:
            return np.nan
        return payment * self.an(terms) + increase / self.im * (
            (1 - self.v ** terms) / self.interest_rate - terms * self.v ** terms
        )

    @check_terms
    def Iaan(self, terms: int, payment: float = 1, increase: float = 1) -> float:
        """
        Present value of a due n-term annuity with payments increasing/decreasing arithmetically.

        Args:
            terms (int): Number of years.
            payment (float, optional): First payment amount. Defaults to 1.
            increase (float, optional): Increase per period. Defaults to 1.

        Returns:
            float: Present value of the annuity.
        """
        return self.Ian(terms, payment, increase) / self.vm

    @check_terms
    def Iman(self, terms: int, payment: float = 1, increase: float = 1) -> float:
        """
        Present value of an immediate n-term annuity with payments increasing/decreasing arithmetically
        in each payment period.

        Args:
            terms (int): Number of years.
            payment (float, optional): First payment amount. Defaults to 1.
            increase (float, optional): Increase per payment period. Defaults to 1.

        Returns:
            float: Present value of the annuity.
        """
        if payment + increase * terms < 0:
            return np.nan
        return (payment - increase) * self.an(terms) \
            + increase * self.v \
            * (self.v ** terms * ((terms * self.frequency) * (self.vm - 1) - 1) + 1) \
            / (self.frequency * self.v ** ((self.frequency - 1) / self.frequency) * (self.vm - 1) ** 2)

    @check_terms
    def Imaan(self, terms: int, payment: float = 1, increase: float = 1) -> float:
        """
        Present value of a due n-term annuity with payments increasing/decreasing arithmetically
        in each payment period.

        Args:
            terms (int): Number of years.
            payment (float, optional): First payment amount. Defaults to 1.
            increase (float, optional): Increase per payment period. Defaults to 1.

        Returns:
            float: Present value of the annuity.
        """
        return self.Iman(terms, payment, increase) / self.vm

    @check_grow
    def Gan(self, terms: int, payment: float = 1, grow: float = 0) -> float:
        """
        Present value of an immediate n-term annuity with payments increasing/decreasing geometrically.

        Args:
            terms (int): Number of years.
            payment (float, optional): First payment amount. Defaults to 1.
            grow (float, optional): Growth rate per year (percentage). Defaults to 0.

        Returns:
            float: Present value of the annuity.
        """
        v = (1 + grow / 100) * self.v
        if self.interest_rate == grow / 100:
            return payment * terms * self.frequency * self.vm / self.frequency
        return payment / (1 + grow / 100) ** (1 / self.frequency) * (1 - v ** terms) / \
            (1 - v ** (1 / self.frequency)) * v ** (1 / self.frequency) / self.frequency

    @check_grow
    def Gaan(self, terms: int, payment: float = 1, grow: float = 0) -> float:
        """
        Present value of a due n-term annuity with payments increasing/decreasing geometrically.

        Args:
            terms (int): Number of years.
            payment (float, optional): First payment amount. Defaults to 1.
            grow (float, optional): Growth rate per year (percentage). Defaults to 0.

        Returns:
            float: Present value of the annuity.
        """
        v = (1 + grow / 100) * self.v
        return self.Gan(terms, payment, grow) / v ** (1 / self.frequency)

    @check_grow
    def Gman(self, terms: int, payment: float = 1, grow: float = 0) -> float:
        """
        Present value of an immediate n-term annuity with payments increasing/decreasing geometrically
        in each payment period.

        Args:
            terms (int): Number of years.
            payment (float, optional): First payment amount. Defaults to 1.
            grow (float, optional): Growth rate per payment period (percentage). Defaults to 0.

        Returns:
            float: Present value of the annuity.
        """
        a1 = (1 - self.v) / self.im
        if self.interest_rate == grow / 100:
            return a1 * terms
        ig = (self.interest_rate - grow / 100) / (1 + grow / 100)
        vg = 1 / (1 + ig)
        a2 = (1 - vg ** terms) / (1 - vg)
        return payment * a1 * a2

    @check_grow
    def Gmaan(self, terms: int, payment: float = 1, grow: float = 0) -> float:
        """
        Present value of a due n-term annuity with payments increasing/decreasing geometrically
        in each payment period.

        Args:
            terms (int): Number of years.
            payment (float, optional): First payment amount. Defaults to 1.
            grow (float, optional): Growth rate per payment period (percentage). Defaults to 0.

        Returns:
            float: Present value of the annuity.
        """
        v = (1 + grow / 100) * self.v
        return self.Gman(terms, payment, grow) / v ** (1 / self.frequency)
