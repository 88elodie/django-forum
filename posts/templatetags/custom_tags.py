# custom_tags.py

from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag
def format_post_date(post_date, text=''):
    if not post_date:
        return ''

    now = timezone.now()
    year = now.strftime('%o')
    week = now.strftime('%W')
    day = now.strftime('%w')

    print(type(post_date))

    if post_date.strftime('%o') == year:
        if post_date.strftime('%W') == week:
            if 'minutes' in post_date.timesince(now):
                return '{} {} ago'.format(text, post_date.timesince(now))
            elif post_date.strftime('%w') == day:
                return '{} today, {}'.format(text, post_date.strftime("%H:%M %p"))
            elif (post_date.strftime('%w') == str(int(day) - 1)):
                return '{} yesterday, {}'.format(text, post_date.strftime("%H:%M %p"))
            else:
                return '{} {}'.format(text, post_date.strftime("%A %I:%M %p"))
        else:
            return '{} {}'.format(text, post_date.strftime("%B %dS \\a\\t %I:%M %p"))
    else:
        return '{} {}'.format(text, post_date.strftime("%B %dS %o \\a\\t %I:%M %p"))
