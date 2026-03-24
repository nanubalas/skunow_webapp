from django import template

register = template.Library()

CURRENCY_SYMBOLS = {
    "GBP": "£",
    "USD": "$",
    "EUR": "€",
}

@register.filter
def money(value, currency_code="GBP"):
    try:
        symbol = CURRENCY_SYMBOLS.get(currency_code, currency_code + " ")
        return f"{symbol}{float(value):,.2f}"
    except Exception:
        return value