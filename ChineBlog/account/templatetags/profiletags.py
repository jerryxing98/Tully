from django import template
register = template.Library()
from account.models import Profile


@register.filter(name='is_fans')
def remove(value, ex_username):
    if isinstance(value,Profile):
        return value.is_fans(ex_username)
    else:
        raise template.TemplateSyntaxError("this filter  requires Profile object")


@register.filter(name='is_follows')
def is_follows(value,ex_username):
    if isinstance(value,Profile):
        return value.is_follows(ex_username)
    else:
        raise template.TemplateSyntaxError("this filter  requires Profile object")


@register.filter(name='fans_follows')
def fans_follows(value):
    if isinstance(value,Profile):
        return value.fans_follows(ex_username)
    else:
        raise template.TemplateSyntaxError("this filter  requires Profile object")

@register.filter(name='get_follows_count')
def get_follows_count(value):
    if isinstance(value,Profile):
        return value.get_follows_count(ex_username)
    else:
        raise template.TemplateSyntaxError("this filter  requires Profile object")

@register.filter(name='get_fans_count')
def get_fans_count(value):
    if isinstance(value,Profile):
        return value.get_fans_count(ex_username)
    else:
        raise template.TemplateSyntaxError("this filter  requires Profile object")


@register.filter(name='get_info')
def get_info(value):
    if isinstance(value,Profile):
        return value.get_info(ex_username)
    else:
        raise template.TemplateSyntaxError("this filter  requires Profile object")