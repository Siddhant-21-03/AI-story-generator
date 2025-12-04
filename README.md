# 📖 AI Story Generator - Production Edition

A professional AI-powered story generation application with **intelligent multi-tier template system**, user authentication, and comprehensive story management. Perfect for demonstrating full-stack development, database design, and production-ready architecture.

## 🎯 **Key Features for Technical Interviews**

### **Smart Rule-Based Story Generation** ✨
- Dynamic template system with 5 calibrated tiers (150/250/400/600/800+ words)
- Genre-specific storytelling (9 genres with custom narrative structures)
- Instant generation (no API delays or model downloads)
- Accurate word count control validated across all ranges

**Why this matters:** Demonstrates:
- Algorithm design and tier-based scaling
- Template engineering for consistent output quality
- Performance optimization (instant vs. API latency)
- User experience focus (reliability over complexity)

### **Production Architecture** 🏗️
```
Frontend (Streamlit)
    ↓
Story Generator (Rule-Based Engine)
    ↓
SQLite Database (Persistent Storage)
    ↓
User Stories & Analytics
```

### **Production Patterns Demonstrated**
- ✅ Clean separation of concerns (app/auth/database/generator modules)
- ✅ Type hints throughout for maintainability
- ✅ Comprehensive error handling
- ✅ Secure authentication (SHA-256 hashing)
- ✅ Database design with proper relationships
- ✅ RESTful CRUD operations
- ✅ Session management

---

## 🌟 Full Feature Set

### Core Story Generation
- **Smart Template Engine**: Rule-based generation with 5 calibrated word-count tiers
- **Multi-Genre Support**: 9 specialized genres (Fantasy, Sci-Fi, Mystery, Romance, Horror, Adventure, Comedy, Drama, Thriller)
- **Customizable Parameters**: Adjust creativity and story length (100-800 words)
- **Instant Generation**: No API delays, no model downloads required

### User Management
- **Authentication System**: Secure login/signup with SHA-256 password hashing
- **User Profiles**: Track user information and activity
- **Session Management**: Persistent login sessions across app restarts

### Story Management
- **SQLite Database**: Persistent storage with full CRUD operations
- **Full CRUD Operations**: Create, Read, Update, Delete stories
- **Story Library**: View all your generated stories
- **Favorites System**: Mark and filter favorite stories
- **Edit Stories**: Modify title, content, genre, and tags
- **Download Stories**: Export stories as Markdown files

### Search & Organization
- **Advanced Search**: Search by title, content, or prompt
- **Genre Filtering**: Filter stories by genre
- **Favorites Filter**: View only favorite stories
- **Tagging System**: Organize stories with custom tags
- **Statistics Dashboard**: Track story count, word count, and genre breakdown

## 🚀 Quick Start

### 1. Setup Environment
```powershell
# Navigate to project
cd d:\str-gen

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application
```powershell
streamlit run app.py
```

### 3. Access the App
Open your browser and navigate to `http://localhost:8501`

### 4. Create Account & Generate Stories
1. Click "Sign Up" to create an account
2. Login with your credentials
3. Go to "Generate Story" page
4. Enter your story idea (e.g., "A dragon learns to code")
5. Select genre and adjust word count (100-800 words)
6. Click "Generate Story" - instant results!
6. Click "Generate Story" - instant results!
7. View your stories in "My Library"

---

## 📁 Project Structure

```
str-gen/
├── app.py                  # Main Streamlit application
├── huggingface_client.py   # Story generation engine (rule-based)
├── database.py             # SQLite with CRUD operations
├── auth.py                 # User authentication (SHA-256)
├── history.py              # Story management UI
├── requirements.txt        # Python dependencies
├── .gitignore              # Protects secrets and cache
├── stories.db              # SQLite database (auto-generated)
└── users.json              # User credentials (auto-generated)
```
├── stories.db          # SQLite database (auto-generated)
└── users.json          # User credentials (auto-generated)
```

---

## 🎤 **Interview Talking Points**

### **"Tell me about your story generation system"**

*"I built an intelligent rule-based story generator with a 5-tier template system that scales from 100 to 800+ words. Each tier has calibrated sentence counts and lengths—for example, the 800-word tier uses 17 sentences averaging 45-50 words each.*

*The key challenge was accurate word count control. I validated the algorithm across all ranges and achieved consistent accuracy. The system generates stories instantly—no API latency, no rate limits, perfect for production reliability.*

*For real AI integration, I'd use HF Inference Endpoints or OpenAI, but this demonstrates algorithm design and performance optimization."*

### **"How does your database architecture work?"**

*"I designed a normalized SQLite schema with two main tables: users and stories. Stories include metadata like genre, creativity level, word count, tags (JSON), and favorite status.*

*I implemented full CRUD operations with proper error handling, parameterized queries to prevent SQL injection, and search functionality with multiple filters. The database module is completely decoupled from the UI using clean interfaces."*

### **"Walk me through the authentication system"**

*"I built secure authentication using SHA-256 password hashing—never storing plaintext passwords. The system uses Streamlit's session state for persistent login across page reloads.*

*User IDs are generated from emails, and all database operations are scoped to the authenticated user. For production, I'd upgrade to bcrypt or Argon2, add rate limiting, and implement JWT tokens for API access."*

### **"Show me the code architecture"**

**Live Demo:**
1. Show separation of concerns: `app.py` (UI) → `huggingface_client.py` (logic) → `database.py` (data)
2. Generate a story - instant results
3. Show database file with saved stories
4. Explain type hints and error handling throughout

---

## 🎯 Usage Guide

### Generating Stories
1. Navigate to "Generate Story" page
2. Enter your story idea (e.g., "A dragon learns to code")
3. Provide a title
4. Select genre, creativity level, and word count (100-800)
5. Add tags like `#fantasy #tech` (optional)
6. Click "Generate Story" - instant results!

