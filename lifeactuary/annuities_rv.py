from lifeActuary import mortality_table


def gen_an(
    interest_rate: float = 0.0,
    payments_moments: list[float] = [0],
    payments: list[float] = [1]
) -> float:
    """
    Calculate the present value of an annuity certain given an interest rate and payment schedule.

    Args:
        interest_rate (float): Annual interest rate as a percentage (e.g., 5 for 5%).
        payments_moments (list[float]): Times (in years) when payments are made.
        payments (list[float]): Amounts of each payment.

    Returns:
        float: Present value of the annuity.
    """
    if not isinstance(payments_moments, list):
        raise TypeError("payments_moments must be a list")
    if not isinstance(payments, list):
        raise TypeError("payments must be a list")
    if len(payments_moments) != len(payments):
        raise ValueError(
            "payments_moments and payments must have the same length")

    int_rate = interest_rate / 100.0
    an = [payments[idx] / (1 + int_rate) ** moment for idx,
          moment in enumerate(payments_moments)]
    return sum(an)


def gen_axn(
    mort_table: mortality_table,
    interest_rate: float = 0.0,
    payments_moments: list[float] = [0],
    payments: list[float] = [1],
    x: float = 0.0,
    moment: float = 1.0,
    method: str = "udd"
) -> float:
    """
    Calculate the expected present value of an annuity contingent on survival, using a mortality table.

    Args:
        mort_table (mortality_table): Mortality table object with npx and nqx methods.
        interest_rate (float): Annual interest rate as a percentage.
        payments_moments (list[float]): Times (in years) when payments are made.
        payments (list[float]): Amounts of each payment.
        x (float): Age at start of annuity.
        moment (float): Moment for calculation (typically 1 for mean).

    Returns:
        float: Expected present value of the contingent annuity.
    """
    if not isinstance(payments_moments, list):
        raise TypeError("payments_moments must be a list")
    if not isinstance(payments, list):
        raise TypeError("payments must be a list")
    if len(payments_moments) != len(payments):
        raise ValueError(
            "payments_moments and payments must have the same length")
    
    # the case x is larger than the maximum age in the mortality table
    if x >= mort_table.w+1:
        if 0 in payments_moments:
            return payments[0]
        else:
            return 0.
    
    # trim payments and moments to the maximum age in the mortality table
    max_moment = mort_table.w - x + 1
    idx_m = next((i for i, m in enumerate(payments_moments)
                 if m > max_moment), len(payments_moments))

    if len(payments_moments) > idx_m:
        payments_moments = payments_moments[0:idx_m]
        payments = payments[0:idx_m]

    # handle edge case where there are no payments
    if len(payments) == 0:
        return 0.    

    an = [gen_an(interest_rate, payments_moments[0:(i + 1)], payments[0:(i + 1)])
          for i, _ in enumerate(payments_moments)]

    prob_surv = [mort_table.npx(x, m, method) for m in payments_moments]
    prob_surv_2 = [prob_surv[i] - prob_surv[i + 1]
                   for i in range(len(prob_surv) - 1)]
    last_prob_surv = mort_table.npx(x, payments_moments[-1], method)
    prob_surv_2.append(last_prob_surv)

    first_prob_surv = mort_table.nqx(x, payments_moments[0], method)
    assert abs((sum(prob_surv_2) + first_prob_surv) - 1) < 1e-6, \
        "Sum of survival probabilities should be 1 (within tolerance)"

    expected_liabilities = [an[i] ** moment * prob_surv_2[i]
                            for i in range(len(an))]
    return sum(expected_liabilities)
