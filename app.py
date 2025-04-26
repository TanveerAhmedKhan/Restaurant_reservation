import os
import json
from menu_service import MenuService
from reservation_service import ReservationService
import config

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    print("=" * 80)
    print(f"{config.APP_NAME}".center(80))
    print("=" * 80)
    print("Type 'exit' or 'quit' to end the conversation.")
    print("Type 'menu' to see the full menu.")
    print("Type 'vegetarian', 'vegan', or 'gluten-free' to see dietary options.")
    print("Type 'appetizers', 'main courses', or 'desserts' to see specific categories.")
    print("-" * 80)

class SimpleRestaurantChatbot:
    def __init__(self):
        self.menu_service = MenuService()
        self.reservation_service = ReservationService()

    def process_message(self, message: str) -> str:
        """Process a user message and return a response."""
        message = message.lower()

        # Menu-related commands
        if message == "menu":
            return self._format_full_menu(self.menu_service.get_full_menu())

        elif message == "vegetarian":
            items = self.menu_service.get_items_by_dietary_preference("vegetarian")
            return self._format_menu_items(items, "Vegetarian Options")

        elif message == "vegan":
            items = self.menu_service.get_items_by_dietary_preference("vegan")
            return self._format_menu_items(items, "Vegan Options")

        elif message == "gluten-free" or message == "gluten free":
            items = self.menu_service.get_items_by_dietary_preference("gluten-free")
            return self._format_menu_items(items, "Gluten-Free Options")

        elif message == "appetizers":
            items = self.menu_service.get_items_by_category("Appetizers")
            return self._format_menu_items(items, "Appetizers")

        elif message == "main courses" or message == "mains" or message == "entrees":
            items = self.menu_service.get_items_by_category("Main Courses")
            return self._format_menu_items(items, "Main Courses")

        elif message == "desserts":
            items = self.menu_service.get_items_by_category("Desserts")
            return self._format_menu_items(items, "Desserts")

        # Search functionality
        elif "search" in message:
            query = message.replace("search", "").strip()
            if query:
                items = self.menu_service.search_items(query)
                return self._format_menu_items(items, f"Search Results for '{query}'")
            else:
                return "Please specify what you'd like to search for. For example: 'search salmon'"

        # Reservation functionality
        elif "reserve" in message or "reservation" in message or "book" in message:
            return "To make a reservation, please provide your name, contact information, date, time, and party size. For example: 'reserve John Doe, 555-123-4567, 2023-07-15, 19:00, 4'"

        # Help command
        elif message == "help":
            return """
Here are the commands you can use:
- 'menu' - View the full menu
- 'vegetarian', 'vegan', 'gluten-free' - View dietary options
- 'appetizers', 'main courses', 'desserts' - View specific categories
- 'search [query]' - Search for dishes (e.g., 'search salmon')
- 'reserve [details]' - Make a reservation
- 'help' - Show this help message
- 'exit' or 'quit' - End the conversation
"""

        # Default response
        else:
            return "I'm not sure how to respond to that. Type 'help' to see available commands."

    def _format_menu_items(self, items, title):
        """Format a list of menu items for display."""
        if not items:
            return f"No {title.lower()} found."

        result = f"\n{title}:\n" + "-" * 40 + "\n"

        for item in items:
            result += f"{item['name']} - ${item['price']:.2f}\n"
            result += f"  {item['description']}\n"
            if item.get('dietary_info'):
                result += f"  Dietary info: {', '.join(item['dietary_info'])}\n"
            result += f"  Item ID: {item['id']}\n\n"

        return result

    def _format_full_menu(self, menu):
        """Format the full menu for display."""
        result = f"\nToday's Menu ({menu.get('date', 'Today')}):\n" + "=" * 40 + "\n"

        for category in menu.get('categories', []):
            result += f"\n{category['name']}:\n" + "-" * 40 + "\n"

            for item in category.get('items', []):
                result += f"{item['name']} - ${item['price']:.2f}\n"
                result += f"  {item['description']}\n"
                if item.get('dietary_info'):
                    result += f"  Dietary info: {', '.join(item['dietary_info'])}\n"
                result += f"  Item ID: {item['id']}\n\n"

        return result

def main():
    """Main application entry point."""
    # Initialize chatbot
    print("Initializing chatbot...")
    chatbot = SimpleRestaurantChatbot()

    # Clear screen and print header
    clear_screen()
    print_header()

    # Welcome message
    print("Chatbot: Welcome to our restaurant! I can help you browse our menu, search for dishes,")
    print("         and make reservations. Type 'help' to see available commands.")

    # Main conversation loop
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()

        # Check for exit command
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\nChatbot: Thank you for visiting our restaurant. Have a great day!")
            break

        # Process user input
        if user_input:
            response = chatbot.process_message(user_input)
            print(f"\nChatbot: {response}")
        else:
            print("\nChatbot: I didn't catch that. Could you please try again?")

if __name__ == "__main__":
    main()
