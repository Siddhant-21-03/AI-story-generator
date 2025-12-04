"""Authentication module using Streamlit-Authenticator"""
import streamlit as st
from typing import Optional, Dict
import hashlib
import json
import os
from datetime import datetime

class SimpleAuth:
    """Simple authentication system for demo purposes"""
    
    def __init__(self, users_file: str = "users.json"):
        self.users_file = users_file
        self.load_users()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            self.save_users()
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, email: str, password: str, display_name: str) -> tuple[bool, str]:
        """Register a new user"""
        if email in self.users:
            return False, "Email already registered"
        
        user_id = hashlib.md5(email.encode()).hexdigest()
        self.users[email] = {
            'user_id': user_id,
            'email': email,
            'password': self.hash_password(password),
            'display_name': display_name,
            'created_at': datetime.now().isoformat()
        }
        self.save_users()
        return True, user_id
    
    def login_user(self, email: str, password: str) -> tuple[bool, Optional[Dict]]:
        """Login user"""
        if email not in self.users:
            return False, None
        
        user = self.users[email]
        if user['password'] == self.hash_password(password):
            return True, {
                'user_id': user['user_id'],
                'email': user['email'],
                'display_name': user['display_name']
            }
        return False, None
    
    def get_user_info(self, email: str) -> Optional[Dict]:
        """Get user information"""
        if email in self.users:
            user = self.users[email]
            return {
                'user_id': user['user_id'],
                'email': user['email'],
                'display_name': user['display_name']
            }
        return None


def show_auth_page():
    """Display authentication page"""
    # Custom CSS for better styling
    st.markdown("""
        <style>
        /* Modern dark theme with improved contrast */
        .main {
            background: #0a0e27;
            background-image: 
                radial-gradient(at 40% 20%, rgba(233, 69, 96, 0.15) 0px, transparent 50%),
                radial-gradient(at 80% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 0% 50%, rgba(139, 92, 246, 0.15) 0px, transparent 50%);
        }
        
        /* Main container */
        .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
        }
        
        /* Header styling */
        h1 {
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 2.5rem !important;
            margin-bottom: 0.5rem !important;
            text-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
        }
        
        h2 {
            color: #e94560 !important;
            font-weight: 700 !important;
            font-size: 1.75rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        h3 {
            color: #cbd5e1 !important;
            font-weight: 600 !important;
            font-size: 1.25rem !important;
            margin-bottom: 2rem !important;
        }
        
        /* Form container with glassmorphism */
        div[data-testid="stForm"] {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(20px);
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 
                0 0 0 1px rgba(233, 69, 96, 0.1),
                0 20px 60px rgba(0, 0, 0, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(233, 69, 96, 0.2);
        }
        
        /* Input field labels */
        label {
            color: #e2e8f0 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            margin-bottom: 0.5rem !important;
            letter-spacing: 0.025em !important;
        }
        
        /* Input fields */
        .stTextInput input {
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
            border: 2px solid #334155 !important;
            border-radius: 12px !important;
            padding: 14px 16px !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput input:focus {
            border-color: #e94560 !important;
            background-color: #0f172a !important;
            box-shadow: 0 0 0 4px rgba(233, 69, 96, 0.15) !important;
            outline: none !important;
        }
        
        .stTextInput input::placeholder {
            color: #64748b !important;
        }
        
        /* Buttons */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #e94560 0%, #c72c3f 100%);
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 17px;
            letter-spacing: 0.5px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 20px rgba(233, 69, 96, 0.4);
            cursor: pointer;
            text-transform: uppercase;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #ff5c7c 0%, #e94560 100%);
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(233, 69, 96, 0.6);
        }
        
        .stButton>button:active {
            transform: translateY(-1px);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background: transparent;
            border-bottom: 2px solid #1e293b;
            padding-bottom: 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            color: #94a3b8;
            border-radius: 12px 12px 0 0;
            padding: 14px 32px;
            font-weight: 600;
            font-size: 16px;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(233, 69, 96, 0.1);
            color: #e94560;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #e94560 0%, #c72c3f 100%);
            color: white !important;
            box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);
        }
        
        /* Tab panels */
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 2rem;
        }
        
        /* Error/Success messages */
        .stAlert {
            border-radius: 12px;
            border: none;
            padding: 1rem 1.25rem;
            font-weight: 500;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("📖 AI Story Generator")
        st.markdown("### Welcome! Please sign in to continue")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        auth = SimpleAuth()
        
        with tab1:
            with st.form("login_form"):
                st.subheader("Login to Your Account")
                email = st.text_input("Email", placeholder="your.email@example.com")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", type="primary")
                
                if submit:
                    if not email or not password:
                        st.error("Please fill in all fields")
                    else:
                        success, user_info = auth.login_user(email, password)
                        if success:
                            st.session_state['authenticated'] = True
                            st.session_state['user'] = user_info
                            st.success("Login successful! Redirecting...")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
        
        with tab2:
            with st.form("signup_form"):
                st.subheader("Create New Account")
                new_name = st.text_input("Display Name", placeholder="John Doe")
                new_email = st.text_input("Email", placeholder="your.email@example.com", key="signup_email")
                new_password = st.text_input("Password", type="password", key="signup_password")
                new_password_confirm = st.text_input("Confirm Password", type="password")
                signup = st.form_submit_button("Sign Up", type="primary")
                
                if signup:
                    if not all([new_name, new_email, new_password, new_password_confirm]):
                        st.error("Please fill in all fields")
                    elif new_password != new_password_confirm:
                        st.error("Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        success, result = auth.register_user(new_email, new_password, new_name)
                        if success:
                            st.success("Account created! Please login.")
                        else:
                            st.error(result)


def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if not st.session_state['authenticated']:
        show_auth_page()
        st.stop()
    
    return st.session_state.get('user', {})


def logout():
    """Logout user"""
    st.session_state['authenticated'] = False
    st.session_state['user'] = None
    st.rerun()
