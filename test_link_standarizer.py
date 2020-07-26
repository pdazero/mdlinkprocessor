import unittest
import link_standarizer


class TestWikiLinkToMdlink(unittest.TestCase):
    def test_wikilink_to_mdlink(self):
        result = link_standarizer.wikilink_to_mdlink("[[MD File]]")
        self.assertEqual(result, "[[MD File]](MD%20File.md)")


class TestEmbeddedImageWikiLinkToMdlink(unittest.TestCase):
    def test_wikilink_to_mdlink(self):
        result = link_standarizer.wikilink_to_mdlink("![[image file.png]]")
        self.assertEqual(result, "![[image file.png]](image%20file.png)")


class TestMdlinkSplit(unittest.TestCase):
    def test_mdlink_split(self):
        # Embedded Image with title but no path
        result = link_standarizer.mdlink_split("![optional title](some%20image.png)")
        self.assertEqual(result, {
            'Embedded': '!',
            'Title': 'optional title',
            'Path': '',
            'Filename': 'some%20image.png'
        })

        # Embedded Image with title and path
        result = link_standarizer.mdlink_split("![optional title](/path/to/some%20image.png)")
        self.assertEqual(result, {
            'Embedded': '!',
            'Title': 'optional title',
            'Path': '/path/to/',
            'Filename': 'some%20image.png'
        })

        # Embedded Image with no title and no path
        result = link_standarizer.mdlink_split("![](some%20image.png)")
        self.assertEqual(result, {
            'Embedded': '!',
            'Title': '',
            'Path': '',
            'Filename': 'some%20image.png'
        })

        # Embedded Image with no title and path
        result = link_standarizer.mdlink_split("![](/path/to/some%20image.png)")
        self.assertEqual(result, {
            'Embedded': '!',
            'Title': '',
            'Path': '/path/to/',
            'Filename': 'some%20image.png'
        })

        # 'urlmdlink': Markdown url link i.e. [title](url)
        result = link_standarizer.mdlink_split("[Somefile link](https://go.to/somefile.html)")
        self.assertEqual(result, {
            'Embedded': '',
            'Title': 'Somefile link',
            'Url': 'https://go.to/somefile.html',
        })

        result = link_standarizer.mdlink_split("![Embedded url image](https://go.to/somefile.png)")
        self.assertEqual(result, {
            'Embedded': '!',
            'Title': 'Embedded url image',
            'Url': 'https://go.to/somefile.png',
        })


class TestEmbeddedImageMdlinkToWikiLink(unittest.TestCase):
    def test_mdlink_to_wikilink(self):
        # Embedded Image with title but no path
        result = link_standarizer.mdlink_to_wikilink("![optional title](some%20image.png)")
        self.assertEqual(result, "![[optional title]](some%20image.png)")

        # Embedded Image with title and path
        result = link_standarizer.mdlink_to_wikilink("![optional title](/path/to/some%20image.png)")
        self.assertEqual(result, "![[optional title]](/path/to/some%20image.png)")

        # Embedded Image with no title and no path
        result = link_standarizer.mdlink_to_wikilink("![](some%20image.png)")
        self.assertEqual(result, "![[]](some%20image.png)")

        # Embedded Image with no title and path
        result = link_standarizer.mdlink_to_wikilink("![](/path/to/some%20image.png)")
        self.assertEqual(result, "![[]](/path/to/some%20image.png)")

class TestLinkType(unittest.TestCase):
    def test_link_type(self):
        # 'urlmdlink': Markdown url link i.e. [title](url)
        result = link_standarizer.link_type("[Somefile link](https://go.to/somefile.html)")
        self.assertEqual(result, 'urlmdlink')

        result = link_standarizer.link_type("![Embedded url image](https://go.to/somefile.png)")
        self.assertEqual(result, 'urlmdlink')

        # 'internalmdlink': Markdown internal link ie. [titile](path/to/mdfile.md)
        result = link_standarizer.link_type("![](/path/to/some%20image.png)")
        self.assertEqual(result, 'internalmdlink')

        result = link_standarizer.link_type("![Image Title](/path/to/some%20image.png)")
        self.assertEqual(result, 'internalmdlink')

        result = link_standarizer.link_type("![MD File](/path/to/MD%20File.md)")
        self.assertEqual(result, 'internalmdlink')

        result = link_standarizer.link_type("![[MD File]](/path/to/MD%20File.md)")
        self.assertEqual(result, 'internalmdlink')

        # 'ahreflink': HTML formatted link i.e. <a href='url'>title</a>
        result = link_standarizer.link_type("![[MD File]](/path/to/MD%20File.md)")
        self.assertEqual(result, 'internalmdlink')

        # 'wikilink': Extended markdown wililink i.e. [[mdfile]] (without .md extension)
        result = link_standarizer.link_type("![[image file.png]]")
        self.assertEqual(result, "wikilink")

        result = link_standarizer.link_type("[[MD File]]")
        self.assertEqual(result, "wikilink")

        # False: No link detected
        result = link_standarizer.link_type("This does *not* have any links here")
        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()
