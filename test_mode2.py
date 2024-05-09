from unittest import TestCase
from ed_utils.decorators import number, visibility

from landsites import Land

from mode2 import Mode2Navigator


class Mode2Tests(TestCase):

    def load_basic(self):
        self.a = Land("A", 400, 100)
        self.b = Land("B", 300, 150)
        self.c = Land("C", 100, 5)
        self.d = Land("D", 350, 90)
        self.e = Land("E", 300, 100)
        self.lands = [
            self.a, self.b, self.c, self.d, self.e
        ]

    @number("2.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_day(self):
        self.load_basic()

        # Used later
        cur_guardians = {
            site.name: site.guardians
            for site in self.lands
        }
        cur_gold = {
            site.name: site.gold
            for site in self.lands
        }

        nav = Mode2Navigator(8)
        nav.add_sites(self.lands)
        results = nav.simulate_day(100)

        # The first team makes 400 gold by going to Island A and sending 100 their crew.
        # Final score: 400 + 0*2.5 = 400
        # The second team makes 375 gold by going to Island D and sending 90 of their crew.
        # Final score: 350 + 10*2.5 = 375
        # The third team makes 337.5 gold by going to Island C and sending 5 of their crew.
        # Final score: 100 + 95*2.5 = 337.5
        # The fourth team makes 300 gold by going to Island E and sending 100 of their crew.
        # Final score: 300 + 0*2.5 = 300
        # The fifth, sixth, seventh, eighth teams should end up with 250 gold.
        expected_scores = [400, 375, 337.5, 300, 250, 250, 250, 250]
        self.assertEqual(len(results), len(expected_scores))

        for (site, sent_crew), expected in zip(results, expected_scores):
            
            if site is None:
                self.assertEqual(2.5 * 100, expected)
                continue
            gold = cur_gold[site.name]
            guardians = cur_guardians[site.name]
            if guardians == 0:
                received = gold
            else:
                received = min(gold, gold * sent_crew / guardians)
            # Update Island
            cur_gold[site.name] = gold - received
            cur_guardians[site.name] = max(0, guardians - sent_crew)
            # Score
            score = 2.5 * (100 - sent_crew) + received
            self.assertEqual(score, expected)

    @number("2.2")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_add_again(self):
        
        self.load_basic()

        # Used later
        cur_guardians = {
            site.name: site.guardians
            for site in self.lands
        }
        cur_gold = {
            site.name: site.gold
            for site in self.lands
        }

        nav = Mode2Navigator(3)
        nav.add_sites(self.lands)
        results_1 = nav.simulate_day(100)
        # Same first 3 decisions as test 2.1
        expected_1 = [400, 375, 337.5]
        self.assertEqual(len(results_1), len(expected_1))
        
        for (site, sent_crew), expected in zip(results_1, expected_1):
            if site is None:
                self.assertEqual(2.5 * 100, expected)
                continue
            gold = cur_gold[site.name]
            guardians = cur_guardians[site.name]
            if guardians == 0:
                received = gold
            else:
                received = min(gold, gold * sent_crew / guardians)
            # Update Island
            cur_gold[site.name]      = gold - received
            cur_guardians[site.name] = max(0, guardians - sent_crew)
            # Score
            score = 2.5 * (100 - sent_crew) + received
            self.assertEqual(score, expected)
        nav.add_sites([Land("F", 900, 150)])
        cur_guardians["F"] = 150
        cur_gold["F"] = 900
        results_2 = nav.simulate_day(100)
        # The first 2 pirates on this day can plunder island F, after which the same decisions as in test 2.1 continue
        expected_2 = [600, 425, 300]
        self.assertEqual(len(results_2), len(expected_2))
        for (site, sent_crew), expected in zip(results_2, expected_2):
            if site is None:
                self.assertEqual(2.5 * 100, expected)
                continue
            gold      = cur_gold[site.name]
            guardians = cur_guardians[site.name]
            if guardians == 0:
                received = gold
            else:
                received = min(gold, gold * sent_crew / guardians)
            # Update Island
            cur_gold[site.name] = gold - received
            cur_guardians[site.name] = max(0, guardians - sent_crew)
            # Score
            score = 2.5 * (100 - sent_crew) + received
            self.assertEqual(score, expected)
