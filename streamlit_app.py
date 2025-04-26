import streamlit as st
import json
import os
from datetime import datetime
from menu_service import MenuService
from reservation_service import ReservationService
import config

# Check for environment variables (useful for Docker)
if os.environ.get("OPENAI_API_KEY"):
    config.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

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

# Reservation process tracking
if 'reservation_process' not in st.session_state:
    st.session_state.reservation_process = {
        "active": False,
        "step": 0,
        "data": {}
    }

# Sidebar with options
with st.sidebar:
    st.title("Restaurant Chatbot")
    st.markdown("---")

    # Navigation
    page = st.radio("Navigation", ["Chat", "Menu", "Make Reservation"])

    # Quick action buttons
    st.markdown("---")
    st.markdown("### Quick Actions")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("View Menu"):
            st.session_state.page = "Menu"
            st.rerun()
    with col2:
        if st.button("Make Reservation"):
            st.session_state.page = "Make Reservation"
            st.rerun()

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
        # Get the full menu and format it for display in the chat
        full_menu = menu_service.get_full_menu()
        menu_text = f"**Today's Menu ({full_menu.get('date', 'Today')}):**\n\n"

        for category in full_menu.get('categories', []):
            menu_text += f"**{category['name']}**\n\n"

            for item in category.get('items', []):
                menu_text += f"**{item['name']}** - ${item['price']:.2f}  \n"
                menu_text += f"{item['description']}  \n"
                if item.get('dietary_info'):
                    menu_text += f"*Dietary info: {', '.join(item['dietary_info'])}*  \n"
                menu_text += f"Item ID: {item['id']}  \n\n"

        return menu_text, None

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
        # Start the reservation process
        st.session_state.reservation_process = {
            "active": True,
            "step": 1,
            "data": {
                "customer_name": "",
                "contact_info": "",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": "19:00",
                "party_size": 2,
                "dish_ids": []
            }
        }

        return """Let's make a reservation for you! Please provide the following information:

1. Your name
2. Contact information (phone or email)
3. Date (YYYY-MM-DD)
4. Time (HH:MM)
5. Number of people in your party

You can provide this information in a single message like this:
"Name: John Doe, Contact: john@example.com, Date: 2023-07-15, Time: 19:00, Party: 4"

Or I can guide you through the process step by step. Would you like to proceed?""", None

    # Handle active reservation process
    elif st.session_state.reservation_process["active"]:
        return handle_reservation_chat(message), None

    # Handle adding dishes to a reservation
    elif message == "add dishes" or message == "add dish":
        return "To add dishes to your reservation, please provide your reservation ID:", "add_dishes"

    # Help command
    elif message == "help":
        return """
Here are the commands you can use:
- 'menu' - View the full menu
- 'vegetarian', 'vegan', 'gluten-free' - View dietary options
- 'appetizers', 'main courses', 'desserts' - View specific categories
- 'search [query]' - Search for dishes (e.g., 'search salmon')
- 'reserve' - Make a reservation directly in the chat
- 'add dishes' - Add dishes to an existing reservation
- 'cancel' - Cancel the current reservation process
- 'help' - Show this help message

When making a reservation, you can provide all information at once like this:
"Name: John Doe, Contact: john@example.com, Date: 2023-07-15, Time: 19:00, Party: 4"

Or follow the step-by-step process when prompted.
        """, None

    # Default response
    else:
        return "I'm not sure how to respond to that. Type 'help' to see available commands.", None

