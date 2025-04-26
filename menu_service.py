import json
from typing import List, Dict, Any, Optional

class MenuService:
    def __init__(self, menu_file_path: str = "menu_data.json"):
        self.menu_file_path = menu_file_path
        self.menu_data = self._load_menu_data()
    
    def _load_menu_data(self) -> Dict[str, Any]:
        """Load menu data from JSON file."""
        try:
            with open(self.menu_file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading menu data: {e}")
            return {"date": "", "categories": []}
    
    def get_full_menu(self) -> Dict[str, Any]:
        """Get the complete menu."""
        return self.menu_data
    
    def get_menu_date(self) -> str:
        """Get the date of the current menu."""
        return self.menu_data.get("date", "")
    
    def get_categories(self) -> List[str]:
        """Get all menu categories."""
        return [category["name"] for category in self.menu_data.get("categories", [])]
    
    def get_items_by_category(self, category_name: str) -> List[Dict[str, Any]]:
        """Get all items in a specific category."""
        for category in self.menu_data.get("categories", []):
            if category["name"].lower() == category_name.lower():
                return category.get("items", [])
        return []
    
    def search_items(self, query: str) -> List[Dict[str, Any]]:
        """Search for menu items by name or description."""
        results = []
        query = query.lower()
        
        for category in self.menu_data.get("categories", []):
            for item in category.get("items", []):
                if (query in item["name"].lower() or 
                    query in item["description"].lower()):
                    # Add category name to the item for context
                    item_with_category = item.copy()
                    item_with_category["category"] = category["name"]
                    results.append(item_with_category)
        
        return results
    
    def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific menu item by ID."""
        for category in self.menu_data.get("categories", []):
            for item in category.get("items", []):
                if item["id"] == item_id:
                    # Add category name to the item for context
                    item_with_category = item.copy()
                    item_with_category["category"] = category["name"]
                    return item_with_category
        return None
    
    def get_available_items(self) -> List[Dict[str, Any]]:
        """Get all available menu items."""
        available_items = []
        
        for category in self.menu_data.get("categories", []):
            for item in category.get("items", []):
                if item.get("available", False):
                    # Add category name to the item for context
                    item_with_category = item.copy()
                    item_with_category["category"] = category["name"]
                    available_items.append(item_with_category)
        
        return available_items
    
    def get_items_by_dietary_preference(self, preference: str) -> List[Dict[str, Any]]:
        """Get items matching a dietary preference."""
        matching_items = []
        
        for category in self.menu_data.get("categories", []):
            for item in category.get("items", []):
                if preference.lower() in [p.lower() for p in item.get("dietary_info", [])]:
                    # Add category name to the item for context
                    item_with_category = item.copy()
                    item_with_category["category"] = category["name"]
                    matching_items.append(item_with_category)
        
        return matching_items
