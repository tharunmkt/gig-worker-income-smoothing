TARGET_DEFAULT = 5000


def calculate_smoothing(actual_income, target_income, current_buffer):
    """
    Calculates:
    - Virtual salary paid
    - New buffer balance
    - Deposit/Withdrawal
    """

    if actual_income >= target_income:

        deposit = actual_income - target_income

        new_buffer = current_buffer + deposit

        return {
            "virtual_salary": target_income,
            "buffer_change": deposit,
            "new_buffer": new_buffer,
            "transaction_type": "Deposit",
            "remarks": "Surplus added to buffer"
        }

    shortage = target_income - actual_income

    withdraw = min(shortage, current_buffer)

    virtual_salary = actual_income + withdraw

    new_buffer = current_buffer - withdraw

    return {
        "virtual_salary": virtual_salary,
        "buffer_change": withdraw,
        "new_buffer": new_buffer,
        "transaction_type": "Withdrawal",
        "remarks": "Buffer used to smooth income"
    }