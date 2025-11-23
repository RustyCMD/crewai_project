# Game Events and Notifications System

import collections

class EventSystem:
    """
    A system for managing game events and notifications.
    Allows different parts of the game to dispatch events and for other parts
    to subscribe to and handle these events.
    """
    def __init__(self):
        # Use a defaultdict to automatically create lists for new event types
        self._listeners = collections.defaultdict(list)
        print("EventSystem initialized.")

    def subscribe(self, event_type: str, handler):
        """
        Subscribes a handler function to a specific event type.

        Args:
            event_type (str): The type of event to subscribe to (e.g., "player_joined", "item_collected").
            handler (callable): The function to call when the event is dispatched.
                                This function should accept the same arguments as the event.
        """
        if not callable(handler):
            print(f"Warning: Handler for event '{event_type}' is not callable. Subscription ignored.")
            return

        if handler not in self._listeners[event_type]:
            self._listeners[event_type].append(handler)
            print(f"Handler '{handler.__name__}' subscribed to event '{event_type}'.")
        else:
            print(f"Handler '{handler.__name__}' is already subscribed to event '{event_type}'.")

    def unsubscribe(self, event_type: str, handler):
        """
        Unsubscribes a handler function from a specific event type.

        Args:
            event_type (str): The type of event to unsubscribe from.
            handler (callable): The handler function to remove.
        """
        if event_type in self._listeners and handler in self._listeners[event_type]:
            self._listeners[event_type].remove(handler)
            print(f"Handler '{handler.__name__}' unsubscribed from event '{event_type}'.")
            # Clean up empty lists to keep the dictionary tidy
            if not self._listeners[event_type]:
                del self._listeners[event_type]
        else:
            print(f"Handler '{handler.__name__}' not found for event '{event_type}' or event type does not exist.")

    def dispatch(self, event_type: str, *args, **kwargs):
        """
        Dispatches an event to all subscribed handlers.

        Args:
            event_type (str): The type of event to dispatch.
            *args: Positional arguments to pass to the handlers.
            **kwargs: Keyword arguments to pass to the handlers.
        """
        if event_type in self._listeners:
            print(f"Dispatching event '{event_type}' with args: {args}, kwargs: {kwargs}")
            # Iterate over a copy of the list in case a handler unsubscribes itself
            for handler in list(self._listeners[event_type]):
                try:
                    handler(*args, **kwargs)
                except Exception as e:
                    print(f"Error executing handler '{handler.__name__}' for event '{event_type}': {e}")
        else:
            print(f"No listeners found for event '{event_type}'.")

    def get_subscribers(self, event_type: str) -> list:
        """
        Returns a list of handlers subscribed to a specific event type.

        Args:
            event_type (str): The type of event.

        Returns:
            list: A list of callable handlers.
        """
        return self._listeners.get(event_type, [])

# --- Frontend API Considerations ---
# The frontend agent will interact with this system by:
# 1. Defining handler functions that respond to specific game events.
# 2. Calling `event_system.subscribe(event_type, handler_function)` to register
#    these handlers for relevant events.
# 3. When a game event occurs (e.g., player action, system update), the backend
#    will call `event_system.dispatch(event_type, *args, **kwargs)`.
# 4. The frontend might also need to call `event_system.unsubscribe` if a
#    component is destroyed or no longer needs to listen to certain events.
# 5. The frontend could potentially use `get_subscribers` for debugging or
#    monitoring purposes, though direct interaction with `dispatch` is backend-driven.

# --- Example Usage (for testing) ---
# if __name__ == "__main__":
#     import time
#     event_sys = EventSystem()

#     # Define some handler functions
#     def handle_player_login(player_name: str, timestamp: float):
#         print(f"EVENT RECEIVED: Player '{player_name}' logged in at {timestamp}.")

#     def log_item_collection(item_name: str, quantity: int, player_id: str):
#         print(f"EVENT RECEIVED: Player '{player_id}' collected {quantity} of '{item_name}'.")

#     def handle_game_over(reason: str):
#         print(f"GAME OVER! Reason: {reason}")

#     # Subscribe handlers to events
#     event_sys.subscribe("player_login", handle_player_login)
#     event_sys.subscribe("item_collected", log_item_collection)
#     event_sys.subscribe("game_over", handle_game_over)
#     event_sys.subscribe("player_login", handle_player_login) # Test duplicate subscription

#     print("\n--- Dispatching Events ---")

#     # Dispatch events
#     event_sys.dispatch("player_login", "Alice", time.time())
#     event_sys.dispatch("item_collected", "Gold Coin", 10, "player_123")
#     event_sys.dispatch("game_over", "Ran out of time")
#     event_sys.dispatch("unknown_event", "some data") # Test unknown event

#     print("\n--- Unsubscribing and Dispatching Again ---")

#     # Unsubscribe a handler
#     event_sys.unsubscribe("item_collected", log_item_collection)
#     event_sys.unsubscribe("player_login", handle_player_login) # Test unsubscribing a handler
#     event_sys.unsubscribe("player_login", handle_player_login) # Test unsubscribing again

#     # Dispatch again to see changes
#     event_sys.dispatch("player_login", "Bob", time.time()) # Should not be handled by handle_player_login
#     event_sys.dispatch("item_collected", "Health Potion", 1, "player_456") # Should not be handled

#     print("\nSubscribers for 'player_login':", event_sys.get_subscribers("player_login"))
#     print("Subscribers for 'item_collected':", event_sys.get_subscribers("item_collected"))
#     print("Subscribers for 'game_over':", event_sys.get_subscribers("game_over"))
