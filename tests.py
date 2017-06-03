from unittest import TestCase

from pyccup import html, safe


class HtmlTestCase(TestCase):
    def t(self, input_, output):
        self.assertEqual(html(input_), output)

    def test_text_node(self):
        self.t('hi',
               'hi')

    def test_text_node_escaped_html(self):
        self.t('<strong>hi</strong>',
               '&lt;strong&gt;hi&lt;/strong&gt;')

    def test_safe_html(self):
        self.t(safe('<strong>hi</strong>'),
               '<strong>hi</strong>')

    def test_element(self):
        self.t(['br'],
               '<br/>')

    def test_child(self):
        self.t(['p', 'hi'],
               '<p>hi</p>')

    def test_attributes(self):
        self.t(['br', {'id': 'i', 'class': 'c'}],
               '<br class="c" id="i"/>')

    def test_attributes_and_child(self):
        self.t(['p', {'class': 'c'}, 'hi'],
               '<p class="c">hi</p>')

    def test_children(self):
        self.t(['div',
                ['p', ['span', 'hi']],
                ['p', 'hello']],
               '<div><p><span>hi</span></p><p>hello</p></div>')

    def test_id(self):
        self.t(['p#i', 'hi'],
               '<p id="i">hi</p>')

    def test_class(self):
        self.t(['p.c', 'hi'],
               '<p class="c">hi</p>')

    def test_classes(self):
        self.t(['p.c1.c2', 'hi'],
               '<p class="c1 c2">hi</p>')

    def test_id_and_classes(self):
        self.t(['p#i.c1.c2', 'hi'],
               '<p class="c1 c2" id="i">hi</p>')
