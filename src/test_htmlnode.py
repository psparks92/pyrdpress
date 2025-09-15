import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("<h1>", "header", None, {"key1":"value1","key2":"value2"})
        node2 = HTMLNode("tag", "value", "children", "none")
        self.assertNotEqual(node, node2)

    def test_print(self):
        node = HTMLNode("<h1>", "header", None, {"key1":"value1","key2":"value2"})
        #print(node)
        self.assertNotEqual(node, None)


    
if __name__ == "__main__":
    unittest.main()
