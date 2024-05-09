from unittest import TestCase
from ed_utils.decorators import number, visibility

from landsites import Land
from mode1 import Mode1Navigator


class Mode1Tests(TestCase):

    def load_basic(self):
        self.a = Land("A", 400, 100)
        self.b = Land("B", 300, 150)
        self.c = Land("C", 100, 5)
        self.d = Land("D", 350, 90)
        self.e = Land("E", 300, 100)
        # Create deepcopies of the islands
        self.lands = [
            Land(self.a.name, self.a.gold, self.a.guardians),
            Land(self.b.name, self.b.gold, self.b.guardians),
            Land(self.c.name, self.c.gold, self.c.guardians),
            Land(self.d.name, self.d.gold, self.d.guardians),
            Land(self.e.name, self.e.gold, self.e.guardians),
        ]

    def check_solution(self, lands, starting_adv, solution, optimal):
        current_money = 0
        current_crew = starting_adv
        for site, crew_sent in solution:
            self.assertGreaterEqual(crew_sent, 0)
            # This assertIn is written so that we allow copies with the same properties to be considered equal.
            self.assertIn((site.name, site.gold, site.guardians), [(i.name, i.gold, i.guardians) for i in lands])
            current_money += min(site.gold * crew_sent / site.guardians, site.gold)
            current_crew -= crew_sent
            self.assertGreaterEqual(current_crew, 0)
        self.assertFalse(current_money < optimal, "Your island selection is suboptimal!")
        if current_money > optimal:
            raise ValueError("ERROR! You somehow made more money than the intended solution")

    @number("1.1")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic(self):
        self.load_basic()
        nav = Mode1Navigator(self.lands, 200)
        selected = nav.select_sites()
        expected_money = 865
        # ^ This can be achieved with ^
        # A: 100 Crew
        # B: 0 Crew
        # C: 5 Crew
        # D: 90 Crew
        # E: 5 Crew
        self.check_solution(self.lands, 200, selected, expected_money)
        # So we must be equal :)

    @number("1.2")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_big_crew(self):
        self.load_basic()
        nav = Mode1Navigator(self.lands, 500)
        selected = nav.select_sites()
        expected_money = 1450
        # ^ This can be achieved with ^
        # A: 100 Marines
        # B: 150 Marines
        # C: 5 Marines
        # D: 90 Marines
        # E: 100 Marines
        self.check_solution(self.lands, 500, selected, expected_money)

    @number("1.3")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_no_crew(self):
        self.load_basic()
        nav = Mode1Navigator(self.lands, 0)
        selected = nav.select_sites()
        # If you did return any islands, you shouldn't have sent anyone.
        for site, crew_sent in selected:
            self.assertEqual(crew_sent, 0)

    @number("1.4")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_repeats(self):
        # choice function should not modify the outcome or the islands.
        self.load_basic()
        nav = Mode1Navigator(self.lands, 200)
        selected = nav.select_sites()
        selected_again = nav.select_sites()
        self.check_solution(self.lands, 200, selected, 865)
        self.check_solution(self.lands, 200, selected_again, 865)

    @number("1.5")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_basic_updates(self):
        self.load_basic()
        nav = Mode1Navigator(self.lands, 200)
        selected = nav.select_sites()
        self.check_solution(self.lands, 200, selected, 865)
        # Update Island A to have only 1 marine, rather than 100.
        nav.update_site(self.lands[0], 400, 1)
        # Done for testing \/ so check_solution works.
        self.lands[0].guardians = 1
        selected_again = nav.select_sites()
        self.check_solution(self.lands, 200, selected_again, 1158)

    @number("1.6")
    @visibility(visibility.VISIBILITY_SHOW)
    def test_multiple_crew_sizes(self):
        self.load_basic()
        nav = Mode1Navigator(self.lands, 200)
        results = nav.select_sites_from_adventure_numbers([0, 200, 500, 300, 40])
        self.assertListEqual(results, [0, 865, 1450, 1160, 240])
