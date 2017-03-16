import json

from classytags.arguments import Argument, MultiKeywordArgument
from django import template
from django.db.models.options import Options
from django.utils.safestring import mark_safe

from items.models import MeasuringInstrument
from site_app.templatetags.charts import BaseChart

register = template.Library()


class StatOfYearChart(BaseChart):
    name = 'chart_year_stat'
    template = 'items/tags/charts/year_stat.html'

    def get_panel_context(self, *args, **kwargs):
        arguments = super(StatOfYearChart, self).get_panel_context(*args, **kwargs)

        q = MeasuringInstrument.objects.year_checking_stat_per_organization_and_month(kwargs.get('year', None))

        data = {}
        for group in list(q):
            org = group['type__checking_organization__name']
            month = group['checking_month']
            mi_count_in_org_in_month = group['type__checking_organization__count']
            if org not in data:
                # init 12 "months"(counts) of instruments to check
                data[org] = [0] * 12
            data[org][month - 1] = mi_count_in_org_in_month

        series = [{'name': org, 'data': data[org]} for org in data]  # formatting for hightcharts
        categories = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
                      'Октябрь', 'Ноябрь', 'Декабрь']
        arguments['series'] = mark_safe(json.dumps(series, ensure_ascii=False))
        arguments['categories'] = mark_safe(json.dumps(categories, ensure_ascii=False))
        return arguments


register.tag(StatOfYearChart)


class StatOfPeriodChart(BaseChart):
    name = 'chart_period_stat'
    template = 'items/tags/charts/period_stat.html'

    def get_panel_context(self, *args, **kwargs):
        arguments = super(StatOfPeriodChart, self).get_panel_context(*args, **kwargs)

        q = MeasuringInstrument.objects.checking_stat_per_organization_and_type(kwargs.get('period_days', 31),
                                                                                kwargs.get('lookup_period_start', None))
        groups = list(q)

        types = []
        for group in groups:
            name = group['type__kind__name'] + ' ' + group['type__name']
            if name not in types:
                types.append(name)

        data = {}
        for group in groups:
            org = group['type__checking_organization__name']
            mi_type = types.index(group['type__kind__name'] + ' ' + group['type__name'])
            mi_count_in_org = group['type__checking_organization__count']
            if org not in data:
                # init types counts of instruments to check
                data[org] = [0] * len(types)

            data[org][mi_type] = mi_count_in_org

        series = [{'name': key, 'data': data[key]} for key in data]  # formatting for hightcharts

        arguments['series'] = mark_safe(json.dumps(series, ensure_ascii=False))
        arguments['categories'] = mark_safe(json.dumps(types, ensure_ascii=False))
        return arguments


register.tag(StatOfPeriodChart)
