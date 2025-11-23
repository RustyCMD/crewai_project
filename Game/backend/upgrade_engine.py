# Game Upgrade and Progression System

import time
from enum import Enum

# --- Enums and Data Structures ---

class UpgradeType(Enum):
    # Example upgrade categories or types
    RESOURCE_GENERATION = "ResourceGeneration"
    UNIT_CAPACITY = "UnitCapacity"
    BUILDING_EFFICIENCY = "BuildingEfficiency"
    NEW_ABILITY = "NewAbility"

class ResourceType(Enum):
    WOOD = "Wood"
    STONE = "Stone"
    GOLD = "Gold"
    MANA = "Mana"

class Upgrade:
    def __init__(self, id: str, name: str, description: str, upgrade_type: UpgradeType, cost: dict, prerequisites: list[str], effect: dict):
        self.id = id
        self.name = name
        self.description = description
        self.upgrade_type = upgrade_type
        self.cost = cost  # e.g., {ResourceType.WOOD: 100, ResourceType.GOLD: 50}
        self.prerequisites = prerequisites  # List of upgrade IDs required
        self.effect = effect  # e.g., {"resource_rate_multiplier": 1.2, "unlock_ability": "charge"}

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

# --- Upgrade Engine Core ---

class UpgradeEngine:
    def __init__(self, resource_system):
        self.available_upgrades: dict[str, Upgrade] = {}
        self.player_unlocked_upgrades: set[str] = set()
        self.resource_system = resource_system # Dependency on ResourceSystem
        self.player_effects: dict = {}
        self._initialize_upgrades()

    def _initialize_upgrades(self):
        """Defines all available upgrades in the game."""
        # This is where you define your game's upgrade tree
        # Example Upgrades:
        self.add_upgrade(Upgrade(
            id="wood_gather_1",
            name="Improved Woodcutting",
            description="Increases wood gathering speed by 20%.",
            upgrade_type=UpgradeType.RESOURCE_GENERATION,
            cost={ResourceType.WOOD: 50, ResourceType.STONE: 20},
            prerequisites=[],
            effect={"resource_rate_multiplier": {"Wood": 1.2}}
        ))

        self.add_upgrade(Upgrade(
            id="stone_gather_1",
            name="Expert Stonemasonry",
            description="Increases stone gathering speed by 15%.",
            upgrade_type=UpgradeType.RESOURCE_GENERATION,
            cost={ResourceType.WOOD: 75, ResourceType.STONE: 30},
            prerequisites=[],
            effect={"resource_rate_multiplier": {"Stone": 1.15}}
        ))

        self.add_upgrade(Upgrade(
            id="storage_capacity_1",
            name="Larger Storage",
            description="Increases resource storage capacity by 50%.",
            upgrade_type=UpgradeType.UNIT_CAPACITY,
            cost={ResourceType.WOOD: 100, ResourceType.GOLD: 25},
            prerequisites=[],
            effect={"storage_capacity_multiplier": 1.5}
        ))

        self.add_upgrade(Upgrade(
            id="wood_gather_2",
            name="Master Woodcutter",
            description="Further increases wood gathering speed by 30%.",
            upgrade_type=UpgradeType.RESOURCE_GENERATION,
            cost={ResourceType.WOOD: 150, ResourceType.GOLD: 75},
            prerequisites=["wood_gather_1"],
            effect={"resource_rate_multiplier": {"Wood": 1.3}}
        ))
        
        self.add_upgrade(Upgrade(
            id="unlock_forge",
            name="Forge Blueprint",
            description="Unlocks the ability to build a Forge.",
            upgrade_type=UpgradeType.NEW_ABILITY,
            cost={ResourceType.STONE: 200, ResourceType.GOLD: 100},
            prerequisites=["stone_gather_1"],
            effect={"unlock_building": "Forge"}
        ))

    def add_upgrade(self, upgrade: Upgrade):
        """Adds an upgrade to the list of available upgrades."""
        if upgrade.id in self.available_upgrades:
            print(f"Warning: Upgrade with ID '{upgrade.id}' already exists. Overwriting.")
        self.available_upgrades[upgrade.id] = upgrade

    def get_available_upgrades(self) -> list[Upgrade]:
        """Returns a list of all defined upgrades."""
        return list(self.available_upgrades.values())

    def get_purchasable_upgrades(self) -> list[Upgrade]:
        """Returns a list of upgrades the player can currently purchase."""
        purchasable = []
        for upgrade_id, upgrade in self.available_upgrades.items():
            if upgrade_id not in self.player_unlocked_upgrades:
                if self.can_afford_upgrade(upgrade):
                    # Check prerequisites
                    prereqs_met = True
                    for prereq_id in upgrade.prerequisites:
                        if prereq_id not in self.player_unlocked_upgrades:
                            prereqs_met = False
                            break
                    if prereqs_met:
                        purchasable.append(upgrade)
        return purchasable

    def get_unlocked_upgrades(self) -> list[str]:
        """Returns a list of IDs of upgrades the player has unlocked."""
        return list(self.player_unlocked_upgrades)

    def can_afford_upgrade(self, upgrade: Upgrade) -> bool:
        """Checks if the player has enough resources to afford an upgrade."""
        for resource, amount in upgrade.cost.items():
            if self.resource_system.get_resource_amount(resource) < amount:
                return False
        return True

    def purchase_upgrade(self, upgrade_id: str) -> bool:
        """Attempts to purchase an upgrade for the player."""
        if upgrade_id not in self.available_upgrades:
            print(f"Error: Upgrade ID '{upgrade_id}' not found.")
            return False

        upgrade = self.available_upgrades[upgrade_id]

        # Check if already unlocked
        if upgrade_id in self.player_unlocked_upgrades:
            print(f"Upgrade '{upgrade.name}' already purchased.")
            return False

        # Check prerequisites
        for prereq_id in upgrade.prerequisites:
            if prereq_id not in self.player_unlocked_upgrades:
                print(f"Prerequisite not met for '{upgrade.name}'. Missing: {prereq_id}")
                return False

        # Check if affordable
        if not self.can_afford_upgrade(upgrade):
            print(f"Not enough resources to purchase '{upgrade.name}'. Required: {upgrade.cost}")
            return False

        # Consume resources
        for resource, amount in upgrade.cost.items():
            self.resource_system.spend_resource(resource, amount)

        # Mark as unlocked and apply effects
        self.player_unlocked_upgrades.add(upgrade_id)
        self.apply_upgrade_effects(upgrade)
        print(f"Successfully purchased upgrade: '{upgrade.name}'")
        return True

    def apply_upgrade_effects(self, upgrade: Upgrade):
        """Applies the effects of a purchased upgrade."""
        # This method should interact with other game systems (e.g., ResourceSystem, AbilitySystem)
        # For demonstration, we'll store effects in a player_effects dict
        # and directly modify resource generators if they exist.

        if upgrade.effect:
            if "resource_rate_multiplier" in upgrade.effect:
                for resource_type, multiplier in upgrade.effect["resource_rate_multiplier"].items():
                    # Assuming ResourceSystem has a way to access/modify generators
                    # This part needs careful integration with ResourceSystem
                    # For now, let's just note the effect.
                    if resource_type.value in self.player_effects:
                        self.player_effects[resource_type.value] *= multiplier
                    else:
                        self.player_effects[resource_type.value] = multiplier
                    print(f"Applied effect: {resource_type.value} rate multiplier x{multiplier}")
                    # TODO: Integrate with ResourceSystem to modify generator rates
                    # Example: self.resource_system.modify_generator_rate(resource_type, multiplier)

            if "storage_capacity_multiplier" in upgrade.effect:
                multiplier = upgrade.effect["storage_capacity_multiplier"]
                self.player_effects["storage_capacity_multiplier"] = self.player_effects.get("storage_capacity_multiplier", 1.0) * multiplier
                print(f"Applied effect: Storage capacity multiplier x{multiplier}")
                # TODO: Integrate with ResourceSystem to update storage limits

            if "unlock_building" in upgrade.effect:
                building_name = upgrade.effect["unlock_building"]
                if "unlocked_buildings" not in self.player_effects:
                    self.player_effects["unlocked_buildings"] = set()
                self.player_effects["unlocked_buildings"].add(building_name)
                print(f"Applied effect: Unlocked building '{building_name}'")
                # TODO: Integrate with BuildingSystem or similar

            # Add more effect types as needed (e.g., new abilities, unit stat boosts)

    def get_current_player_effects(self) -> dict:
        """Returns the combined effects of all unlocked upgrades."""
        # This would typically involve iterating through player_unlocked_upgrades
        # and aggregating their effects. For simplicity, we're applying them directly
        # during purchase and storing them in self.player_effects.
        return self.player_effects

    def get_upgrade_status(self, upgrade_id: str) -> str:
        """Returns the status of a specific upgrade (e.g., 'available', 'purchased', 'locked')."""
        if upgrade_id not in self.available_upgrades:
            return "not_defined"
        if upgrade_id in self.player_unlocked_upgrades:
            return "purchased"
        
        upgrade = self.available_upgrades[upgrade_id]
        if not self.can_afford_upgrade(upgrade):
            return "locked_cost"
        
        for prereq_id in upgrade.prerequisites:
            if prereq_id not in self.player_unlocked_upgrades:
                return "locked_prerequisite"
        
        return "available"

