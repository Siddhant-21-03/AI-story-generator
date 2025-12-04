import streamlit as st
import os 
from dotenv import load_dotenv
from datetime import datetime
from auth import check_authentication, logout
from database import Database
from history import show_history_page
from huggingface_client import generate_story

load_dotenv()

YOUR_HF_TOKEN = os.getenv("HF_TOKEN")

GENRES = ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Adventure", "Comedy", "Drama", "Thriller"]

GENRE_PROMPTS = {
    "Fantasy": "Include magical elements, mythical creatures, and an epic quest.",
    "Sci-Fi": "Set in the future with advanced technology and space exploration themes.",
    "Mystery": "Include a puzzling crime or enigma that needs to be solved.",
    "Romance": "Focus on emotional connections and relationship development.",
    "Horror": "Create suspense and fear with dark, eerie atmospheres.",
    "Adventure": "Include thrilling journeys and daring exploits.",
    "Comedy": "Make it humorous with witty dialogue and funny situations.",
    "Drama": "Focus on serious themes and character conflicts.",
    "Thriller": "Build tension with fast-paced action and unexpected twists."
}


# Streamlit UI - MUST BE FIRST
st.set_page_config(page_title="AI Story Generator", page_icon="📖", layout="wide")

# Check authentication
user = check_authentication()

# Initialize database
db = Database()
db.create_or_update_user(user['user_id'], user['email'], user['display_name'])

