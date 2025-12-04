"""Database models and operations for the Story Generator"""
import sqlite3
from datetime import datetime
from typing import List, Optional, Dict
import json

class Database:
    def __init__(self, db_name: str = "stories.db"):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                display_name TEXT,
                photo_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Stories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stories (
                story_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                prompt TEXT NOT NULL,
                content TEXT NOT NULL,
                genre TEXT,
                creativity REAL,
                word_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_favorite BOOLEAN DEFAULT 0,
                tags TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Create indexes for faster queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_stories ON stories(user_id, created_at DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_story_genre ON stories(genre)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_story_favorite ON stories(user_id, is_favorite)')
        
        conn.commit()
        conn.close()
    
    # User operations
    def create_or_update_user(self, user_id: str, email: str, display_name: str | None = None, photo_url: str | None = None):
        """Create or update user in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (user_id, email, display_name, photo_url, last_login)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                email = excluded.email,
                display_name = excluded.display_name,
                photo_url = excluded.photo_url,
                last_login = CURRENT_TIMESTAMP
        ''', (user_id, email, display_name, photo_url))
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    # Story operations
    def save_story(self, user_id: str, title: str, prompt: str, content: str, 
                   genre: Optional[str] = None, creativity: float = 0.7, tags: Optional[List[str]] = None) -> int:
        """Save a new story"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        word_count = len(content.split())
        tags_json = json.dumps(tags) if tags else None
        
        cursor.execute('''
            INSERT INTO stories (user_id, title, prompt, content, genre, creativity, word_count, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, title, prompt, content, genre, creativity, word_count, tags_json))
        
        story_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return story_id if story_id else 0
    
    def get_user_stories(self, user_id: str, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Get all stories for a user with pagination"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM stories 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
        ''', (user_id, limit, offset))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_story(self, story_id: int, user_id: str) -> Optional[Dict]:
        """Get a specific story"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM stories 
            WHERE story_id = ? AND user_id = ?
        ''', (story_id, user_id))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def update_story(self, story_id: int, user_id: str, title: Optional[str] = None, 
                     content: Optional[str] = None, genre: Optional[str] = None, tags: Optional[List[str]] = None):
        """Update an existing story"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if content is not None:
            updates.append("content = ?")
            params.append(content)
            updates.append("word_count = ?")
            params.append(len(content.split()))
        if genre is not None:
            updates.append("genre = ?")
            params.append(genre)
        if tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(tags))
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.extend([story_id, user_id])
            
            query = f"UPDATE stories SET {', '.join(updates)} WHERE story_id = ? AND user_id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def delete_story(self, story_id: int, user_id: str):
        """Delete a story"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM stories WHERE story_id = ? AND user_id = ?', (story_id, user_id))
        conn.commit()
        conn.close()
    
    def toggle_favorite(self, story_id: int, user_id: str):
        """Toggle favorite status of a story"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE stories 
            SET is_favorite = NOT is_favorite 
            WHERE story_id = ? AND user_id = ?
        ''', (story_id, user_id))
        
        conn.commit()
        conn.close()
    
    def search_stories(self, user_id: str, query: str, genre: Optional[str] = None, 
                       favorite_only: bool = False, limit: int = 50) -> List[Dict]:
        """Search stories by title or content with filters"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        sql = '''
            SELECT * FROM stories 
            WHERE user_id = ? 
            AND (title LIKE ? OR content LIKE ? OR prompt LIKE ?)
        '''
        params: List = [user_id, f'%{query}%', f'%{query}%', f'%{query}%']
        
        if genre:
            sql += ' AND genre = ?'
            params.append(genre)
        
        if favorite_only:
            sql += ' AND is_favorite = 1'
        
        sql += ' ORDER BY created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_stats(self, user_id: str) -> Dict:
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_stories,
                SUM(word_count) as total_words,
                COUNT(CASE WHEN is_favorite = 1 THEN 1 END) as favorite_count,
                COUNT(DISTINCT genre) as genre_count
            FROM stories 
            WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        
        cursor.execute('''
            SELECT genre, COUNT(*) as count 
            FROM stories 
            WHERE user_id = ? AND genre IS NOT NULL
            GROUP BY genre 
            ORDER BY count DESC
        ''', (user_id,))
        
        genre_stats = cursor.fetchall()
        conn.close()
        
        return {
            **dict(row),
            'genres': [dict(g) for g in genre_stats]
        }