def handle_reservation_chat(message):
    """Handle the reservation process in the chat."""
    message = message.lower()
    process = st.session_state.reservation_process

    # Check for cancel command
    if message in ["cancel", "stop", "quit"]:
        st.session_state.reservation_process["active"] = False
        return "Reservation process cancelled. How else can I help you today?"

    # Check if the user provided all information in one message
    if "name:" in message and "contact:" in message and "date:" in message and "time:" in message and "party:" in message:
        # Parse the message for reservation details
        try:
            # Extract name
            name_start = message.find("name:") + 5
            name_end = message.find(",", name_start)
            name = message[name_start:name_end].strip() if name_end != -1 else message[name_start:].strip()

            # Extract contact
            contact_start = message.find("contact:") + 8
            contact_end = message.find(",", contact_start)
            contact = message[contact_start:contact_end].strip() if contact_end != -1 else message[contact_start:].strip()

            # Extract date
            date_start = message.find("date:") + 5
            date_end = message.find(",", date_start)
            date_str = message[date_start:date_end].strip() if date_end != -1 else message[date_start:].strip()

            # Extract time
            time_start = message.find("time:") + 5
            time_end = message.find(",", time_start)
            time_str = message[time_start:time_end].strip() if time_end != -1 else message[time_start:].strip()

            # Extract party size
            party_start = message.find("party:") + 6
            party_end = message.find(",", party_start)
            party_str = message[party_start:party_end].strip() if party_end != -1 else message[party_start:].strip()
            party_size = int(party_str)

            # Create the reservation
            reservation = reservation_service.create_reservation(
                customer_name=name,
                contact_info=contact,
                date=date_str,
                time=time_str,
                party_size=party_size,
                dish_ids=[]
            )

            # Reset the reservation process
            st.session_state.reservation_process["active"] = False

            # Return confirmation message
            return f"""Reservation confirmed!

Name: {name}
Contact: {contact}
Date: {date_str}
Time: {time_str}
Party Size: {party_size}

Your reservation ID is {reservation['id']}.
Would you like to add any dishes to your reservation? Type 'add dishes' to select dishes."""

        except Exception as e:
            return f"""I couldn't process your reservation information. Please make sure it's in the correct format:
"Name: John Doe, Contact: john@example.com, Date: 2023-07-15, Time: 19:00, Party: 4"

Or let me guide you through the process step by step. Just answer the questions as I ask them."""

    # Handle step-by-step reservation process
    step = process["step"]
    data = process["data"]

    if step == 1:  # Name
        data["customer_name"] = message
        process["step"] = 2
        return "Great! Now, please provide your contact information (phone or email):"

    elif step == 2:  # Contact
        data["contact_info"] = message
        process["step"] = 3
        return f"Thank you! What date would you like to make the reservation for? (YYYY-MM-DD, default is {data['date']}):"

    elif step == 3:  # Date
        if message != "":
            try:
                # Validate date format
                datetime.strptime(message, "%Y-%m-%d")
                data["date"] = message
            except ValueError:
                return "Invalid date format. Please use YYYY-MM-DD format:"

        process["step"] = 4
        return f"What time would you like to make the reservation for? (HH:MM, default is {data['time']}):"

    elif step == 4:  # Time
        if message != "":
            try:
                # Validate time format
                datetime.strptime(message, "%H:%M")
                data["time"] = message
            except ValueError:
                return "Invalid time format. Please use HH:MM format (24-hour):"

        process["step"] = 5
        return "How many people will be in your party?"

    elif step == 5:  # Party size
        try:
            party_size = int(message)
            if party_size < 1:
                return "Party size must be at least 1. Please enter a valid number:"

            data["party_size"] = party_size

            # Create the reservation
            reservation = reservation_service.create_reservation(
                customer_name=data["customer_name"],
                contact_info=data["contact_info"],
                date=data["date"],
                time=data["time"],
                party_size=data["party_size"],
                dish_ids=[]
            )

            # Reset the reservation process
            st.session_state.reservation_process["active"] = False

            # Return confirmation message
            return f"""Reservation confirmed!

Name: {data["customer_name"]}
Contact: {data["contact_info"]}
Date: {data["date"]}
Time: {data["time"]}
Party Size: {data["party_size"]}

Your reservation ID is {reservation['id']}.
Would you like to add any dishes to your reservation? Type 'add dishes' to select dishes."""

        except ValueError:
            return "Invalid party size. Please enter a number:"

    return "I'm sorry, there was an error processing your reservation. Please try again or type 'cancel' to stop."

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
        if action == "add_dishes":
            # Store the last message for reference (should be the reservation ID)
            if len(st.session_state.messages) >= 2:
                last_user_message = st.session_state.messages[-2]["content"]
                # Try to find a reservation with this ID
                try:
                    reservation_id = last_user_message.strip()
                    reservation = reservation_service.get_reservation(reservation_id)
                    if reservation:
                        # Store the reservation ID in session state
                        st.session_state.current_reservation_id = reservation_id
                        # Switch to the Make Reservation page
                        st.session_state.page = "Make Reservation"
                        st.rerun()
                    else:
                        # Add error message to chat
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"I couldn't find a reservation with ID: {reservation_id}. Please check the ID and try again."
                        })
                        with st.chat_message("assistant"):
                            st.markdown(f"I couldn't find a reservation with ID: {reservation_id}. Please check the ID and try again.")
                except Exception as e:
                    # Add error message to chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Invalid reservation ID. Please provide a valid reservation ID."
                    })
                    with st.chat_message("assistant"):
                        st.markdown("Invalid reservation ID. Please provide a valid reservation ID.")

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
