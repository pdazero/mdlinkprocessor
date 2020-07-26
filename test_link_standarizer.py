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

class TestEmbeddedImageMdlinkToWikiLink(unittest.TestCase):
    def test_mdlink_to_wikilink(self):
        result = link_standarizer.mdlink_to_wikilink("![optional title](some%20image.png)")
        self.assertEqual(result, "![[optional title]](some%20image.png)")

if __name__ == '__main__':
    unittest.main()
