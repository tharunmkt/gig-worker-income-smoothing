TARGET_DAILY_INCOME = 5000

def calculate_smoothing(actual_income, current_buffer):
    if actual_income >= TARGET_DAILY_INCOME:
        deposit = actual_income - TARGET_DAILY_INCOME
        new_buffer = current_buffer + deposit
        payout = TARGET_DAILY_INCOME

        return {
            "transaction": "Deposit",
            "amount": deposit,
            "buffer": new_buffer,
            "salary": payout
        }

    else:
        shortage = TARGET_DAILY_INCOME - actual_income

        withdraw = min(shortage, current_buffer)

        payout = actual_income + withdraw

        new_buffer = current_buffer - withdraw

        return {
            "transaction": "Withdraw",
            "amount": withdraw,
            "buffer": new_buffer,
            "salary": payout
        }