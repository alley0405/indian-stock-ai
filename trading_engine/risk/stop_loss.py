def calculate_stop_loss(entry_price, stop_loss_pct):
    return round(entry_price * (1 -  stop_loss_pct / 100), 2)

def calculate_target(entry_prie, target_pct):
    return round(entry_price * (1 + target_pct / 100), 2)
