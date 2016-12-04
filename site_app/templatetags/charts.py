import json

from django import template
from classytags.core import Options
from classytags.arguments import Argument, MultiKeywordArgument

from .panels import BasePanel


register = template.Library()


class Chart(BasePanel):

    name = 'chart'
    template = 'tags/chart.html'
    options = Options(
        Argument('container_id'),
        MultiKeywordArgument('kw', required=False),
        blocks=[('endchart', 'nodelist')],
    )

    def get_panel_context(self, arguments):
        kw = arguments.pop('kw')
        arguments['style'] = kw.get('style', 'min-width: 310px; height: 400px; margin: 0 auto')
        return arguments

register.tag(Chart)


