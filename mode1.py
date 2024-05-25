from landsites import Land
from algorithms.mergesort import mergesort
from data_structures.bst import *
from typing import Tuple

class Mode1Navigator:
    """
    Student-TODO: short paragraph as per
    https://edstem.org/au/courses/14293/lessons/46720/slides/318306
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        Initialize the navigator with the given list of land sites and the total number of
        adventurers.
        
        Parameters:
            sites (list[Land]): List of land sites, where each site is an instance of Land.
            adventurers (int): Total number of adventurers available for raiding the sites.
        
        Complexity:
            Best Case: O(N log N) - Sorting the sites based on a specific ratio or criteria for efficient decision-making.
            Worst Case: O(N log N) - The same, as sorting dominates the initialization complexity.
        """

        self.adventurers = adventurers
        self.sites = BinarySearchTree[Land, float]()
        for site in sites:
            self.sites[site.get_gold() / site.get_guardians()] = site # Insert with comparison key

    def select_sites(self) -> list[tuple[Land, int]]:
        """
        Select which land sites to attack and determine the number of adventurers to send to each site
        to maximize the gold obtained.

        Returns:
            list[tuple[Land, int]]: A list of tuples where each tuple contains a land site and the
            number of adventurers sent to that site.

        Complexity:
            Best Case: O(1) - When no adventurers are available or all sites have no guardians.
            Worst Case: O(N) - Need to iterate through all sites to determine the optimal distribution of adventurers.
        """
        remaining_adventurers = self.adventurers
        selected_sites = []

        for site in iter(self.sites):
            if remaining_adventurers == 0:
                break
            adventurers_to_send = min(remaining_adventurers, site.item.get_guardians())
            selected_sites.append((site.item, adventurers_to_send))
            remaining_adventurers -= adventurers_to_send

        return selected_sites

    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        Calculate the maximum amount of gold obtainable for various numbers of adventurers.

        Parameters:
            adventure_numbers (list[int]): List of different numbers of adventurers to evaluate.

        Returns:
            list[float]: List of maximum gold amounts corresponding to each entry in adventure_numbers.

        Complexity:
            Best Case: O(N) - When the list of adventure numbers is empty.
            Worst Case: O(A * N) - Where A is the length of adventure_numbers and N is the number of sites.
        """
        rewards = []

        for adventurers in adventure_numbers:
            total_reward = 0
            remaining_adventurers = adventurers

            for node in iter(self.sites):
                site = node.item
                if remaining_adventurers == 0:
                    break
                adventurers_to_send = min(remaining_adventurers, site.get_guardians())
                reward = min((adventurers_to_send / site.get_guardians()) * site.get_gold(), site.get_gold())
                total_reward += reward
                remaining_adventurers -= adventurers_to_send

            rewards.append(total_reward)

        return rewards

    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        Update the specified land site with new values for reward and guardians.

        Parameters:
            land (Land): The land site to update.
            new_reward (float): New amount of gold at the site.
            new_guardians (int): New number of guardians at the site.

        Complexity:
            Best Case: O(1) - Direct assignment of new values.
            Worst Case: O(log(N)) - The same, as the operation involves only a few direct assignments.
        """
        key = land.get_gold() / land.get_guardians()
        land.set_gold(new_reward)
        land.set_guardians(new_guardians)
        self.sites[key] = land
        
if __name__ == "__main__":
    a = Land("A", 400, 100)
    b = Land("B", 300, 150)
    c = Land("C", 100, 5)
    d = Land("D", 350, 90)
    e = Land("E", 300, 100)
    # Create deepcopies of the sites
    sites = [
        Land(a.get_name(), a.get_gold(), a.get_guardians()),
        Land(b.get_name(), b.get_gold(), b.get_guardians()),
        Land(c.get_name(), c.get_gold(), c.get_guardians()),
        Land(d.get_name(), d.get_gold(), d.get_guardians()),
        Land(e.get_name(), e.get_gold(), e.get_guardians()),
    ]
    nav = Mode1Navigator(sites, 200)
    ans = nav.select_sites()
    print(ans)