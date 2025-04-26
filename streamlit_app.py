import streamlit as st
import json
from datetime import datetime
from menu_service import MenuService
from reservation_service import ReservationService
import config

# Initialize services
menu_service = MenuService()
reservation_service = ReservationService()

# Set page config
st.set_page_config(
    page_title="Restaurant Chatbot",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #f0f2f6;
    }
    .chat-message.bot {
        background-color: #e6f7ff;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message {
        flex: 1;
    }
    .menu-item {
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .menu-item h4 {
        margin-top: 0;
    }
    .menu-item .price {
        font-weight: bold;
        color: #4CAF50;
    }
    .menu-item .dietary {
        font-style: italic;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Welcome to our restaurant! I can help you browse our menu, search for dishes, and make reservations. How can I assist you today?"
    })

if 'reservation_data' not in st.session_state:
    st.session_state.reservation_data = {
        "customer_name": "",
        "contact_info": "",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": "19:00",
        "party_size": 2,
        "dish_ids": []
    }

# Sidebar with options
with st.sidebar:
    st.title("Restaurant Chatbot")
    st.markdown("---")
    
    # Navigation
    page = st.radio("Navigation", ["Chat", "Menu", "Make Reservation"])
    
    st.markdown("---")
    st.markdown("### Quick Commands")
    st.markdown("- Type 'menu' to see the full menu")
    st.markdown("- Type 'vegetarian', 'vegan', or 'gluten-free' to see dietary options")
    st.markdown("- Type 'appetizers', 'main courses', or 'desserts' to see specific categories")
    st.markdown("- Type 'search [query]' to search for dishes")
    st.markdown("- Type 'reserve' to make a reservation")
    st.markdown("- Type 'help' for assistance")

# Helper functions
def format_menu_items(items, title):
    """Format menu items for display."""
    if not items:
        return f"No {title.lower()} found."
    
    result = f"### {title}\n\n"
    
    for item in items:
        result += f"**{item['name']}** - ${item['price']:.2f}  \n"
        result += f"{item['description']}  \n"
        if item.get('dietary_info'):
            result += f"*Dietary info: {', '.join(item['dietary_info'])}*  \n"
        result += f"Item ID: {item['id']}  \n\n"
    
    return result

def display_menu_items_cards(items, title):
    """Display menu items as cards."""
    if not items:
        st.info(f"No {title.lower()} found.")
        return
    
    st.subheader(title)
    
    # Create columns for the menu items (3 items per row)
    cols = st.columns(3)
    
    for i, item in enumerate(items):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"""
                <div class="menu-item">
                    <h4>{item['name']}</h4>
                    <p class="price">${item['price']:.2f}</p>
                    <p>{item['description']}</p>
                    {f'<p class="dietary">Dietary: {", ".join(item["dietary_info"])}</p>' if item.get('dietary_info') else ''}
                    <p><small>Item ID: {item['id']}</small></p>
                </div>
                """, unsafe_allow_html=True)

def process_message(message):
    """Process a user message and return a response."""
    message = message.lower()
    
    # Menu-related commands
    if message == "menu":
        return "Here's our full menu:", "menu_full"
    
    elif message == "vegetarian":
        items = menu_service.get_items_by_dietary_preference("vegetarian")
        return format_menu_items(items, "Vegetarian Options"), None
    
    elif message == "vegan":
        items = menu_service.get_items_by_dietary_preference("vegan")
        return format_menu_items(items, "Vegan Options"), None
    
    elif message == "gluten-free" or message == "gluten free":
        items = menu_service.get_items_by_dietary_preference("gluten-free")
        return format_menu_items(items, "Gluten-Free Options"), None
    
    elif message == "appetizers":
        items = menu_service.get_items_by_category("Appetizers")
        return format_menu_items(items, "Appetizers"), None
    
    elif message == "main courses" or message == "mains" or message == "entrees":
        items = menu_service.get_items_by_category("Main Courses")
        return format_menu_items(items, "Main Courses"), None
    
    elif message == "desserts":
        items = menu_service.get_items_by_category("Desserts")
        return format_menu_items(items, "Desserts"), None
    
    # Search functionality
    elif "search" in message:
        query = message.replace("search", "").strip()
        if query:
            items = menu_service.search_items(query)
            return format_menu_items(items, f"Search Results for '{query}'"), None
        else:
            return "Please specify what you'd like to search for. For example: 'search salmon'", None
    
    # Reservation functionality
    elif message == "reserve" or message == "reservation" or message == "book":
        return "Let's make a reservation for you!", "reservation"
    
    # Help command
    elif message == "help":
        return """
Here are the commands you can use:
- 'menu' - View the full menu
- 'vegetarian', 'vegan', 'gluten-free' - View dietary options
- 'appetizers', 'main courses', 'desserts' - View specific categories
- 'search [query]' - Search for dishes (e.g., 'search salmon')
- 'reserve' - Make a reservation
- 'help' - Show this help message
        """, None
    
    # Default response
    else:
        return "I'm not sure how to respond to that. Type 'help' to see available commands.", None

