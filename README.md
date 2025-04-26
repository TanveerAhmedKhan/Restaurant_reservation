# Restaurant Chatbot

A chatbot for a restaurant that helps users search the menu and make reservations using OpenAI's GPT-4o model and LangChain. The application includes both a command-line interface and a web interface built with Streamlit.

## Features

- Browse the restaurant's menu
- Search for specific dishes by name, description, or dietary preferences
- Make reservations for dishes
- Natural language interaction
- Web interface with Streamlit
- Docker support for easy deployment

## Requirements

- Python 3.8+
- OpenAI API key
- Docker (optional, for containerized deployment)

## Installation and Setup

### Option 1: Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/TanveerAhmedKhan/Restaurant_reservation.git
   cd Restaurant_reservation
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_openai_api_key_here`

### Option 2: Docker Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/TanveerAhmedKhan/Restaurant_reservation.git
   cd Restaurant_reservation
   ```

2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Build and run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

## Usage

### Command-line Interface

Run the command-line application:
```bash
python app.py
```

### Web Interface (Streamlit)

Run the Streamlit web application:
```bash
streamlit run streamlit_app.py
```

If using Docker, the Streamlit app will be available at:
```
http://localhost:8080
```

### Example Interactions

- "What's on the menu today?"
- "Do you have any vegetarian options?"
- "Tell me about your desserts"
- "I'd like to reserve a table for 4 people tomorrow at 7 PM"
- "Can I order the Grilled Salmon?"

## Project Structure

- `app.py` - Command-line interface application
- `streamlit_app.py` - Streamlit web interface
- `chatbot.py` - Chatbot implementation using LangChain
- `menu_service.py` - Service for menu-related operations
- `reservation_service.py` - Service for reservation-related operations
- `config.py` - Configuration settings
- `menu_data.json` - Sample menu data
- `reservations.json` - Reservation data (created when first reservation is made)
- `Dockerfile` - Docker configuration for containerization
- `docker-compose.yml` - Docker Compose configuration for easy deployment

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