# --- Frontend API Specifications ---

# The Frontend Agent can interact with the UpgradeEngine via the following methods:

# 1. Get all available upgrades (regardless of player progress):
#    - Method: `get_available_upgrades()`
#    - Returns: A list of `Upgrade` objects, each containing details like id, name, description, cost, prerequisites, and effect.

# 2. Get upgrades the player can currently purchase:
#    - Method: `get_purchasable_upgrades()`
#    - Returns: A list of `Upgrade` objects that meet resource and prerequisite criteria.

# 3. Get upgrades the player has already unlocked:
#    - Method: `get_unlocked_upgrades()`
#    - Returns: A list of strings, where each string is the ID of an unlocked upgrade.

# 4. Attempt to purchase an upgrade:
#    - Method: `purchase_upgrade(upgrade_id: str)`
#    - Parameters:
#        - `upgrade_id`: The string ID of the upgrade to purchase.
#    - Returns: `True` if the purchase was successful, `False` otherwise.
#    - Note: This method handles prerequisite checks, resource consumption, and applying effects.

# 5. Get the current combined effects from all unlocked upgrades:
#    - Method: `get_current_player_effects()`
#    - Returns: A dictionary representing the active effects on the player (e.g., resource multipliers, unlocked features).

# 6. Get the status of a specific upgrade:
#    - Method: `get_upgrade_status(upgrade_id: str)`
#    - Parameters:
#        - `upgrade_id`: The string ID of the upgrade to check.
#    - Returns: A string indicating the status: "purchased", "available", "locked_cost", "locked_prerequisite", "not_defined".

