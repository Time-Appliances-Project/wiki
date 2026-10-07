"""Check section isolation and fail-safe publication."""
import unittest
from sync_wiki_sections import SECTIONS, render


class SectionPublicationTests(unittest.TestCase):
    def setUp(self):
        self.pages = {page: f'Updated {page}' for page in SECTIONS.values()}
        self.home = 'Unrelated introduction\n'
        for section in SECTIONS:
            self.home += (f'### {section}\n<!-- BEGIN SECTION: {section} -->\n'
                          f'Old content\n<!-- END SECTION: {section} -->\n')
        self.home += 'Unrelated calendar and references\n'

    def test_preserves_everything_outside_sections(self):
        updated = render(self.home, self.pages)
        expected = self.home
        for page in SECTIONS.values():
            expected = expected.replace('\nOld content\n', f'\n\nUpdated {page}\n\n', 1)
        self.assertEqual(updated, expected)
        self.assertEqual(render(updated, self.pages), updated)

    def test_missing_duplicate_or_reversed_markers_fail(self):
        marker = '<!-- BEGIN SECTION: upcoming-calls -->'
        for broken in (self.home.replace(marker, ''), self.home + marker,
                       self.home.replace(marker, '<!-- END SECTION: upcoming-calls -->', 1)):
            with self.assertRaises(ValueError):
                render(broken, self.pages)

    def test_empty_missing_or_nested_source_fails(self):
        for bad in ('', '   ', '<!-- BEGIN SECTION: upcoming-calls -->'):
            with self.assertRaises(ValueError):
                render(self.home, dict(self.pages, **{'Upcoming-Calls': bad}))
        with self.assertRaises(KeyError):
            render(self.home, {})


if __name__ == '__main__':
    unittest.main()
