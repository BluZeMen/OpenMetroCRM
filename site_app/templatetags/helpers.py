from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_put2get(context, field, value):
    get_params = context['request'].GET.copy()
    get_params[field] = value
    return get_params.urlencode()


@register.inclusion_tag('tags/pagination.html', takes_context=True)
def pagination(context, url_name, **kwargs):
    if not context.get('is_paginated', False):
        return {}

    current_number = context['page_obj'].number;
    num_pages = context['page_obj'].paginator.num_pages;
    num_sibling_pages = kwargs.get('num_sibling', 0)
    pages = range(current_number - num_sibling_pages, current_number + num_sibling_pages + 1)
    pages = [p for p in pages if 0 <= p < num_pages]

    return {
        'pages': pages,
        'request': context['request'],
        'page_obj': context['page_obj'],
        'is_paginated': context['is_paginated'],
        'url_name': url_name
    }


