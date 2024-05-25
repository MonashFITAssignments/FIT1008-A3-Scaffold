from landsites import Land
import heapq

class Mode2Navigator:
    """
    Student-TODO: short paragraph as per
    https://edstem.org/au/courses/14293/lessons/46720/slides/318306
    """

from dataclasses import dataclass
import heapq

@dataclass
class Land:
    name: str
    gold: int
    guardians: int

class Mode2Navigator:
    def __init__(self, n_teams: int) -> None:
        self.n_teams = n_teams
        self.sites = []

    def add_sites(self, sites: list[Land]) -> None:
        self.sites.extend(sites)

    def compute_score(self, land: Land, adventurer_size: int) -> tuple[float, int, int]:
        if land.guardians >= adventurer_size:
            return 0, adventurer_size, 0
        
        remaining_adventurers = adventurer_size - land.guardians
        gold_gained = land.gold
        score = 2.5 * remaining_adventurers + gold_gained
        return score, remaining_adventurers, gold_gained

    def construct_score_data_structure(self, adventurer_size: int) -> list:
        score_heap = []
        for land in self.sites:
            score, remaining_adventurers, gold_gained = self.compute_score(land, adventurer_size)
            heapq.heappush(score_heap, (-score, land.name, land, remaining_adventurers, gold_gained))
        return score_heap

    def simulate_day(self, adventurer_size: int) -> list[tuple[Land|None, int]]:
        decisions = []
        score_heap = self.construct_score_data_structure(adventurer_size)

        for _ in range(self.n_teams):
            if score_heap:
                _, _, land, remaining_adventurers, gold_gained = heapq.heappop(score_heap)
                decisions.append((land, adventurer_size))
                # Update the land site
                land.gold -= gold_gained
                land.guardians = max(0, land.guardians - adventurer_size)
            else:
                decisions.append((None, 0))

        return decisions

