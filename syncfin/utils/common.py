

def format_currency(amount):
    try:
        amount = float(amount)
    except Exception:
        return amount

    million = 10 ** 6
    billion = 10 ** 9
    trillion = 10 ** 12

    if amount < million:
        return '$ %s Million' % round(amount / million, 2)
    elif million <= amount <= billion:
        return '$ %s Million' % round(amount / million, 2)
    elif billion <= amount <= trillion:
        return '$ %s Billion' % round(amount / billion, 2)
    else:
        return '$ %s Trillion' % round(amount / trillion, 2)