"""Run with python3 scripts/test_status_canonical.py; never writes monitoring data."""
from html.parser import HTMLParser
from pathlib import Path
import unittest


class HeadLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.canonicals = []

    def handle_starttag(self, tag, attrs):
        if tag == 'head':
            self.in_head = True
        attrs = dict(attrs)
        if tag == 'link' and 'canonical' in (attrs.get('rel') or '').split():
            self.canonicals.append((self.in_head, attrs.get('href')))

    def handle_endtag(self, tag):
        if tag == 'head':
            self.in_head = False


class CanonicalTest(unittest.TestCase):
    def test_exact_single_head_canonical(self):
        parser = HeadLinks()
        parser.feed((Path(__file__).resolve().parents[1] / 'status' / 'index.html').read_text())
        self.assertEqual(parser.canonicals, [(True, 'https://status.datarakyat.id/')])


if __name__ == '__main__':
    unittest.main()