# Custom CSS
st.markdown("""
    <style>
    /* Main app background with animated gradient */
    .main {
        background: #0a0e27;
        background-image: 
            radial-gradient(at 20% 30%, rgba(233, 69, 96, 0.1) 0px, transparent 50%),
            radial-gradient(at 80% 20%, rgba(59, 130, 246, 0.1) 0px, transparent 50%),
            radial-gradient(at 40% 80%, rgba(139, 92, 246, 0.1) 0px, transparent 50%);
        min-height: 100vh;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #0a0e27 100%);
        border-right: 2px solid rgba(233, 69, 96, 0.3);
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #f1f5f9;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #e94560 !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
    }
    
    /* Headers with improved typography */
    h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 3rem !important;
        text-shadow: 0 0 30px rgba(233, 69, 96, 0.4);
        letter-spacing: -0.02em !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
        font-size: 1.75rem !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Text areas and inputs with glassmorphism */
    .stTextArea textarea, .stTextInput input {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
        color: #f1f5f9 !important;
        border: 2px solid #334155 !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #e94560 !important;
        background: rgba(10, 14, 39, 0.95) !important;
        box-shadow: 0 0 0 4px rgba(233, 69, 96, 0.2) !important;
        outline: none !important;
    }
    
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: #64748b !important;
    }
    
    /* Primary buttons with enhanced effects */
    .stButton>button[kind="primary"], .stButton>button:not([kind="secondary"]) {
        background: linear-gradient(135deg, #e94560 0%, #c72c3f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 32px !important;
        font-weight: 700 !important;
        font-size: 17px !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(233, 69, 96, 0.4) !important;
        text-transform: uppercase !important;
    }
    
    .stButton>button[kind="primary"]:hover, .stButton>button:not([kind="secondary"]):hover {
        background: linear-gradient(135deg, #ff5c7c 0%, #e94560 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(233, 69, 96, 0.6) !important;
    }
    
    /* Secondary buttons */
    .stButton>button[kind="secondary"] {
        background: rgba(59, 130, 246, 0.2) !important;
        color: #60a5fa !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button[kind="secondary"]:hover {
        background: rgba(59, 130, 246, 0.3) !important;
        border-color: #60a5fa !important;
        transform: translateY(-2px) !important;
    }
    
    /* Metrics with card design */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(233, 69, 96, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #e94560 !important;
        text-shadow: 0 2px 10px rgba(233, 69, 96, 0.3);
    }
    
    div[data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Select boxes */
    .stSelectbox label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
        color: #f1f5f9 !important;
        border: 2px solid #334155 !important;
        border-radius: 12px !important;
    }
    
    /* Sliders */
    .stSlider label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    
    .stSlider [data-baseweb="slider"] {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Dividers */
    hr {
        border-color: rgba(233, 69, 96, 0.2) !important;
        margin: 2rem 0 !important;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.5) !important;
    }
    
    /* Alert messages */
    .stSuccess {
        background: rgba(34, 197, 94, 0.15) !important;
        border-left: 4px solid #22c55e !important;
        color: #86efac !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        border-left: 4px solid #ef4444 !important;
        color: #fca5a5 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .stWarning {
        background: rgba(251, 146, 60, 0.15) !important;
        border-left: 4px solid #fb923c !important;
        color: #fdba74 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15) !important;
        border-left: 4px solid #3b82f6 !important;
        color: #93c5fd !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    /* Markdown content */
    .stMarkdown {
        color: #e2e8f0 !important;
    }
    
    .stMarkdown p {
        line-height: 1.7 !important;
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    .stRadio [role="radiogroup"] {
        background: rgba(15, 23, 42, 0.5);
        padding: 1rem;
        border-radius: 12px;
    }
    
    /* Captions */
    .caption {
        color: #94a3b8 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #e94560 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown(f"### 👤 {user['display_name']}")
    st.caption(f"📧 {user['email']}")
    st.divider()
    
    page = st.radio(
        "Navigation",
        ["✍️ Generate Story", "📚 My Library"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    if st.button("🚪 Logout", use_container_width=True):
        logout()

# Show selected page
if page == "📚 My Library":
    show_history_page(user['user_id'])
else:
    # Main story generation page
    st.title("📖 AI Story Generator")
    st.markdown("### Create amazing stories with AI")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        prompt = st.text_area(
            "🎨 Your Story Idea",
            height=120,
            placeholder="Example: A robot who discovers they have emotions...",
            help="Describe what you want your story to be about"
        )
        
        title = st.text_input(
            "📝 Story Title",
            placeholder="My Amazing Story",
            help="Give your story a catchy title"
        )
    
    with col2:
        st.markdown("#### ⚙️ Settings")
        
        genre = st.selectbox(
            "Genre",
            GENRES,
            help="Choose your story genre"
        )
        
        creativity = st.slider(
            "Creativity",
            0.1, 1.0, 0.7, 0.05,
            help="Higher values = more creative and unpredictable"
        )
        
        length = st.slider(
            "Length (words)",
            100, 800, 300, 50,
            help="Approximate word count"
        )
        
        tags_input = st.text_input(
            "Tags (comma-separated)",
            placeholder="adventure, hero, quest",
            help="Add tags to organize your stories"
        )
    
    if st.button("✨ Generate Story", type="primary", use_container_width=True, key="generate_story_btn") and prompt:
        if not title:
            st.warning("Please provide a title for your story")
        else:
            st.info("⏳ Trying HF API first...")
            with st.spinner(f"🎭 Crafting your {genre} story..."):
                story = generate_story(prompt, genre, creativity, length)
            
            if story and isinstance(story, str) and not story.startswith("Unable"):
                st.success("✅ Story generated successfully!")
                
                # Save to database
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
                story_id = db.save_story(
                    user_id=user['user_id'],
                    title=title,
                    prompt=prompt,
                    content=story,
                    genre=genre,
                    creativity=creativity,
                    tags=tags
                )
                
                st.markdown("---")
                st.markdown(f"## {title}")
                st.markdown(story)
                
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        "💾 Download",
                        story,
                        f"{title.replace(' ', '_')}.md",
                        mime="text/markdown",
                        key="download_story_btn"
                    )
                
                with col2:
                    if st.button("🔄 Generate Another", key="generate_another_btn"):
                        st.rerun()
                
                with col3:
                    if st.button("📚 View Library", key="view_library_btn"):
                        st.session_state['page'] = "📚 My Library"
                        st.rerun()
            else:
                st.error(story)
    elif st.button("✨ Generate Story", type="primary", use_container_width=True, key="generate_story_empty_btn"):
        st.warning("Please enter a story idea first!")
    
    # Quick stats
    stats = db.get_stats(user['user_id'])
    if stats['total_stories'] > 0:
        st.markdown("---")
        st.markdown("### 📊 Your Stats")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Stories Created", stats['total_stories'])
        with col2:
            st.metric("Total Words", f"{stats['total_words']:,}")
        with col3:
            st.metric("Favorite Stories", stats['favorite_count'])

# Token verification
if YOUR_HF_TOKEN == "hf_your_actual_token_here":
    st.error("⚠️ Please set your Hugging Face token in the .env file")