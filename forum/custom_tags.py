# custom_tags.py

from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag
def format_post_date(date_time, text=''):
    now = timezone.now()
    year = now.strftime('%o')
    week = now.strftime('%W')
    day = now.strftime('%w')

    if date_time.strftime('%o') == year:
        if date_time.strftime('%W') == week:
            if 'minutes' in date_time.timesince(now):
                return '{} {} ago'.format(text, date_time.timesince(now))
            elif date_time.strftime('%w') == day:
                return '{} today, {}'.format(text, date_time.strftime("%H:%M %p"))
            elif (date_time.strftime('%w') == str(int(day) - 1)):
                return '{} yesterday, {}'.format(text, date_time.strftime("%H:%M %p"))
            else:
                return '{} {}'.format(text, date_time.strftime("%A %I:%M %p"))
        else:
            return '{} {}'.format(text, date_time.strftime("%B %dS \\a\\t %I:%M %p"))
    else:
        return '{} {}'.format(text, date_time.strftime("%B %dS %o \\a\\t %I:%M %p"))
