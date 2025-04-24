import unittest
from markdown_to_html import *

class Test_Markdown_to_Html(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_blockquote(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>"I am in fact a Hobbit in all but size." -- J.R.R. Tolkien</blockquote></div>',
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
- This is text that _should_ remain
- the **same** even with inline stuff
- This is text that `should` remain
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is text that <i>should</i> remain</li><li>the <b>same</b> even with inline stuff</li><li>This is text that <code>should</code> remain</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. This is text that _should_ remain
2. the **same** even with inline stuff
3. This is text that `should` remain
4. This is text that should remain
5. the same even with inline stuff
6. This is text that should remain
7. This is text that should remain
8. the same even with inline stuff
9. This is text that should remain
10. This is text that should remain
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is text that <i>should</i> remain</li><li>the <b>same</b> even with inline stuff</li><li>This is text that <code>should</code> remain</li><li>This is text that should remain</li><li>the same even with inline stuff</li><li>This is text that should remain</li><li>This is text that should remain</li><li>the same even with inline stuff</li><li>This is text that should remain</li><li>This is text that should remain</li></ol></div>",
        )

    def test_headers(self):
        md = """
### Header 3

# Header 1

## Header 2

#### Header 4

###### Header 6

##### Header 5
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Header 3</h3><h1>Header 1</h1><h2>Header 2</h2><h4>Header 4</h4><h6>Header 6</h6><h5>Header 5</h5></div>",
        )