### Managing Stories
1. Navigate to "My Library"
2. View all your stories with search/filter
3. **View** - Read full story
4. **Edit** - Modify title, content, genre, tags
5. **Download** - Export as Markdown
6. **Delete** - Remove permanently
7. Toggle ⭐ for favorites

### Statistics Dashboard
- Total stories & words written
- Genre breakdown chart
- Recent activity
- Favorite count

---

## 🛠️ Technologies Used

- **Frontend**: Streamlit (modern glassmorphism UI)
- **Backend**: Python 3.13
- **Database**: SQLite3 with full CRUD
- **AI Models**: 
  - Primary: HF Router API (gpt2, gpt-neo-1.3B, bloom-560m)
  - Fallback: Local transformers pipeline
- **Authentication**: SHA-256 hash-based with session management
- **API Integration**: requests + huggingface-hub
- **Environment Management**: python-dotenv

## 📊 Database Schema

### Users Table
- user_id (PRIMARY KEY)
- email (UNIQUE)
- display_name
- photo_url
- created_at
- last_login

### Stories Table
- story_id (PRIMARY KEY, AUTO-INCREMENT)
- user_id (FOREIGN KEY)
- title
- prompt
- content
- genre
- creativity
- word_count
- created_at
- updated_at
- is_favorite
- tags (JSON)

## 🔐 Security Features

- ✅ Password hashing with SHA-256
- ✅ Session-based authentication
- ✅ User-specific data isolation
- ✅ SQL injection protection (parameterized queries)
- ✅ Type hints throughout for code safety
- ✅ Proper error handling and validation

---

## 🎓 **What This Project Demonstrates**

✅ **Full-stack development** (Frontend UI + Backend logic + Database)  
✅ **Clean architecture** (Separation of concerns, modular design)  
✅ **Algorithm design** (Multi-tier template system with word count calibration)  
✅ **Database design** (Normalized schema, CRUD operations, search/filter)  
✅ **Authentication & security** (Password hashing, session management)  
✅ **Production patterns** (Error handling, type hints, validation)  
✅ **User experience** (Instant generation, responsive UI, comprehensive features)

---

## 🛠️ Technologies Used

- **Frontend**: Streamlit with custom CSS (glassmorphism design)
- **Backend**: Python 3.13
- **Database**: SQLite3 with full CRUD operations
- **Story Generation**: Rule-based template engine with tier scaling
- **Authentication**: SHA-256 password hashing
- **Session Management**: Streamlit session state
- **Type Safety**: Type hints with Optional types

---

## 🚀 Future Enhancements

- [ ] Integrate real AI models (GPT-4, Claude, or Llama)
- [ ] Add story versioning and revision history
- [ ] Implement collaborative story writing
- [ ] Add export to PDF/EPUB formats
- [ ] Create mobile-responsive design
- [ ] Add story sharing and social features
- [ ] Implement advanced analytics dashboard
- [ ] Add story templates and genre-specific prompts

---

## 📄 License

This project is open source and available for portfolio use.

---

## 👨‍💻 Author

Built as a demonstration of full-stack development skills, clean code architecture, and production-ready patterns.

**Key Achievements:**
- ✅ Complete user authentication system
- ✅ Full CRUD database operations
- ✅ Smart algorithmic story generation
- ✅ Professional UI/UX design
- ✅ Comprehensive error handling
- ✅ Type-safe code throughout

Perfect for technical interviews and portfolio demonstrations!
5. **PostgreSQL** instead of SQLite for scalability
6. **Monitoring** (Sentry for errors, Datadog for performance)
7. **CI/CD pipeline** with automated testing
8. **Deploy on cloud** (AWS/GCP with auto-scaling)

---

## 🎬 **Interview Demo Script**

### Step 1: Prove Token Works
```powershell
python hf_test.py
```
*"This validates my HF token and shows I can integrate with their API."*

### Step 2: Show Code Architecture
Open `app.py` and walk through `generate_story()` function:
- Token handling (lines 12-15)
- Model fallback loop (lines 60-85)
- Local fallback (lines 38-46)

### Step 3: Live Demo
```powershell
streamlit run app.py
```
Generate a story, show terminal output with model attempts.

### Step 4: Explain Production Thinking
*"For production, I'd use HF Inference Endpoints with guaranteed uptime, add caching to reduce API costs, and implement comprehensive monitoring. The local fallback is great for demos but wouldn't scale—I'd use a secondary API provider instead."*

---

## 🤝 Contributing

Contributions welcome! Please submit a Pull Request.

## 📝 License

MIT License - Open source and free to use.

## 👤 Author

**Siddhant**
- GitHub: [@Siddhant-21-03](https://github.com/Siddhant-21-03)
- Project: Demonstrates production-ready API integration for technical interviews

## 🙏 Acknowledgments

- **Hugging Face** for free inference API and amazing models
- **Streamlit** for rapid UI development
- **EleutherAI** for GPT-Neo models
- **BigScience** for BLOOM multilingual model
