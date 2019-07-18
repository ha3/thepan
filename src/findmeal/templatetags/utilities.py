"""
This is a heavily edited version of a custom template tag which I found at
https://www.silviogutierrez.com/blog/smarter-django-url-tag/
"""

from django import template
from django.template.defaulttags import URLNode, url as url_tag

register = template.Library()

@register.tag
def url(parser, token):
    validator = url_tag(parser, token)
    return SmartURLNode(validator.view_name, validator.args, validator.kwargs, validator.asvar)

class SmartURL(str):
    # This is a wrapper class that allows us to attach attributes to strings.
    pass

class SmartURLNode(URLNode):
    def render(self, context):
        view_name = self.view_name.resolve(context)
        view_name_string = "'%s'" % view_name

        #If it is a hard-coded url, strip it from the commas and assign it to context variable
        if len(view_name_string) >= 3 and view_name_string[0] == view_name_string[-1] and view_name_string[0] in ('"', "'") and view_name_string[1] == '/':
            context[self.asvar] = view_name_string[1:-1]

        # If not, use the standard url logic.
        else:
            super(SmartURLNode, self).render(context)

        resolved_url = SmartURL(context[self.asvar])
        request = context.get('request', None)

        if request:
            '''
            If the request path matches the url exactly,
            'active' attr is set as 'active' on the resolved_url instance.
            '''
            if resolved_url == request.path:
                resolved_url.active = 'active'
            else:
                resolved_url.active = ''

            '''
            If the request path starts with the url,
            'active_root' attr is set as 'active' on the resolved_url instance.
            '''
            if request.path.startswith(resolved_url):
                resolved_url.active_root = 'active'
            else:
                resolved_url.active_root = ''

        context[self.asvar] = resolved_url
        return ''
