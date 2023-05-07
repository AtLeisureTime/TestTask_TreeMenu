import re
from django import template
from django.urls import reverse
import django.urls.exceptions as dj_exceptions
import django.utils.safestring as dj_safestring
import django.db.models.query as dj_query
from menu import models as menuModels


register = template.Library()
urlToTreePath = {}  # element relative url to tree menu path mapping


def generateMenuHtml(allElems: dj_query.QuerySet, parentIds: list, parentValues: list,
                     parentUrls: list, treePath: str, requestPath: str) -> str:
    """ Generate html code for the menu using recursive depth-first search algorithm
        for menu tree traversal.

    Args:
        allElems (dj_query.QuerySet): all menuModels.Element objects related to the menu
        parentIds (list): ids of parent menuModels.Element objects
        parentValues (list): values of parent menuModels.Element objects
        parentUrls (list): urls of parent menuModels.Element objects
        treePath (str): path to the parent element in the tree,
                        e.g. '/menuId/elem1Id/elem2Id'
        requestPath (str): relative url of the selected element in the tree

    Returns:
        str: menu html code
    """
    html = ''
    for parentId, parentValue, parentUrl in zip(parentIds, parentValues, parentUrls):
        childIds, childValues, childUrls = [], [], []
        parentTreePath = f'{treePath}' if parentId is None else f'{treePath}/{parentId}'
        menuId = None

        for elemId, _menuId, elemParentId, value, url, namedUrl in allElems:
            if parentId == elemParentId:
                childIds.append(elemId)
                childValues.append(value)

                if not url and namedUrl:
                    try:
                        url = reverse(namedUrl)
                    except dj_exceptions.NoReverseMatch:
                        # named url doesn't exist
                        pass

                try:
                    if url and not namedUrl:
                        # get relative url
                        url = re.search('(?:^https?://[^/]*)(/.*)', url).group(1)
                except AttributeError | IndexError:
                    # can't parse relative url
                    url = None

                childTreePath = f'{parentTreePath}/{elemId}'
                childUrl = url or childTreePath
                urlToTreePath[_menuId][childUrl] = childTreePath
                childUrls.append(childUrl)
            menuId = _menuId

        if childIds:
            innerHtml = generateMenuHtml(allElems, childIds, childValues, childUrls,
                                         parentTreePath, requestPath)

        requestTreePath = urlToTreePath[menuId].get(requestPath, None)
        liSelected = ' class="selected"' if parentTreePath == requestTreePath else ''

        if childIds:
            parentClass, childClass = "caret", "nested"
            if requestTreePath and re.search(f'^{parentTreePath}(?:/|$)', requestTreePath):
                # unfold the node
                parentClass, childClass = "caret caret-down", "nested active"

            html += f'<li><span class="{parentClass}"><a href="{parentUrl}"{liSelected}>'\
                f'{parentValue}</a></span><ul class="{childClass}">{innerHtml}</ul></li>'
        else:
            html += f'<li><a href="{parentUrl}"{liSelected}>{parentValue}</a></li>'

    return html


@register.simple_tag
def draw_menu(name: dj_safestring.SafeString, requestPath: str) -> dj_safestring.SafeText:
    """ Select all menuModels.Element objects related to the menu
        and generate menu html code.

    Args:
        name (dj_safestring.SafeString): menu name
        requestPath (str): relative url of the selected element in the tree

    Returns:
        dj_safestring.SafeText: menu html code
    """
    html = ''
    qs = menuModels.Element.objects.select_related('menu').filter(menu__name=name)
    allElems = qs.values_list()
    if allElems:
        menuId = allElems[0][1]
        menuUrl = menuTreePath = f'/{menuId}'
        urlToTreePath[menuId] = {menuUrl:  menuTreePath}
        innerHtml = generateMenuHtml(allElems, [None], [name], [menuUrl],
                                     menuTreePath, requestPath)
        html = f'<ul id="myUL">{innerHtml}</ul>'

    return dj_safestring.mark_safe(html)
