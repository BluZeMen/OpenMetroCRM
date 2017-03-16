from datetime import date, timedelta

from django import template

register = template.Library()


@register.simple_tag
def mark_check_date(check_date, danger_days=0, warning_days=7, ok_days=30):
    zero_date = date.today()
    check_date = date(check_date.year, check_date.month, check_date.day)
    danger_date = zero_date + timedelta(days=danger_days)
    warning_date = zero_date + timedelta(days=warning_days)
    ok_date = zero_date + timedelta(days=ok_days)

    # print('dates:', check_date, zero_date, ok_date)

    if check_date < danger_date:
        return 'danger'
    elif danger_date <= check_date <= warning_date:
        return 'warning'
    elif warning_date < check_date <= ok_date:
        return 'success'
    else:
        return ''
