from lifeActuary import mortality_table

def gen_Axn(
    mort_table: mortality_table,
    interest_rate: float = 0.0,
    payments_moments: list[float] = [0],
    payments: list[float] = [1],
    x: float = 0.0,
    moment: float = 1.0,
    method: str = "udd"
) -> float:
    """
    Calculate the expected present value of a mortality insurance, using a mortality table.

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
        raise TypeError("payments_moments must be a list.")
    if not isinstance(payments, list):
        raise TypeError("payments must be a list.")
    if len(payments_moments) != len(payments):
        raise ValueError(
            "payments_moments and payments must have the same length.")
    
    # the case x is larger than the maximum age in the mortality table
    if x >= mort_table.w+1:
        if 0 in payments_moments:
            return payments[1]/(1 + interest_rate / 100)**payments_moments[1]
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

    v= 1 / (1 + interest_rate / 100)
    an = [payments[i]*v**payments_moments[i] for i, h in enumerate(payments_moments)]

    # compute the probability of no payment
    prob_0_begin = mort_table.nqx(x, payments_moments[0], method)
    prob_0_end = mort_table.npx(x, payments_moments[-1], method)
    prob_0= prob_0_begin + prob_0_end

    prob_surv = [mort_table.npx(x, m, method) for m in payments_moments]
    prob_surv_2 = [prob_surv[i] - prob_surv[i + 1]
                   for i in range(len(prob_surv) - 1)]

    assert abs((sum(prob_surv_2) + prob_0) - 1) < 1e-6, \
        "Sum of survival probabilities should be 1 (within tolerance)"

    expected_liabilities = [a ** moment * prob_surv_2[i]
                            for i, a in enumerate(an[1:])]
    return sum(expected_liabilities)