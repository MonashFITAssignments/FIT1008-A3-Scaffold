from landsites import Land
from data_structures.bst import *
from data_structures.linked_stack import LinkedStack

class Mode1Navigator:
    """
    Navigator for optimizing the allocation of adventurers to maximize gold obtained from land sites.
    
    Approach:
    - This class manages land sites and determines the optimal allocation of adventurers to these sites.
    - A Binary Search Tree (BST) is used to efficiently sort and access land sites based on a custom comparison key.
    - The class provides methods to select sites based on the number of adventurers and update site details.
    
    Data Structures and Types:
    - `List[Land]`: Initial list of land sites.
    - `BinarySearchTree`: A BST to store and manage land sites based on their efficiency (gold per guardian ratio). BST is a special kind of binary tree.
        Reasons for using a BST:

        Efficient Searching:
        BSTs provide an efficient way to search for elements, with an average-case complexity of O(log n)
        O(logN) for search operations. This is useful for quickly locating a specific land site when it needs to be updated or accessed.

        Order Maintenance:
        BSTs maintain elements in a sorted order. This is beneficial when we need to keep track of land sites based on certain attributes, such as gold-to-guardian ratios or other scoring metrics.

        Dynamic Updates:
        As land sites are plundered, their attributes (gold and guardians) change. A BST allows for efficient updates, ensuring that the tree remains balanced and search operations continue to be efficient.

        Range Queries:
        If we need to perform range queries (e.g., finding all land sites with a score within a certain range), a BST can handle this more efficiently compared to other data structures.
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        Initialize the navigator with the given list of land sites and the total number of
        adventurers.
        
        Parameters:
            sites (list[Land]): List of land sites, where each site is an instance of Land.
            adventurers (int): Total number of adventurers available for raiding the sites.
        
        Complexity:
            Best Case: O(N log N) - Sorting the sites based on a specific ratio or criteria for efficient decision-making. Cyclic lists take O(n) time and adding each value to a binary tree takes O(log n) time.
            Worst Case: O(N log N) - The same, as sorting dominates the initialization complexity.
            N is the number of land sites in the input list.

        Approach:
        - Initializes the navigator by creating a BST to store land sites sorted by their gold-to-guardian ratio.
        - Each land site is inserted into the BST with a key that reflects its efficiency.
        - Items are inserted into the BST based on the ratio of gold to guardians with a nagative sign. This allows the BST to sort the sites in descending order, and with InOrder traversal, we can get the sites in ascending order.
        
        Example:

        self.sites = [
            Land("A", 400, 100)
            Land("B", 300, 150)
            Land("C", 100, 5)
            Land("D", 350, 90)
            Land("E", 300, 100)
        ]
        nav = Mode1Navigator(self.sites, 200)
        
        list of sites: [Land(name='A', gold=400, guardians=100), Land(name='B', gold=300, guardians=150), Land(name='C', gold=100, guardians=5), Land(name='D', gold=350, guardians=90), Land(name='E', gold=300, guardians=100)]

        How the BST looks like after inserting the sites:
        -4.0
        ╟─-20.0
        ╙─-2.0
            ╟─-3.888888888888889
            ║ ╟─
            ║ ╙─-3.0
            ╙─
        """
        self.adventurers = adventurers
        self.sites = BinarySearchTree()
        for site in sites:
            self.sites[-(site.get_gold() / site.get_guardians()) if site.guardians != 0 else float('inf')] = site # Insert with comparison key

    def select_sites(self) -> list[tuple[Land, int]]:
        """
        Select which land sites to attack and determine the number of adventurers to send to each site
        to maximize the gold obtained.

        Returns:
            list[tuple[Land, int]]: A list of tuples where each tuple contains a land site and the
            number of adventurers sent to that site.

        Complexity:
            Best Case: O(1) - When no adventurers are available.
            Worst Case: O(N) - Need to iterate through all sites to determine the optimal distribution of adventurers.
            N is the number of land sites in the BST.

        Approach:
        - The method iterates through the BST to select sites for raiding. With InOrder traversal, the sites are visited in ascending order.
        - It calculates the number of adventurers to send to each site based on the available adventurers and the site's guardians.
        - If the remaining adventurers are zero, the method stops and returns the selected sites.
        - Elif a site has both gold and guardians, the method calculates the number of adventurers to send based on the ratio of gold to guardians, and adds the site to the selected sites.
        
        Example:
        result = navigator.select_sites() Refer to the example in the __init__ method.
        print(result)  # Outputs: [(Land(name='C', gold=100, guardians=5), 5), (Land(name='A', gold=400, guardians=100), 100), (Land(name='D', gold=350, guardians=90), 90), (Land(name='E', gold=300, guardians=100), 5)]
        """
        remaining_adventurers = self.adventurers
        selected_sites = []

        for node in BSTInOrderIterator(self.sites.root):
            site = node.item
            if remaining_adventurers == 0:
                break
            if site.gold > 0 and site.guardians > 0:
                adventurers_to_send = min(remaining_adventurers, site.get_guardians())
                selected_sites.append((site, adventurers_to_send))
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
            Best Case: O(A * N) - Same as the worst case.
            Worst Case: O(A * N) - Where A is the length of adventure_numbers, N is the number of sites in the BST.
            The reason for this is that this method needs to iterate through every element in adventure_numbers (which requires A operations), and for each element it may need to perform a lookup or other operation in the BST (which requires N operations).
            Functons inside loops, such as comparison, addition, subtraction, multiplication, division, and assignment, have a complexity of O(1).
            
        Approach:
        - The method iterates through the provided list of adventurer numbers.
        - For each number, it calculates the total gold that can be obtained by iterating through the BST and selecting optimal sites.
        - The total gold is calculated based on the gold-to-guardian ratio of each site and the number of adventurers sent to the site.
        - The total gold is added to the rewards list and returned at the end.
        - The remaining adventurers are updated after each site selection.
        - The method returns a list of total gold rewards corresponding to each entry in the adventure_numbers list.
        
        Example:
        rewards = navigator.select_sites_from_adventure_numbers([0, 200, 500, 300, 40])
        Each reward corresponds to the min(min(remaining_adventurers, site.get_guardians())* (site.get_gold() / site.get_guardians()), site.get_gold()).
        For example:
        For a number of 200 adventures: reward = 100.0 + 400.0 + 350.0 + 15.0 = 865.0
        print(rewards)  # Outputs: [0, 865, 1450, 1160, 240]
        """
        rewards = []

        for adventurers in adventure_numbers:
            total_reward = 0.0
            remaining_adventurers = adventurers
            
            for node in BSTInOrderIterator(self.sites.root):
                site = node.item
                if remaining_adventurers == 0:
                    break
                if site.gold > 0 and site.guardians > 0:
                    adventurers_to_send = min(remaining_adventurers, site.get_guardians())
                    reward = min(adventurers_to_send * (site.get_gold() / site.get_guardians()), site.get_gold())
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
            Best Case: O(CompK) - Occurs when the first value of the query, which is the value of root, is the same as the value we are looking for.
            Worst Case: O(CompK * D) - When the query value is in the deepest part of the BST, where D is the depth of the tree.
            CompK is the complexity of comparing the keys
            Both set gold and set guardians takes only constant time complexity O(1).
        Approach:
        - Finds the specified land site in the BST and updates its properties directly.
        
        Example:
        nav.update_site(self.sites[0], 400, 1)
        land = self.sites[-(land.get_gold() / land.get_guardians())] 
        Searching for the first item, which would return (-4.0, Land(name='A', gold=400, guardians=100)), for the best case.

        How the BST looks like:
        -4.0
        ╟─-20.0
        ╙─-2.0
            ╟─-3.888888888888889
            ║ ╟─
            ║ ╙─-3.0
            ╙─
        After getting the land from the BST, modify its attribute.
        """
        land = self.sites[-(land.get_gold() / land.get_guardians())] 
        land.set_gold(new_reward)
        land.set_guardians(new_guardians)
        
if __name__ == "__main__":
    """
    For testing purposes.
    """
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