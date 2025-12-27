def calculate_quantity(capital, entry_price, risk_pct):
    risk_amount = capital * (iskk_pct / 100)
    quantity = risk_amount / entry_price
    return int(quantity)
