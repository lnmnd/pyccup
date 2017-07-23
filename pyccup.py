import xml.dom.minidom as minidom


_void_elements = set([
    'area',
    'base',
    'br',
    'col',
    'embed',
    'hr',
    'img',
    'input',
    'keygen',
    'link',
    'meta',
    'param',
    'source',
    'track',
    'wbr',
])


class _SafeText:
    def __init__(self, text):
        self.text = text


def _text_node(doc, content):
    return doc.createTextNode(content), []


def _safe_text(_, content):
    return minidom.parseString(content.text).documentElement, []


def _set_attributes(element, attributes):
    for k, v in attributes.items():
        element.setAttribute(k, v)


def _tag_and_attrs(sweet_tag):
    if '#' in sweet_tag and '.' in sweet_tag:
        tag, rest = sweet_tag.split('#')
        id_, *classes = rest.split('.')
        return tag, {
            'id': id_,
            'class': ' '.join(classes),
        }
    elif '#' in sweet_tag:
        tag, id_ = sweet_tag.split('#')
        return tag, {
            'id': id_,
        }
    elif '.' in sweet_tag:
        tag, *classes = sweet_tag.split('.')
        return tag, {
            'class': ' '.join(classes),
        }
    else:
        return sweet_tag, {}


def _element(doc, content):
    sweet_tag, *rest = content
    tag, attrs = _tag_and_attrs(sweet_tag)
    el = doc.createElement(tag)
    _set_attributes(el, attrs)

    if len(rest) > 0 and isinstance(rest[0], dict):
        attrs, *children = rest
        _set_attributes(el, attrs)
    else:
        children = rest[0:]

    if tag not in _void_elements and not children:
        children = ['']

    return el, children


_node_funs = [
    [str,       _text_node],
    [_SafeText, _safe_text],
    [list,      _element],
]


class _NodeContainer:
    def appendChild(self, child):
        self.root = child


def _node_fun(content, doc):
    for type_, fun in _node_funs:  # pragma: no branch
        if isinstance(content, type_):
            return fun(doc, content)


def _node(content):
    impl = minidom.getDOMImplementation()
    doc = impl.createDocument(None, 'html', None)
    container = _NodeContainer()
    children = [(container, content)]
    while children:
        new_children = []
        for parent, content in children:
            node, cs = _node_fun(content, doc)
            parent.appendChild(node)
            new_children.extend([(node, child) for child in cs])
        children = new_children
    return container.root


def html(content):
    """
    Converts content to html string.

    >>> html(['span', {'class': 'important'}, 'hi'])
    '<span class="important">hi</span>'
    """
    return _node(content).toxml()


def safe(text):
    """
    Creates safe text (not escaped).

    >>> html(safe('<span>hi</span>'))
    '<span>hi</span>'
    """
    return _SafeText(text)
