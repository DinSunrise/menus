from django import template
from django.db.models import Q
from django.urls import reverse
from menus.models import MenuItem
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    menu_items = MenuItem.objects.filter(parent__isnull=True)
    current_url = request.path_info
    menu_html = ''

    for item in menu_items:
        menu_html += '<li'
        if item.url == current_url or item.named_url == current_url:
            menu_html += ' class="active"'
        menu_html += '><a href="'
        if item.url:
            menu_html += item.url
        elif item.named_url:
            menu_html += reverse(item.named_url)
        menu_html += '">'
        menu_html += item.name
        menu_html += '</a>'
        if item.children.exists():
            menu_html += '<ul>'
            expanded = False
            for child in item.children.all():
                menu_html += '<li'
                if child.url == current_url or child.named_url == current_url:
                    menu_html += ' class="active"'
                    expanded = True
                menu_html += '><a href="'
                if child.url:
                    menu_html += child.url
                elif child.named_url:
                    menu_html += reverse(child.named_url)
                menu_html += '">'
                menu_html += child.name
                menu_html += '</a>'
                if child.children.exists():
                    sub_menu_html = ''
                    for sub_child in child.children.all():
                        sub_menu_html += '<li'
                        if sub_child.url == current_url or sub_child.named_url == current_url:
                            sub_menu_html += ' class="active"'
                            expanded = True
                        sub_menu_html += '><a href="'
                        if sub_child.url:
                            sub_menu_html += sub_child.url
                        elif sub_child.named_url:
                            sub_menu_html += reverse(sub_child.named_url)
                        sub_menu_html += '">'
                        sub_menu_html += sub_child.name
                        sub_menu_html += '</a></li>'
                    if expanded:
                        menu_html += '<ul class="expanded">'
                    else:
                        menu_html += '<ul>'
                    menu_html += sub_menu_html
                    menu_html += '</ul>'
            menu_html += '</ul>'
        menu_html += '</li>'
    return mark_safe(menu_html)
