from datetime import datetime, timedelta
from django import template

register = template.Library()


@register.simple_tag
def mark_check_date(date):
    danger_time = datetime.today().date()
    warning_time = danger_time + timedelta(days=7)
    going_time = danger_time + timedelta(days=30)

    if date < danger_time:
        return 'danger'
    elif danger_time <= date <= warning_time:
        return 'warning'
    elif warning_time < date <= going_time:
        return 'success'
    else:
        return ''
