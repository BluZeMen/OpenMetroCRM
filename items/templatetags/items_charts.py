import copy
import json

from datetime import timedelta, datetime
from django import template
from django.utils.safestring import mark_safe

from items.models import MeasuringInstrument, MeasuringInstrumentType

register = template.Library()


@register.simple_tag
def mi_year_check_per_organization_series():
    instruments = list(MeasuringInstrument.objects.all().values(
        'id', 'next_check_date', 'type__checking_organization__name'))
    data = dict()
    for ins in instruments:
        if ins['type__checking_organization__name'] not in data:
            data[ins['type__checking_organization__name']] = [0]*12
        data[ins['type__checking_organization__name']][ins['next_check_date'].month-1] += 1  # counting instruments per month

    series = [{'name': org, 'data': data[org]} for org in data]  # formatting for hightcharts
    return mark_safe(json.dumps(series, ensure_ascii=False))


@register.simple_tag
def mi_operative_check_series(period_days=31):
    # Getting all required info about organizations}
    operative_date = datetime.today() + timedelta(days=period_days)
    data = dict()

    instruments = list(MeasuringInstrument.objects.filter(
        next_check_date__lte=operative_date).values('id',
                                                    'next_check_date',
                                                    'type__name',
                                                    'type__checking_organization__name'))

    attr_org = 'type__checking_organization__name'
    attr_type = 'type__name'

    organizations = {key[attr_org]: 0 for key in instruments}
    types = {key[attr_type]: 0 for key in instruments}

    ch_serie_item, ch_serie_name = attr_org, attr_type
    cats = organizations

    for ins in instruments:
        if ins[ch_serie_name] not in data:
            data[ins[ch_serie_name]] = copy.copy(cats)
        if ins[ch_serie_item] not in data[ins[ch_serie_name]]:
            data[ins[ch_serie_name]][ins[ch_serie_item]] = 0
        data[ins[ch_serie_name]][ins[ch_serie_item]] += 1

    series = [{'name': key, 'data': list(data[key].values())}
              for key in data] # formatting for hightcharts
    return {
        'series': mark_safe(json.dumps(series, ensure_ascii=False)),
        'categories': mark_safe(json.dumps(list(cats.keys()), ensure_ascii=False))
    }