def display_full_menu():
    """Display the full menu."""
    menu = menu_service.get_full_menu()
    st.header(f"Today's Menu ({menu.get('date', 'Today')})")
    
    for category in menu.get('categories', []):
        display_menu_items_cards(category.get('items', []), category['name'])

def display_chat():
    """Display the chat interface."""
    st.header("Chat with our Restaurant Assistant")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process the message
        response, action = process_message(prompt)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Handle special actions
        if action == "menu_full":
            st.session_state.page = "Menu"
            st.rerun()
        elif action == "reservation":
            st.session_state.page = "Make Reservation"
            st.rerun()

def display_reservation_form():
    """Display the reservation form."""
    st.header("Make a Reservation")
    
    with st.form("reservation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Name", value=st.session_state.reservation_data["customer_name"])
            contact_info = st.text_input("Contact Information (Phone/Email)", value=st.session_state.reservation_data["contact_info"])
            date = st.date_input("Date", value=datetime.strptime(st.session_state.reservation_data["date"], "%Y-%m-%d") if st.session_state.reservation_data["date"] else datetime.now())
        
        with col2:
            time = st.time_input("Time", value=datetime.strptime(st.session_state.reservation_data["time"], "%H:%M").time() if st.session_state.reservation_data["time"] else datetime.strptime("19:00", "%H:%M").time())
            party_size = st.number_input("Party Size", min_value=1, max_value=20, value=st.session_state.reservation_data["party_size"])
        
        # Display available menu items for selection
        st.subheader("Select Dishes (Optional)")
        available_items = menu_service.get_available_items()
        
        # Group items by category
        items_by_category = {}
        for item in available_items:
            category = item.get("category", "Other")
            if category not in items_by_category:
                items_by_category[category] = []
            items_by_category[category].append(item)
        
        # Display items by category with checkboxes
        selected_dishes = []
        for category, items in items_by_category.items():
            st.markdown(f"**{category}**")
            cols = st.columns(3)
            for i, item in enumerate(items):
                with cols[i % 3]:
                    if st.checkbox(f"{item['name']} (${item['price']:.2f})", value=item['id'] in st.session_state.reservation_data["dish_ids"]):
                        selected_dishes.append(item['id'])
        
        # Submit button
        submitted = st.form_submit_button("Make Reservation")
        
        if submitted:
            # Update reservation data
            st.session_state.reservation_data = {
                "customer_name": customer_name,
                "contact_info": contact_info,
                "date": date.strftime("%Y-%m-%d"),
                "time": time.strftime("%H:%M"),
                "party_size": party_size,
                "dish_ids": selected_dishes
            }
            
            # Validate form
            if not customer_name or not contact_info:
                st.error("Please provide your name and contact information.")
            else:
                # Create reservation
                reservation = reservation_service.create_reservation(
                    customer_name=customer_name,
                    contact_info=contact_info,
                    date=date.strftime("%Y-%m-%d"),
                    time=time.strftime("%H:%M"),
                    party_size=party_size,
                    dish_ids=selected_dishes
                )
                
                # Show success message
                st.success(f"Reservation confirmed! Your reservation ID is {reservation['id']}.")
                
                # Add message to chat history
                dishes_text = ""
                if selected_dishes:
                    dish_names = []
                    for dish_id in selected_dishes:
                        dish = menu_service.get_item_by_id(dish_id)
                        if dish:
                            dish_names.append(dish['name'])
                    dishes_text = f" with the following dishes: {', '.join(dish_names)}"
                
                reservation_message = f"Your reservation has been confirmed for {party_size} people on {date.strftime('%Y-%m-%d')} at {time.strftime('%H:%M')}{dishes_text}. Your reservation ID is {reservation['id']}."
                st.session_state.messages.append({"role": "assistant", "content": reservation_message})

# Main content based on selected page
if page == "Chat":
    display_chat()
elif page == "Menu":
    display_full_menu()
elif page == "Make Reservation":
    display_reservation_form()
