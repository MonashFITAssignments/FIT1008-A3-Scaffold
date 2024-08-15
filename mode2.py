from landsites import Land
from typing import List, Tuple, Union
from data_structures.heap import MaxHeap
from data_structures.bst import *

class Mode2Navigator:
    """
    Navigator for simulating a fair fight among multiple adventurer teams.
    
    Approach:
    - This class manages multiple adventurer teams and various land sites where teams can raid for gold.
    - It uses a max-heap data structure to efficiently determine the land site that yields the highest score.
    - The score computation considers the number of adventurers and properties of each land site (gold and guardians).
    - The class simulates a day's worth of raiding by distributing adventurers to different land sites and updating the state of these sites accordingly.
    
    Data Structures and Types:
    - List[Land]: A list to store instances of `Land`.
    - MaxHeap: A max-heap to store and retrieve land sites based on computed scores.
        Reasons for using a max-heap:
            Efficiency in Finding Maximum: The primary operation required in the simulate_day method is to repeatedly find the land site with the highest score. A MaxHeap allows us to efficiently extract the maximum score in O(logn) time.
            Dynamic Updates: As adventurers raid the sites, the scores of the sites need to be updated. A MaxHeap supports efficient reordering after updates, maintaining the heap property with insertions and deletions in O(logn) time.
            Priority Queue Behavior: A MaxHeap acts as a priority queue, which is perfect for our use case where land sites are prioritized based on their scores.

    - Tuple: Used to store and return multiple values from methods.
        The tuple (score, site.get_name(), site) contains three elements:
            Score: This is the primary metric used for comparison in the heap. We need to prioritize land sites based on the highest score, so the score is the first element in the tuple.
            Site Name: Including site.get_name() helps in uniquely identifying and comparing sites, especially if multiple sites have the same score. It serves as a tiebreaker to ensure the heap structure remains stable.
            Site Instance: The site object itself is included to have direct access to the Land instance for updating its state (gold and guardians) and recomputing scores.
    """

    def __init__(self, n_teams: int) -> None:
        """
        Initialize the navigator with the number of teams.
        
        Parameters:
            n_teams (int): Number of adventurer teams.
        
        Complexity:
            O(1) - Best/Worst Case: Initialization is a constant time operation.
        """
        self.n_teams = n_teams
        self.sites = []

    def add_sites(self, sites: List[Land]) -> None:
        """
        Add land sites to the navigator.

        Parameters:
            sites (List[Land]): List of land sites, where each site is an instance of Land.

        Complexity:
            Best Case: O(N) - N is the number of elements in the sites list.
            Worst Case: O(N) - The same as the best case, as the operation involves extending the list.
            To add additional elements or an iterable to the end of a list, extend() adds each item to the list independently after iterating through each one in the input.

        Approach:
        - The method uses a list to store land sites.
        - It extends the current list of sites with the new sites provided as input.
        
        Example:
        The original list:
        [Land(name='A', gold=400, guardians=100), Land(name='B', gold=300, guardians=150), Land(name='C', gold=100, guardians=5), Land(name='D', gold=350, guardians=90), Land(name='E', gold=300, guardians=100)]

        navigator.add_sites(Land(name='F', gold=900, guardians=150))

        The updated list:
        [Land(name='A', gold=400, guardians=100), Land(name='B', gold=300, guardians=150), Land(name='C', gold=100, guardians=5), Land(name='D', gold=350, guardians=90), Land(name='E', gold=300, guardians=100), Land(name='F', gold=900, guardians=150)]
        """
        self.sites.extend(sites)

    def simulate_day(self, adventurer_size: int) -> List[Tuple[Union[Land, None], int]]:
        """
        Simulate a day of the game.

        Parameters:
            adventurer_size (int): Number of adventurers for each team.

        Returns:
            List[Tuple[Union[Land, None], int]]: A list of tuples representing the choices made by each team.
                Each tuple contains:
                - An instance of Land or None if no site was chosen.
                - An integer representing the number of adventurers sent to the chosen site.

        Complexity:
            Best Case: O(n * log n + t) - where n is the number of land sites and t is the number of teams.
            Worst Case: O(n * log n + t) - The same as the best case due to the operations involved in maintaining the heap and iterating over the teams.
            For each team, we extract the maximum element and potentially reinsert a modified element. According to the assignment instruction, extracting and reinserting both take O(1) time.
            Functons inside loops, such as comparison, addition, subtraction, multiplication, division, and assignment, have a complexity of O(1).
            The method conpute_score has a complexity of O(1) as it performs simple arithmetic operations and comparisons. 
            If there are t teams, the overall complexity is O(t).
            Combining these gives us O(nlogn + t). 

        Approach:
        - Constructs a max-heap data structure to prioritize land sites based on scores.
        - Iterates over each team, selecting the best available site for raiding.
        - For each team, the best available land site is chosen by extracting the maximum score from the heap.
        - Add the score to the result list.
        - The state of the chosen site is updated based on the raid (gold and guardians).
        - The new score for the updated site is recomputed and reinserted into the heap to maintain the correct ordering.
        
        Example:
            Consider the following scenario with 2 land sites and 3 teams, each with 100 adventurers:

            MaxHeap (before simulation)
            +-----------------------------------------------------+
            | (score, site_name, site)                            |
            | (400.0, A, Land(name='A', gold=400, guardians=100)) |
            | (375.0, D, Land(name='D', gold=350, guardians=90))  |
            +-----------------------------------------------------+
            Return List = []

            Team 1:
            - Chose Land "A"
            - Sent 100 adventurers
            - New state of Land "A": gold = 0.0, guardians = 0
            - Get a score of 400.0

            MaxHeap (after Team 1)
            +-----------------------------------------------------+
            | (score, site_name, site)                            |
            | (250.0, A, Land(name='A', gold=0, guardians=0))     |
            | (375.0, D, Land(name='D', gold=350, guardians=90))  |
            +-----------------------------------------------------+
            Return List = [(Land A, 400.0)]

            Team 2:
            - Chose Land "D"
            - Sent 100 adventurers
            - New state of Land "D": gold = 0, guardians = 0
            - Get a score of 375.0

            MaxHeap (after Team 2)
            +-----------------------------------------------------+
            | (score, site_name, site)                            |
            | (250.0, A, Land(name='A', gold=0, guardians=0))     |
            | (250.0, D, Land(name='D', gold=0, guardians=0))     |
            +-----------------------------------------------------+
            Return List = [(Land A, 400.0), (Land B, 5.0)]

            Team 3:
            - Chose Land "A"
            - Sent 100 adventurers
            - New state of Land "A": gold = 0, guardians = 0
            - Get a score of 250.0

            MaxHeap (after Team 3)
            +-----------------------------------------------------+
            | (score, site_name, site)                            |
            | (250.0, A, Land(name='A', gold=0, guardians=0))     |
            | (250.0, D, Land(name='D', gold=0, guardians=0))     |
            +-----------------------------------------------------+
            Return List = [(Land A, 400.0), (Land B, 5.0), (Land A, 250.0)]

        """
        choices = []

        heap = self.construct_score_data_structure(adventurer_size)

        for team in range(self.n_teams):
            if len(heap) == 0 or adventurer_size == 0:
                choices.append((None, 0))
                continue

            _, _, best_site = heap.get_max()
            _, remaining_adventurers, gold_gained = self.compute_score(best_site, adventurer_size)
            sent_adventurers = adventurer_size - remaining_adventurers
            choices.append((best_site, sent_adventurers))
            best_site.gold -= gold_gained
            best_site.guardians -= sent_adventurers
            
            new_score, _, _ = self.compute_score(best_site, adventurer_size)
            heap.add((new_score, best_site.get_name(), best_site))

        return choices

    
    def compute_score(self, land: Land, adventurers: int) -> Tuple[float, int, float]:
        """
        Compute the score of a land site for a given number of adventurers.

        Parameters:
            land (Land): An instance of Land.
            adventurers (int): Number of adventurers coming to the land.

        Returns:
            Tuple[float, int, float]: A tuple containing the score, remaining adventurers, and gold gained.

        Complexity:
            Best Case: O(1) - Simple arithmetic operations and comparisons.
            Worst Case: O(1) - The same as the best case, no iterative or recursive operations involved.

        Approach:
        - The method calculates the potential score based on the number of adventurers and the site's properties.
        - If there are no guardians, the score is straightforward.
        - Otherwise, it calculates the gold gained and remaining adventurers based on the number of guardians and gold.
        
        Example:
            Steps for computing the score:

            score = navigator.compute_score(Land(name='A', gold=400, guardians=100), 100)
            ci = min(adventurers, land.guardians) = 100
            gold_gained = min(ci * (land.gold / land.guardians), land.gold) = 400
            score = 2.5 * remaining_adventurers + gold_gained = 2.5 * 0 + 400 = 400

            print(score)  # Outputs: (computed score, remaining adventurers, gold gained): (400, 0, 400)
        """

        if land.guardians == 0:
            return 2.5 * adventurers, adventurers, 0

        ci = min(adventurers, land.guardians)
        gold_gained = min(ci * (land.gold / land.guardians), land.gold)
        remaining_adventurers = adventurers - ci
        score = 2.5 * remaining_adventurers + gold_gained
        return score, remaining_adventurers, gold_gained

    def construct_score_data_structure(self, adventurers: int):
        """
        Constructs a max-heap data structure containing the scores of land sites for a given number of adventurers.

        Parameters:
            adventurers (int): Number of adventurers coming to explore the sites.

        Returns:
            MaxHeap: A max-heap containing tuples where each tuple consists of the score and the corresponding site.

        Complexity:
            Best Case: O(n * log n) - where n is the number of land sites.
            Worst Case: O(n * log n) - The same as the best case, due to heap operations involved.
            We add n elements to the heap, each insertion taking O(logn) time. Thus, the overall complexity is O(nlogn).

        Approach:
        - The MaxHeap is initialized with the size equal to the number of land sites.
        - We compute the initial scores for each site based on the given number of adventurers.
        - These scores, along with the site names and instances, are added to the heap as tuples.
                
        Example:
            Land Sites:
            1. Land("A", 100, 10)
            2. Land("B", 200, 20)

            Scores Computed:
            - Land "A": (12.5, "A", Land("A", 100, 10))
            - Land "B": (25.0, "B", Land("B", 200, 20))

            MaxHeap:
            +---------------------------------------+
            | (25.0, "B", Land("B", 200, 20))       |
            | (12.5, "A", Land("A", 100, 10))       |
            +---------------------------------------+
        """
        heap = MaxHeap(len(self.sites))

        # Initialize the max-heap with land site scores
        for site in self.sites:
            score, _, _ = self.compute_score(site, adventurers)
            heap.add((score, site.get_name(), site))

        return heap