# --- Example Usage (for testing) ---
# Needs a mock ResourceSystem for demonstration
class MockResourceSystem:
    def __init__(self):
        self._resources = {ResourceType.WOOD: 200, ResourceType.STONE: 150, ResourceType.GOLD: 100}
        self.generators = {}

    def get_resource_amount(self, resource_type: ResourceType) -> int:
        return self._resources.get(resource_type, 0)

    def spend_resource(self, resource_type: ResourceType, amount: int) -> bool:
        if self._resources.get(resource_type, 0) >= amount:
            self._resources[resource_type] -= amount
            print(f"Mock spend: {amount} {resource_type.value}. Remaining: {self.get_resource_amount(resource_type)}")
            return True
        else:
            print(f"Mock spend failed: Not enough {resource_type.value}.")
            return False
            
    # Mock method for applying effects, assuming it modifies generators
    def modify_generator_rate(self, resource_type: ResourceType, multiplier: float):
        if resource_type in self.generators:
            self.generators[resource_type].rate *= multiplier
            print(f"Mock: {resource_type.value} generator rate set to {self.generators[resource_type].rate}")
        else:
            print(f"Mock: Generator for {resource_type.value} not found.")

    # Mock method for storage capacity
    def update_storage_capacity(self, multiplier: float):
        print(f"Mock: Storage capacity multiplier applied: x{multiplier}")

    # Mock method for unlocking buildings
    def unlock_building(self, building_name: str):
        print(f"Mock: Building '{building_name}' unlocked.")

if __name__ == "__main__":
    mock_resource_sys = MockResourceSystem()
    upgrade_engine = UpgradeEngine(mock_resource_sys)

    print("--- Available Upgrades ---")
    for upgrade in upgrade_engine.get_available_upgrades():
        print(f"- {upgrade.name} (Cost: {upgrade.cost})")

    print("\n--- Initial State ---")
    print(f"Current Resources: Wood={mock_resource_sys.get_resource_amount(ResourceType.WOOD)}, Stone={mock_resource_sys.get_resource_amount(ResourceType.STONE)}, Gold={mock_resource_sys.get_resource_amount(ResourceType.GOLD)}")
    print(f"Unlocked Upgrades: {upgrade_engine.get_unlocked_upgrades()}")
    print(f"Player Effects: {upgrade_engine.get_current_player_effects()}")

    print("\n--- Attempting Purchases ---")
    # Try to purchase wood_gather_1 (should be affordable)
    if upgrade_engine.purchase_upgrade("wood_gather_1"):
        print("Purchase successful!")
    else:
        print("Purchase failed.")

    # Try to purchase storage_capacity_1 (should be affordable)
    if upgrade_engine.purchase_upgrade("storage_capacity_1"):
        print("Purchase successful!")
    else:
        print("Purchase failed.")

    # Try to purchase wood_gather_2 (requires wood_gather_1, should be affordable)
    if upgrade_engine.purchase_upgrade("wood_gather_2"):
        print("Purchase successful!")
    else:
        print("Purchase failed.")
        
    # Try to purchase unlock_forge (requires stone_gather_1, which is not defined/purchased yet)
    if upgrade_engine.purchase_upgrade("unlock_forge"):
        print("Purchase successful!")
    else:
        print("Purchase failed.")

    print("\n--- State After Purchases ---")
    print(f"Current Resources: Wood={mock_resource_sys.get_resource_amount(ResourceType.WOOD)}, Stone={mock_resource_sys.get_resource_amount(ResourceType.STONE)}, Gold={mock_resource_sys.get_resource_amount(ResourceType.GOLD)}")
    print(f"Unlocked Upgrades: {upgrade_engine.get_unlocked_upgrades()}")
    print(f"Player Effects: {upgrade_engine.get_current_player_effects()}")

    print("\n--- Purchasable Upgrades Now ---")
    purchasable_now = upgrade_engine.get_purchasable_upgrades()
    if purchasable_now:
        for upgrade in purchasable_now:
            print(f"- {upgrade.name} (Cost: {upgrade.cost})")
    else:
        print("No upgrades are currently purchasable.")