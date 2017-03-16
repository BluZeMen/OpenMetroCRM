from classytags.arguments import Argument, MultiKeywordArgument
from classytags.core import Tag, Options
from django import template

register = template.Library()


class BasePanel(Tag):
    def render_tag(self, context, **kwargs):
        nodelist = kwargs.pop('nodelist')
        body = nodelist.render(context)

        panel_context = self.get_panel_context(kwargs)
        panel_context['body'] = body

        t = template.loader.get_template(self.template)
        c = template.Context(kwargs)

        return t.render(c)

    def get_panel_context(self, arguments):
        """
            Override this method if need to use fancy arguments,
            e.g: MultiKeywordArgument
        """
        return arguments


class Panel(BasePanel):
    name = 'panel'
    template = 'tags/panel.html'
    options = Options(
        Argument('title'),
        MultiKeywordArgument('kw', required=False),
        blocks=[('endpanel', 'nodelist')],
    )

    def get_panel_context(self, arguments):
        kw = arguments.pop('kw')
        arguments['state'] = kw.get('state', 'default')
        arguments['icon'] = kw.get('icon', 'fa-cube')
        return arguments


register.tag(Panel)


# class Chart(BasePanel):
#     name = 'chart'
#     template = 'tags/chart.html'
#     options = Options(
#         Argument('container_id'),
#         MultiKeywordArgument('kw', required=False),
#         blocks=[('endchart', 'nodelist')],
#     )
#
#     def get_panel_context(self, arguments):
#         kw = arguments.pop('kw')
#         arguments['style'] = kw.get('style', 'min-width: 310px; height: 400px; margin: 0 auto')
#         return arguments
