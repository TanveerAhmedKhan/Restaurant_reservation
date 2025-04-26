# Restaurant Chatbot

A chatbot for a restaurant that helps users search the menu and make reservations using OpenAI's GPT-4o model and LangChain.

## Features

- Browse the restaurant's menu
- Search for specific dishes by name, description, or dietary preferences
- Make reservations for dishes
- Natural language interaction

## Requirements

- Python 3.8+
- OpenAI API key

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd restaurant-chatbot
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Open the `.env` file
   - Replace `your_openai_api_key_here` with your actual OpenAI API key

## Usage

Run the application:
```
python app.py
```

### Example Interactions

- "What's on the menu today?"
- "Do you have any vegetarian options?"
- "Tell me about your desserts"
- "I'd like to reserve a table for 4 people tomorrow at 7 PM"
- "Can I order the Grilled Salmon?"

## Project Structure

- `app.py` - Main application entry point
- `chatbot.py` - Chatbot implementation using LangChain
- `menu_service.py` - Service for menu-related operations
- `reservation_service.py` - Service for reservation-related operations
- `config.py` - Configuration settings
- `menu_data.json` - Sample menu data
- `reservations.json` - Reservation data (created when first reservation is made)

## Customization

You can customize the menu by editing the `menu_data.json` file. The structure should be maintained as follows:

```json
{
  "date": "YYYY-MM-DD",
  "categories": [
    {
      "name": "Category Name",
      "items": [
        {
          "id": "unique_id",
          "name": "Item Name",
          "description": "Item Description",
          "price": 0.00,
          "available": true,
          "dietary_info": ["vegetarian", "gluten-free", etc.]
        }
      ]
    }
  ]
}
```
