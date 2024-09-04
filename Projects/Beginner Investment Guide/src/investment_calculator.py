# investment_calculator.py

def calculate_compound_interest(principal, rate, times_compounded, years):
    """
    Calculate compound interest.

    :param principal: Initial amount of money.
    :param rate: Annual interest rate (as a decimal).
    :param times_compounded: Number of times interest is compounded per year.
    :param years: Number of years the money is invested for.
    :return: The amount of money accumulated after n years, including interest.
    """
    return principal * (1 + rate / times_compounded) ** (times_compounded * years)

def calculate_future_value(principal, annual_rate, periods_per_year, years):
    """
    Calculate future value of an investment.

    :param principal: Initial investment amount.
    :param annual_rate: Annual interest rate (as a decimal).
    :param periods_per_year: Number of compounding periods per year.
    :param years: Number of years the investment is held.
    :return: The future value of the investment.
    """
    rate_per_period = annual_rate / periods_per_year
    total_periods = periods_per_year * years
    return principal * (1 + rate_per_period) ** total_periods

def calculate_annualized_return(initial_investment, final_value, years):
    """
    Calculate the annualized return of an investment.

    :param initial_investment: The initial amount of money invested.
    :param final_value: The final value of the investment after the holding period.
    :param years: Number of years the money was invested.
    :return: The annualized return (as a decimal).
    """
    return (final_value / initial_investment) ** (1 / years) - 1

if __name__ == "__main__":
    # Example usage
    principal = 1000
    rate = 0.05
    times_compounded = 4  # Quarterly
    years = 10

    compound_interest = calculate_compound_interest(principal, rate, times_compounded, years)
    future_value = calculate_future_value(principal, rate, times_compounded, years)
    annualized_return = calculate_annualized_return(principal, future_value, years)

    print(f"Compound Interest: ${compound_interest:.2f}")
    print(f"Future Value: ${future_value:.2f}")
    print(f"Annualized Return: {annualized_return:.2%}")
