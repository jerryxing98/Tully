from django import template
register = template.Library()
from account.models import Profile
from friendship.models import Friend,Follow
from django.db.models import Q
@register.filter(name='is_fans')
def is_fans(value, ex_username):
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


@register.inclusion_tag('userena/profile_list.html',takes_context = True)
def followers_following(context,user):
    """
    Simple tag to grab all friends
    """
    return {'user':context['user'],'profile_list': Profile.objects.get_profile_list(set(Follow.objects.followers(user))&set(Follow.objects.following(user)))}


@register.inclusion_tag('userena/profile_list.html',takes_context = True)
def followers(context,user):
    """
    Simple tag to grab all followers
    """
    return {'user':context['user'],'profile_list': Profile.objects.get_profile_list(Follow.objects.followers(user))}


@register.inclusion_tag('userena/profile_list.html',takes_context = True)
def following(context,user):
    """
    Simple tag to grab all users who follow the given user
    """
    return {'user':context['user'],'profile_list': Profile.objects.get_profile_list(Follow.objects.following(user))}


@register.inclusion_tag('userena/profile_list.html',takes_context = True)
def user_lists(context,user):
    return {'user':context['user'],'profile_list': Profile.objects.get_visible_profiles().exclude(Q(user = user))}




