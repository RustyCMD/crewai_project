# Game Resource Management System

from enum import Enum
import time

class ResourceType(Enum):
    WOOD = "Wood"
    STONE = "Stone"
    GOLD = "Gold"
    MANA = "Mana"

class ResourceGenerator:
    def __init__(self, resource_type: ResourceType, rate: float, active: bool = True):
        self.resource_type = resource_type
        self.rate = rate  # resources per second
        self.active = active
        self.last_generated_time = time.time()

    def generate(self):
        if not self.active:
            return 0
        
        current_time = time.time()
        time_elapsed = current_time - self.last_generated_time
        generated_amount = time_elapsed * self.rate
        
        if generated_amount >= 1:
            self.last_generated_time = current_time
            return int(generated_amount) # Return whole resources
        return 0

    def set_active(self, active: bool):
        self.active = active

class ResourceStorage:
    def __init__(self):
        self.resources = {resource: 0 for resource in ResourceType}

    def add_resource(self, resource_type: ResourceType, amount: int):
        if amount > 0:
            self.resources[resource_type] += amount
            print(f"Added {amount} {resource_type.value}. Current: {self.resources[resource_type]}")

    def consume_resource(self, resource_type: ResourceType, amount: int) -> bool:
        if amount <= 0:
            return False
        if self.resources[resource_type] >= amount:
            self.resources[resource_type] -= amount
            print(f"Consumed {amount} {resource_type.value}. Remaining: {self.resources[resource_type]}")
            return True
        else:
            print(f"Not enough {resource_type.value}. Needed: {amount}, Have: {self.resources[resource_type]}")
            return False

    def get_resource_amount(self, resource_type: ResourceType) -> int:
        return self.resources.get(resource_type, 0)

    def get_all_resources(self) -> dict:
        return self.resources.copy()

class ResourceSystem:
    def __init__(self):
        self.storage = ResourceStorage()
        self.generators = {}
        self.last_update_time = time.time()

    def add_generator(self, generator: ResourceGenerator):
        if generator.resource_type in self.generators:
            print(f"Warning: Generator for {generator.resource_type.value} already exists. Overwriting.")
        self.generators[generator.resource_type] = generator

    def update_generators(self):
        """Generates resources from all active generators."""
        generated_this_tick = {}
        for resource_type, generator in self.generators.items():
            amount = generator.generate()
            if amount > 0:
                self.storage.add_resource(resource_type, amount)
                generated_this_tick[resource_type] = generated_this_tick.get(resource_type, 0) + amount
        return generated_this_tick

    def collect_resource(self, resource_type: ResourceType, amount: int) -> bool:
        """Simulates player collecting resources (e.g., from an active node)."""
        # This might be triggered by a player action interacting with the game world
        # For now, it directly adds to storage.
        self.storage.add_resource(resource_type, amount)
        return True

    def spend_resource(self, resource_type: ResourceType, amount: int) -> bool:
        """Simulates player spending resources (e.g., to build something)."""
        return self.storage.consume_resource(resource_type, amount)

    def get_player_resources(self) -> dict:
        """Returns a dictionary of all player's current resources."""
        return self.storage.get_all_resources()

    def get_resource_amount(self, resource_type: ResourceType) -> int:
        """Returns the amount of a specific resource."""
        return self.storage.get_resource_amount(resource_type)

    def toggle_generator(self, resource_type: ResourceType, active: bool):
        """Activates or deactivates a specific resource generator."""
        if resource_type in self.generators:
            self.generators[resource_type].set_active(active)
            print(f"Generator for {resource_type.value} set to {'active' if active else 'inactive'}.")
        else:
            print(f"Error: Generator for {resource_type.value} not found.")

# --- Frontend API Considerations ---
# The Frontend Agent would typically interact with this system via:
# 1. Requesting the player's current resource amounts (e.g., get_player_resources()).
# 2. Triggering resource spending (e.g., spend_resource(ResourceType.WOOD, 10)).
# 3. Potentially triggering specific collection actions based on player interaction.
# The resource generation itself happens in the backend loop, and the frontend
# would poll for updated resource amounts.

# --- Example Usage (for testing) ---
# if __name__ == "__main__":
#     resource_sys = ResourceSystem()
#     
#     # Add some generators
#     wood_gen = ResourceGenerator(ResourceType.WOOD, 5.0) # 5 wood per second
#     gold_gen = ResourceGenerator(ResourceType.GOLD, 0.5) # 0.5 gold per second
#     resource_sys.add_generator(wood_gen)
#     resource_sys.add_generator(gold_gen)
#     
#     print("Initial resources:", resource_sys.get_player_resources())
#     
#     # Simulate game loop ticks
#     print("\nSimulating resource generation...")
#     for _ in range(5):
#         resource_sys.update_generators()
#         time.sleep(1) # Simulate 1 second passing
#     
#     print("\nResources after generation:", resource_sys.get_player_resources())
#     
#     # Simulate spending resources
#     print("\nAttempting to spend resources...")
#     can_afford_wood = resource_sys.spend_resource(ResourceType.WOOD, 15)
#     can_afford_gold = resource_sys.spend_resource(ResourceType.GOLD, 3)
#     can_afford_stone = resource_sys.spend_resource(ResourceType.STONE, 10) # Will fail if not generated
#     
#     print("\nResources after spending:", resource_sys.get_player_resources())
#     
#     # Toggle a generator
#     resource_sys.toggle_generator(ResourceType.WOOD, False)
#     print("\nWood generator deactivated. Simulating more time...")
#     for _ in range(3):
#         resource_sys.update_generators()
#         time.sleep(1)
#     print("\nResources after wood generator deactivated:", resource_sys.get_player_resources())
