# AI Story Generator

A story generation app built with Streamlit. Users can sign up, generate stories with customizable genre and word count, and manage their library.

## Features

- **Story Generation**: Rule-based template system that generates stories from 100-800 words
- **Genres**: Fantasy, Sci-Fi, Mystery, Romance, Horror, Adventure, Comedy, Drama, Thriller
- **User Authentication**: Sign up and login with secure password hashing
- **Story Library**: Save, search, edit, organize stories
- **Word Count Control**: Specify exact length with accurate scaling

## Tech Stack

- Python 3.13
- Streamlit (UI)
- SQLite (Database)
- SHA-256 (Password hashing)

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

App runs at `http://localhost:8501`

## How It Works

The story generator uses a 5-tier template system based on target word count:

| Target | Sentences | Avg Length | Notes |
|--------|-----------|------------|-------|
| <150   | 5         | 20-25 words | Short stories |
| <250   | 8         | 25-30 words | Brief narratives |
| <400   | 11        | 30-35 words | Medium length |
| <600   | 14        | 35-42 words | Longer stories |
| 600+   | 17        | 45-50 words | Extended narratives |

Each sentence is carefully crafted to stay within the tier's constraints.

## Project Structure

```
├── app.py                 Main UI
├── huggingface_client.py  Story generation
├── database.py            SQLite operations
├── auth.py                Authentication
├── history.py             Story library UI
├── requirements.txt       Dependencies
└── stories.db             Database (auto-created)
```

## Usage

1. Sign up with email and password
2. Generate a story: Enter prompt, select genre, set word count
3. View all stories in "My Library"
4. Edit, delete, or download stories

## Database

Two main tables:

**users**
- user_id (primary key)
- email, password_hash, display_name
- created_at, last_login

**stories**
- story_id (primary key)
- user_id (foreign key)
- title, prompt, content
- genre, word_count
- created_at, updated_at
- is_favorite, tags (JSON)

## Key Implementation Details

### Word Count Accuracy
The biggest challenge was scaling word counts accurately. Initial versions were too short because sentences averaged ~20 words. The solution was to:
1. Calculate words per sentence for each tier
2. Create templates with appropriate sentence complexity
3. Test across all ranges to validate accuracy

### Authentication
Uses SHA-256 password hashing stored in SQLite. Session state manages login persistence. All queries are scoped to the authenticated user.

### Database Design
Normalized schema with proper foreign keys and indexes. Parameterized queries prevent SQL injection. Tags stored as JSON for flexibility.

## Future Work

- Real AI models (GPT-4, Claude, Llama)
- Story versioning
- PDF/EPUB export
- User collaboration
- Advanced analytics

## License

Open source.
