from __future__ import absolute_import

import decimal

from django import template
from django.forms.widgets import CheckboxInput


register = template.Library()


CURRENCY_TO_SYMBOL = {
    'USD': ('$', 'left'),
}


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, CheckboxInput)


@register.filter
def format_money(amount, currency):
    amount = decimal.Decimal(amount).quantize(decimal.Decimal('0.01'))
    if currency in CURRENCY_TO_SYMBOL:
        symbol, side = CURRENCY_TO_SYMBOL[currency]
        format = u'{symbol}{amount}' if side == 'left' else '{amount}{symbol}'
        return format.format(symbol=symbol, amount=amount)
    return u'{} {}'.format(amount, currency)


@register.filter
def absolute_value(value):
    try:
        return abs(value)
    except TypeError:
        return ''
