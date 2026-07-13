from decimal import Decimal

def minimize_debts(balances):
    """
    Accepts a dictionary of user IDs and their net balances, e.g.:
    {user_1: Decimal('50.00'), user_2: Decimal('-30.00'), user_3: Decimal('-20.00')}
    Returns a list of clean payment instructions: (payer, receiver, amount)
    """
    # Separate roommates into creditors (positive net) and debtors (negative net)
    participants = list(balances.items())
    
    debtors = []
    creditors = []
    
    for user, net_value in participants:
        if net_value < 0:
            debtors.append([user, abs(net_value)])
        elif net_value > 0:
            creditors.append([user, net_value])
            
    transactions = []
    
    # Match greatest debtors with greatest creditors
    while debtors and creditors:
        debtor = debtors[0]
        creditor = creditors[0]
        
        min_amount = min(debtor[1], creditor[1])
        
        transactions.append({
            'from_user': debtor[0],
            'to_user': creditor[0],
            'amount': round(min_amount, 2)
        })
        
        # Deduct the settled amount
        debtor[1] -= min_amount
        creditor[1] -= min_amount
        
        if debtor[1] < Decimal('0.01'):
            debtors.pop(0)
        if creditor[1] < Decimal('0.01'):
            creditors.pop(0)
            
    return transactions