def format_indian_currency(number):
    """
    Convert number into Indian currency format
    like Lakhs and Crores.
    """

    if number >= 10000000:
        return f"₹ {number / 10000000:.2f} Cr"

    elif number >= 100000:
        return f"₹ {number / 100000:.2f} L"

    else:
        return f"₹ {number:,.0f}"