import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("b", "Hello, world with props!", {"key1":"value1","key2":"value2"})
        self.assertEqual(node.to_html(), "<b key1=\"value1\" key2=\"value2\">Hello, world with props!</b>")

if __name__ == "__main__":
    unittest.main()
