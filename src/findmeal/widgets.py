import re

from django.forms.widgets import Widget, Select
from django.utils.safestring import mark_safe

pattern = r'(\d\d):(\d\d):(\d\d)$'

class SelectTimeWidget(Widget):
    def __init__(self, attrs=None, hour_step=None, minute_step=None):
        self.attrs = attrs or {}
        hour_step = hour_step or 1
        minute_step = minute_step or 1

        self.hours = range(0, 24, hour_step)
        self.minutes = range(0, 60, minute_step)

    def render(self, name, value, attrs=None, renderer=None):
        try:
            hour, minute = value.hour, value.minute

        except AttributeError:
            hour = minute = 0

            if isinstance(value, str):
                match = re.compile(pattern).match(value)

                if match:
                    time_groups = match.groups()
                    hour = int(time_groups[0])
                    minute = int(time_groups[1])

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = f'id_{name}'

        hour, minute = f'{hour:02}', f'{minute:02}'

        hour_choices = [(f'{i:02}', f'{i:02}') for i in self.hours]
        local_attrs = self.build_attrs({'id': f'{id_}_hour', 'title': 'Saat'})
        select_html = Select(choices=hour_choices).render(
            name=f'{name}_hour', value=hour, attrs=local_attrs)
        output.append(select_html)

        minute_choices = [(f'{i:02}', f'{i:02}') for i in self.minutes]
        local_attrs = self.build_attrs({'id': f'{id_}_minute', 'title': 'Dakika'})
        select_html = Select(choices=minute_choices).render(
            name=f'{name}_minute', value=minute, attrs=local_attrs)
        output.append(select_html)

        return mark_safe('\n'.join(output))

    def value_from_datadict(self, data, files, name):
        h = data.get(f'{name}_hour', 0)
        m = data.get(f'{name}_minute', 0)

        if (int(h) == 0 or h) and (int(m) == 0 or m):
            return f'{h}:{m}:00'

        return data.get(name, None)
