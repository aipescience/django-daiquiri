from markdown import markdown as markdown_function

from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from ..utils import get_internal_link

register = template.Library()


@register.simple_tag(takes_context=True)
def internal_link(context, text, name, *args, **kwargs):
    if 'permission' in kwargs:
        if kwargs['permission'] == 'login_required':
            if not context.request.user.is_authenticated():
                return ''
        else:
            if not context.request.user.has_perm(kwargs['permission']):
                return ''
        del kwargs['permission']

    return get_internal_link(text, name, *args, **kwargs)


@register.simple_tag(takes_context=True)
def admin_link(context):
    if not context.request.user.is_superuser:
        return ''

    return get_internal_link('Admin', 'admin:index')


@register.simple_tag(takes_context=True)
def login_link(context):
    if context.request.user.is_authenticated():
        return '<a href=\"%s\">%s</a>' % (settings.LOGOUT_URL, _('Logout'))
    else:
        return '<a href=\"%s\">%s</a>' % (settings.LOGIN_URL, _('Login'))


@register.simple_tag()
def horizontal_form(form):
    return render_to_string('core/horizontal_form.html', {'form': form})


@register.filter(name='next')
def next(value, arg):
    try:
        return value[int(arg)+1]
    except:
        return None


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    return mark_safe(markdown_function(force_text(value)))
