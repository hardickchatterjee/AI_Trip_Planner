import streamlit as st
import requests
import datetime

# from exception.exceptions import TradingBotException
import sys

BASE_URL = "http://localhost:8000"  # Backend endpoint

# Page Configuration
st.set_page_config(
    page_title="🌍 Travel Planner Agentic Application",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "AI Travel Planner - Your personal AI travel assistant powered by advanced agentic workflows"
    }
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .trip-card {
        padding: 1.5rem;
        background-color: #fafafa;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "trip_count" not in st.session_state:
    st.session_state.trip_count = 0

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 🎯 Quick Options")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("📝 Reset", use_container_width=True):
            st.session_state.trip_count = 0
            st.rerun()
    
    st.markdown("---")
    
    with st.expander("💡 **Trip Planning Tips**", expanded=False):
        st.markdown("""
        **Best Practices:**
        - Be specific about dates and duration
        - Mention your budget preferences
        - Include any special interests
        - Tell us about travel party size
        - Specify dietary preferences
        
        **Popular Destinations:**
        - Mountains & Trekking
        - Beach & Island Escapes
        - Cultural Heritage
        - Adventure Sports
        - Food Tours
        """)
    
    with st.expander("📊 **Chat Statistics**", expanded=False):
        st.metric("Total Trips Planned", st.session_state.trip_count)
        st.metric("Messages in Chat", len(st.session_state.messages))
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    backend_url = st.text_input("Backend URL", value=BASE_URL)

# Main Content Area
st.markdown("""
    <div class="main-header">
        <h1>🌍 Travel Planner Agentic Application</h1>
        <p style="font-size: 1.1rem; margin-top: 0.5rem;">Your AI-Powered Travel Planning Assistant</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🗣️ Chat with Your Travel Agent")

with col2:
    st.markdown(f"### 📌 Chats: {len(st.session_state.messages)//2 if st.session_state.messages else 0}")

# Display Chat History
if st.session_state.messages:
    st.markdown("---")
    st.markdown("### 📖 Conversation History")
    
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You:</strong><br>{msg["content"]}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Travel Agent:</strong><br>{msg["content"][:500]}{'...' if len(msg["content"]) > 500 else ''}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")

# Chat Input Form
st.markdown("### ✍️ Plan Your Next Adventure")

with st.form(key="query_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "What trip would you like to plan?",
            placeholder="e.g., Plan a 5-day trip to Goa with beach activities and local cuisine",
            label_visibility="collapsed"
        )
    
    with col2:
        submit_button = st.form_submit_button("🚀 Send", use_container_width=True)

# Handle User Input
if submit_button and user_input.strip():
    try:
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Show loading state
        with st.spinner("🤖 Your travel agent is thinking..."):
            payload = {"question": user_input}
            response = requests.post(f"{backend_url}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            
            # Add assistant message to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })
            
            st.session_state.trip_count += 1
            
            # Display the formatted response
            st.markdown("---")
            st.markdown("### 🎒 Your Travel Plan")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.metric("🗓️ Generated", datetime.datetime.now().strftime('%m-%d %H:%M'))
            with col2:
                st.metric("👤 Agent", "AI Planner")
            with col3:
                st.metric("📍 Status", "Ready")
            
            st.markdown("---")
            
            # Display the travel plan in an organized way
            with st.container(border=True):
                st.markdown(f"""
                **Generated:** {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M')}  
                **Created by:** Atriyo's AI Travel Agent

                ---

                {answer}

                ---

                **⚠️ Disclaimer:** This travel plan was generated by AI. Please verify all information, especially prices, operating hours, and travel requirements before your trip.
                """)
            
            st.success("✅ Travel plan created successfully!")
            st.rerun()
        else:
            st.error(f"❌ Bot failed to respond: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Please ensure the backend server is running.")
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: gray;">
        <p>🌟 <strong>Travel Planner Agentic Application</strong> | Powered by AI & Advanced Workflows</p>
        <p style="font-size: 0.85rem;">Made with ❤️ for travel enthusiasts</p>
    </div>
    """, unsafe_allow_html=True)