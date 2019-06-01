from django import template
from django.template.defaulttags import URLNode, url as url_tag

register = template.Library()

@register.tag
def url(parser, token):
    validator = url_tag(parser, token)
    return SmartURLNode(validator.view_name, validator.args, validator.kwargs, validator.asvar)

class SmartURL(str):
    pass

class SmartURLNode(URLNode):
    def render(self, context):
        resolved_view_name = self.view_name.resolve(context)

        if resolved_view_name:
            view_name_string = "'%s'" % resolved_view_name
        else:
            view_name_string = unicode(self.view_name)

        if len(view_name_string) >= 3 and view_name_string[0] == view_name_string[-1] and view_name_string[0] in ('"', "'") and view_name_string[1] == '/':
            rendered = view_name_string[1:-1]

            if self.asvar:
                context[self.asvar] = rendered

        else:
            rendered = super(SmartURLNode, self).render(context)

        if not self.asvar:
            return rendered

        else:
            resolved_url = SmartURL(context[self.asvar])
            request = context.get('request', None)

            if request:
                # Step 7
                if resolved_url == request.path:
                    resolved_url.active = 'active'
                else:
                    resolved_url.active = ''

                if request.path.startswith(resolved_url):
                    resolved_url.active_root = 'active'
                else:
                    resolved_url.active_root = ''

            context[self.asvar] = resolved_url
            return ''
