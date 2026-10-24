from __future__ import annotations

import unittest

from v03_test_helpers import SCRIPTS_DIR  # noqa: F401

from research_agenda_common import detect_domains


class DomainDetectionTest(unittest.TestCase):
    def test_negated_dlo_context_does_not_tag_dlo(self) -> None:
        domains = detect_domains("This paper does not evaluate DLO or rope manipulation.", [])
        self.assertNotIn("DLO", domains)

        domains = detect_domains("论文没做 DLO，也未验证线缆整理。", [])
        self.assertNotIn("DLO", domains)

    def test_positive_dlo_context_still_tags_dlo(self) -> None:
        domains = detect_domains("The method targets bimanual DLO manipulation with tactile feedback.", [])
        self.assertIn("DLO", domains)
        self.assertIn("bimanual", domains)
        self.assertIn("tactile", domains)

    def test_explicit_tag_still_adds_domain(self) -> None:
        self.assertIn("DLO", detect_domains("not evaluated on ropes", ["DLO"]))


if __name__ == "__main__":
    unittest.main()
