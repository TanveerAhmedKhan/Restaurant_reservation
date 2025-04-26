import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class ReservationService:
    def __init__(self, reservation_file_path: str = "reservations.json"):
        self.reservation_file_path = reservation_file_path
        self.reservations = self._load_reservations()
    
    def _load_reservations(self) -> List[Dict[str, Any]]:
        """Load reservations from JSON file."""
        if not os.path.exists(self.reservation_file_path):
            return []
        
        try:
            with open(self.reservation_file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading reservations: {e}")
            return []
    
    def _save_reservations(self) -> None:
        """Save reservations to JSON file."""
        try:
            with open(self.reservation_file_path, 'w') as file:
                json.dump(self.reservations, file, indent=2)
        except Exception as e:
            print(f"Error saving reservations: {e}")
    
    def create_reservation(self, 
                          customer_name: str, 
                          contact_info: str,
                          date: str,
                          time: str,
                          party_size: int,
                          dish_ids: List[str] = None) -> Dict[str, Any]:
        """Create a new reservation."""
        # Generate a simple reservation ID
        reservation_id = f"RES{len(self.reservations) + 1:04d}"
        
        # Create reservation object
        reservation = {
            "id": reservation_id,
            "customer_name": customer_name,
            "contact_info": contact_info,
            "date": date,
            "time": time,
            "party_size": party_size,
            "dish_ids": dish_ids or [],
            "created_at": datetime.now().isoformat(),
            "status": "confirmed"
        }
        
        # Add to reservations list
        self.reservations.append(reservation)
        
        # Save to file
        self._save_reservations()
        
        return reservation
    
    def get_reservation(self, reservation_id: str) -> Optional[Dict[str, Any]]:
        """Get a reservation by ID."""
        for reservation in self.reservations:
            if reservation["id"] == reservation_id:
                return reservation
        return None
    
    def update_reservation(self, reservation_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing reservation."""
        for i, reservation in enumerate(self.reservations):
            if reservation["id"] == reservation_id:
                # Update reservation with new values
                self.reservations[i] = {**reservation, **updates}
                # Save changes
                self._save_reservations()
                return self.reservations[i]
        return None
    
    def cancel_reservation(self, reservation_id: str) -> bool:
        """Cancel a reservation."""
        for i, reservation in enumerate(self.reservations):
            if reservation["id"] == reservation_id:
                # Update status to cancelled
                self.reservations[i]["status"] = "cancelled"
                # Save changes
                self._save_reservations()
                return True
        return False
    
    def get_reservations_by_date(self, date: str) -> List[Dict[str, Any]]:
        """Get all reservations for a specific date."""
        return [r for r in self.reservations if r["date"] == date and r["status"] != "cancelled"]
    
    def add_dish_to_reservation(self, reservation_id: str, dish_id: str) -> bool:
        """Add a dish to an existing reservation."""
        for i, reservation in enumerate(self.reservations):
            if reservation["id"] == reservation_id:
                if dish_id not in reservation["dish_ids"]:
                    self.reservations[i]["dish_ids"].append(dish_id)
                    # Save changes
                    self._save_reservations()
                return True
        return False
