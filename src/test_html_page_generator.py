import unittest
from html_page_generator import *

class Test_Html_Page_Generator(unittest.TestCase):
    def test_extract_title_1(self):
        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
        """
        title = extract_title(md)
        self.assertEqual(title, "Tolkien Fan Club")

    def test_extract_title_2(self):
        md = """
![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

# Tolkien Fan Club
        """
        title = extract_title(md)
        self.assertEqual(title, "Tolkien Fan Club")

    def test_extract_title_3(self):
        md = """
## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy

###### My favorite characters (in order)
##### My favorite characters (in order)
#### My favorite characters (in order)
### My favorite characters (in order)
# Tolkien Fan Club
        """
        title = extract_title(md)
        self.assertEqual(title, "Tolkien Fan Club")