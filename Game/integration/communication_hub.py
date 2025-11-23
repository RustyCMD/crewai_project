# Communication Hub

import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CommunicationHub:
    def __init__(self):
        self.message_log = []
        self.listeners = {}
        logging.info("Communication Hub initialized.")

    def register_listener(self, agent_name, callback_function):
        """Registers a callback function for an agent to receive messages."""
        if agent_name not in self.listeners:
            self.listeners[agent_name] = []
        self.listeners[agent_name].append(callback_function)
        logging.info(f"Listener registered for agent: {agent_name}")

    def unregister_listener(self, agent_name, callback_function):
        """Unregisters a callback function for an agent."""
        if agent_name in self.listeners and callback_function in self.listeners[agent_name]:
            self.listeners[agent_name].remove(callback_function)
            logging.info(f"Listener unregistered for agent: {agent_name}")
            if not self.listeners[agent_name]:
                del self.listeners[agent_name]
        else:
            logging.warning(f"Attempted to unregister non-existent listener for agent: {agent_name}")

    def send_message(self, sender, recipient, message_type, payload):
        """Sends a message to a specific agent or broadcasts it."""
        message = {
            "sender": sender,
            "recipient": recipient,  # Can be an agent name or 'all' for broadcast
            "type": message_type,
            "payload": payload
        }
        self.message_log.append(message)
        logging.info(f"Message sent from {sender} to {recipient} (Type: {message_type})")
        self.deliver_message(message)

    def deliver_message(self, message):
        """Delivers a message to the appropriate listeners."""
        recipient = message["recipient"]
        if recipient == "all":
            # Broadcast message to all listeners
            for agent_name, callbacks in self.listeners.items():
                for callback in callbacks:
                    try:
                        callback(message)
                    except Exception as e:
                        logging.error(f"Error delivering message to {agent_name}: {e}")
        elif recipient in self.listeners:
            # Direct message to a specific agent
            for callback in self.listeners[recipient]:
                try:
                    callback(message)
                except Exception as e:
                    logging.error(f"Error delivering message to {recipient}: {e}")
        else:
            logging.warning(f"No listeners found for recipient: {recipient}")

    def receive_message(self, agent_name):
        """Retrieves messages intended for a specific agent. (This is a simplified model; actual reception is event-driven via callbacks)."""
        # In a real-time system, messages are pushed to listeners via callbacks.
        # This method could be used for polling or retrieving historical messages if needed.
        received = [msg for msg in self.message_log if msg["recipient"] == agent_name or msg["recipient"] == "all"]
        logging.info(f"{agent_name} is checking for messages. Found {len(received)} potentially relevant historical messages.")
        return received

    def get_message_log(self):
        """Returns the entire message log."""
        return self.message_log

# --- Example Usage --- 
# This section demonstrates how the CommunicationHub might be used.
# In a real application, agents would be instantiated and registered.

# if __name__ == "__main__":
#     hub = CommunicationHub()

#     # Define dummy callback functions for agents
#     def agent_a_callback(message):
#         print(f"Agent A received: {message}")

#     def agent_b_callback(message):
#         print(f"Agent B received: {message}")

#     # Register agents with the hub
#     hub.register_listener("AgentA", agent_a_callback)
#     hub.register_listener("AgentB", agent_b_callback)

#     # Send a direct message
#     hub.send_message("System", "AgentA", "GREETING", {"text": "Hello Agent A!"})

#     # Send a broadcast message
#     hub.send_message("System", "all", "STATUS_UPDATE", {"status": "System is operational"})

#     # Agent B trying to receive (demonstration of the receive_message method's purpose)
#     # Note: In practice, callbacks handle immediate message delivery.
#     print("\nAgent B checking historical messages:")
#     print(hub.receive_message("AgentB"))

#     print("\nFull message log:")
#     for log_entry in hub.get_message_log():
#         print(log_entry)