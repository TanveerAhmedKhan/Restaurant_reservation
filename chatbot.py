from typing import Dict, List, Any, Optional
import json
from datetime import datetime
from openai import OpenAI
from menu_service import MenuService
from reservation_service import ReservationService
import config

class RestaurantChatbot:
    def __init__(self):
        self.menu_service = MenuService()
        self.reservation_service = ReservationService()
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.MODEL_NAME
        self.conversation_history = []

        # Add system message to conversation history
        self._add_to_history("system", self._get_system_message())

    def _get_system_message(self) -> str:
        """Get the system message for the chatbot."""
        return """You are a helpful restaurant chatbot assistant.
        You can help customers browse the menu, search for dishes, and make reservations.

        When helping customers:
        1. Be friendly and professional
        2. Provide detailed information about dishes when asked
        3. Guide customers through the reservation process
        4. Ask for all necessary information to complete a reservation
        5. Confirm details before finalizing a reservation

        Always format prices with 2 decimal places and a dollar sign (e.g., $12.99).
        When displaying menu items, include the name, description, and price.
        """

    def _add_to_history(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def process_message(self, message: str) -> str:
        """Process a user message and return the chatbot's response."""
        try:
            # Add user message to history
            self._add_to_history("user", message)

            # Process the message based on its content
            response_content = self._handle_user_message(message)

            # Add assistant response to history
            self._add_to_history("assistant", response_content)

            return response_content
        except Exception as e:
            print(f"Error processing message: {e}")
            return "I'm sorry, I encountered an error while processing your request. Please try again."

    def _handle_user_message(self, message: str) -> str:
        """Handle the user message and generate a response."""
        # Check if the message is about the menu
        if any(keyword in message.lower() for keyword in ["menu", "dish", "food", "eat", "cuisine", "appetizer", "dessert", "main course"]):
            return self._handle_menu_query(message)

        # Check if the message is about reservations
        elif any(keyword in message.lower() for keyword in ["reserve", "reservation", "book", "table", "seat", "party", "people"]):
            return self._handle_reservation_query(message)

        # For general queries, use the OpenAI API
        else:
            return self._get_ai_response()

    def _handle_menu_query(self, message: str) -> str:
        """Handle menu-related queries."""
        # Check for specific menu queries
        if "vegetarian" in message.lower():
            vegetarian_items = self.menu_service.get_items_by_dietary_preference("vegetarian")
            return self._format_menu_items(vegetarian_items, "Vegetarian dishes")

        elif "vegan" in message.lower():
            vegan_items = self.menu_service.get_items_by_dietary_preference("vegan")
            return self._format_menu_items(vegan_items, "Vegan dishes")

        elif "gluten-free" in message.lower() or "gluten free" in message.lower():
            gf_items = self.menu_service.get_items_by_dietary_preference("gluten-free")
            return self._format_menu_items(gf_items, "Gluten-free dishes")

        elif "appetizer" in message.lower():
            appetizers = self.menu_service.get_items_by_category("Appetizers")
            return self._format_menu_items(appetizers, "Appetizers")

        elif "main" in message.lower() or "entree" in message.lower():
            mains = self.menu_service.get_items_by_category("Main Courses")
            return self._format_menu_items(mains, "Main Courses")

        elif "dessert" in message.lower():
            desserts = self.menu_service.get_items_by_category("Desserts")
            return self._format_menu_items(desserts, "Desserts")

        # For general menu queries or searches
        else:
            # Try to find specific dishes mentioned in the message
            search_results = self.menu_service.search_items(message)
            if search_results:
                return self._format_menu_items(search_results, "Menu items matching your query")
            else:
                # If no specific dishes found, show the full menu
                full_menu = self.menu_service.get_full_menu()
                return self._format_full_menu(full_menu)

    def _handle_reservation_query(self, message: str) -> str:
        """Handle reservation-related queries."""
        # For now, just use the AI to respond to reservation queries
        # In a real implementation, we would parse the message for reservation details
        return self._get_ai_response()

    def _format_menu_items(self, items: List[Dict[str, Any]], title: str) -> str:
        """Format a list of menu items for display."""
        if not items:
            return "I couldn't find any dishes matching your criteria."

        result = f"**{title}:**\n\n"
        for item in items:
            result += f"**{item['name']}** - ${item['price']:.2f}\n"
            result += f"{item['description']}\n"
            if item.get('dietary_info'):
                result += f"*Dietary info: {', '.join(item['dietary_info'])}*\n"
            result += f"Item ID: {item['id']}\n\n"

        return result

    def _format_full_menu(self, menu: Dict[str, Any]) -> str:
        """Format the full menu for display."""
        result = f"**Today's Menu ({menu.get('date', 'Today')}):**\n\n"

        for category in menu.get('categories', []):
            result += f"**{category['name']}**\n\n"

            for item in category.get('items', []):
                result += f"**{item['name']}** - ${item['price']:.2f}\n"
                result += f"{item['description']}\n"
                if item.get('dietary_info'):
                    result += f"*Dietary info: {', '.join(item['dietary_info'])}*\n"
                result += f"Item ID: {item['id']}\n\n"

        return result

    def _get_ai_response(self) -> str:
        """Get a response from the OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting AI response: {e}")
            return "I'm sorry, I'm having trouble connecting to my AI service. Please try again later."
