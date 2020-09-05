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


class TestEmbeddedImageMdlinkToStandarizedImageMdLink(unittest.TestCase):
    def test_internal_mdlink_to_standarizedinternal_mdlink(self):
        # Embedded Image with title but no path
        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("![optional title](some%20image.png)")
        self.assertEqual(result, "![[some image.png]](some%20image.png)")

        # Embedded Image with title and path
        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("![optional title](/path/to/some%20image.png)")
        self.assertEqual(result, "![[some image.png]](/path/to/some%20image.png)")

        # Embedded Image with no title and no path
        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("![](some%20image.png)")
        self.assertEqual(result, "![[some image.png]](some%20image.png)")

        # Embedded Image with no title and path
        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("![](/path/to/some%20image.png)")
        self.assertEqual(result, "![[some image.png]](/path/to/some%20image.png)")

        # -------- Same tests but without url encoding ------------------------------

        # Embedded Image with title but no path
        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("![optional title](some image.png)")
        self.assertEqual(result, "![[some image.png]](some%20image.png)")

        # Embedded Image with title and path
        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("![optional title](/path/to/some image.png)")
        self.assertEqual(result, "![[some image.png]](/path/to/some%20image.png)")

        # Embedded Image with no title and no path
        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("![](some image.png)")
        self.assertEqual(result, "![[some image.png]](some%20image.png)")

        # Embedded Image with no title and path
        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("![](/path/to/some image.png)")
        self.assertEqual(result, "![[some image.png]](/path/to/some%20image.png)")

        # Not a MD Link
        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("Not a link here")
        self.assertEqual(result, False)

class TestInternalMdlinkToStandarizedInternalMdLink(unittest.TestCase):
    def test_mdlink_to_wikilink(self):
        # Internal link with title but no path
        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("[A note](some%20file.md)")
        self.assertEqual(result, "[[some file.md]](some%20file.md)")

        # Internal link with title and path
        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("[A note](/path/to/some%20file.md)")
        self.assertEqual(result, "[[some file.md]](/path/to/some%20file.md)")

        # -------- Same tests but without url encoding ------------------------------

        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("[A note](some file.md)")
        self.assertEqual(result, "[[some file.md]](some%20file.md)")

        # Internal link with title and path
        result = link_standarizer.internal_mdlink_to_standarizedinternal_mdlink("[A note](/path/to/some file.md)")
        self.assertEqual(result, "[[some file.md]](/path/to/some%20file.md)")


class TestLinkType(unittest.TestCase):
    def test_link_type(self):
        # 'urlmdlink': Markdown url link i.e. [title](url)
        result = link_standarizer.link_type("[Somefile link](https://go.to/somefile.html)")
        self.assertEqual(result, 'urlmdlink')

        result = link_standarizer.link_type("![Embedded url image](https://go.to/somefile.png)")
        self.assertEqual(result, 'urlmdlink')

        # 'internalmdlink': Markdown internal link ie. [title](path/to/mdfile.md)
        result = link_standarizer.link_type("![](/path/to/some%20image.png)")
        self.assertEqual(result, 'internalmdlink')

        result = link_standarizer.link_type("![Image Title](/path/to/some%20image.png)")
        self.assertEqual(result, 'internalmdlink')

        result = link_standarizer.link_type("![MD File](/path/to/MD%20File.md)")
        self.assertEqual(result, 'internalmdlink')

        # 'ahreflink': HTML formatted link i.e. <a href='url'>title</a>
        result = link_standarizer.link_type("<a href='url'>title</a>")
        self.assertEqual(result, 'ahreflink')

        # 'wikilink': Extended markdown wikilink without md extension i.e. [[mdfile]]
        result = link_standarizer.link_type("![[image file.png]]")
        self.assertEqual(result, "wikilink")

        result = link_standarizer.link_type("[[MD File]]")
        self.assertEqual(result, "wikilink")

        # 'standardizedinternalmdlink': Internal markdown link wikilink-compatible i.e. [[mdfile]](/path/to/mdfile.md)
        result = link_standarizer.link_type("[[MD File]](path/to/MD%20File.md)")
        self.assertEqual(result, "standardizedinternalmdlink")

        # Embedded standardizedinternalmdlink (transclusion)
        result = link_standarizer.link_type("![[MD File]](path/to/MD%20File.md)")
        self.assertEqual(result, "standardizedinternalmdlink")

        # False: No link detected
        result = link_standarizer.link_type("This does *not* have any links here")
        self.assertEqual(result, False)


