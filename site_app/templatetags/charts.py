from classytags.arguments import Argument, MultiKeywordArgument
from classytags.core import Options
from django import template

from .panels import BasePanel

register = template.Library()


class BaseChart(BasePanel):
    name = 'chart'
    template = 'tags/chart.html'
    options = Options(
        Argument('container_id'),
        MultiKeywordArgument('kw', required=False),
        blocks=[('endchart', 'nodelist')],
    )
    DEFAULT_STYLES = 'min-width: 310px; height: 400px; margin: 0 auto'

    def get_panel_context(self, arguments):
        kw = arguments.pop('kw')
        arguments['style'] = kw.get('style', self.DEFAULT_STYLES)
        return arguments


register.tag(BaseChart)