class TestAnyLinkToStandarizedLink(unittest.TestCase):
    def test_anylink_to_standarizedmdlink(self):
        result = link_standarizer.anylink_to_standarizedmdlink("![[MD File]](path/to/MD%20File.md)")
        self.assertEqual(result, "![[MD File]](path/to/MD%20File.md)")

        # Embedded Image with title but no path
        result = link_standarizer.anylink_to_standarizedmdlink("![optional title](some%20image.png)")
        self.assertEqual(result, "![[some image.png]](some%20image.png)")

        # Embedded Image with title and path
        result = link_standarizer.anylink_to_standarizedmdlink(
            "![optional title](/path/to/some%20image.png)")
        self.assertEqual(result, "![[some image.png]](/path/to/some%20image.png)")

        # Embedded Image with no title and no path
        result = link_standarizer.anylink_to_standarizedmdlink("![](some%20image.png)")
        self.assertEqual(result, "![[some image.png]](some%20image.png)")

        # Embedded Image with no title and path
        result = link_standarizer.anylink_to_standarizedmdlink("![](/path/to/some%20image.png)")
        self.assertEqual(result, "![[some image.png]](/path/to/some%20image.png)")

        # -------- Same tests but without url encoding ------------------------------

        # Embedded Image with title but no path
        result = link_standarizer.anylink_to_standarizedmdlink("![optional title](some image.png)")
        self.assertEqual(result, "![[some image.png]](some%20image.png)")

        # Embedded Image with title and path
        result = link_standarizer.anylink_to_standarizedmdlink(
            "![optional title](/path/to/some image.png)")
        self.assertEqual(result, "![[some image.png]](/path/to/some%20image.png)")

        # Embedded Image with no title and no path
        result = link_standarizer.anylink_to_standarizedmdlink("![](some image.png)")
        self.assertEqual(result, "![[some image.png]](some%20image.png)")

        # Embedded Image with no title and path
        result = link_standarizer.anylink_to_standarizedmdlink("![](/path/to/some image.png)")
        self.assertEqual(result, "![[some image.png]](/path/to/some%20image.png)")

        # Not a MD Link
        result = link_standarizer.anylink_to_standarizedmdlink("Not a link here")
        self.assertEqual(result, False)

        # -------------

        # Internal link with title but no path
        result = link_standarizer.anylink_to_standarizedmdlink("[A note](some%20file.md)")
        self.assertEqual(result, "[[some file.md]](some%20file.md)")

        # Internal link with title and path
        result = link_standarizer.anylink_to_standarizedmdlink("[A note](/path/to/some%20file.md)")
        self.assertEqual(result, "[[some file.md]](/path/to/some%20file.md)")

        # -------- Same tests but without url encoding ------------------------------

        result = link_standarizer.anylink_to_standarizedmdlink("[A note](some file.md)")
        self.assertEqual(result, "[[some file.md]](some%20file.md)")

        # Internal link with title and path
        result = link_standarizer.anylink_to_standarizedmdlink("[A note](/path/to/some file.md)")
        self.assertEqual(result, "[[some file.md]](/path/to/some%20file.md)")


class TestAhrefLinkSplit(unittest.TestCase):
    def test_ahreflink_split(self):
        # 'ahreflink': HTML formatted link i.e. <a href='url'>title</a>
        result = link_standarizer.ahreflink_split("<a href='https://go.to/somefile.html'>title</a>")
        self.assertEqual(result, {
            'Title': 'title',
            'Url': 'https://go.to/somefile.html',
            'Class': ''
        })

        result = link_standarizer.ahreflink_split("<a href='https://go.to/somefile%20with%20space.html'>Another title</a>")
        self.assertEqual(result, {
            'Title': 'Another title',
            'Url': 'https://go.to/somefile%20with%20space.html',
            'Class': ''
        })

        # a href link to internal attachment
        result = link_standarizer.ahreflink_split("<a href='attachments/document.pdf'>PDF Document</a>")
        self.assertEqual(result, {
            'Title': 'PDF Document',
            'Url': 'attachments/document.pdf',
            'Class': ''
        })

        result = link_standarizer.ahreflink_split("<a href='attachments/folder%20with%20spaces/document.pdf'>PDF Document</a>")
        self.assertEqual(result, {
            'Title': 'PDF Document',
            'Url': 'attachments/folder%20with%20spaces/document.pdf',
            'Class': ''
        })

if __name__ == '__main__':
    unittest.main()
