"""Story history and management UI"""
import streamlit as st
from database import Database
from datetime import datetime
import json

def parse_tags(tags_json):
    """Parse tags from JSON string"""
    if tags_json:
        try:
            return json.loads(tags_json)
        except:
            return []
    return []

def show_story_card(story, db, on_edit_callback=None):
    """Display a story card with actions"""
    with st.container():
        col1, col2 = st.columns([5, 1])
        
        with col1:
            st.markdown(f"### {story['title']}")
            created = datetime.fromisoformat(story['created_at']).strftime("%B %d, %Y at %I:%M %p")
            genre_badge = f"🏷️ {story['genre']}" if story['genre'] else ""
            st.caption(f"📅 {created} | 📝 {story['word_count']} words | {genre_badge}")
        
        with col2:
            is_fav = story['is_favorite']
            if st.button("⭐" if is_fav else "☆", key=f"fav_{story['story_id']}", help="Toggle favorite"):
                db.toggle_favorite(story['story_id'], story['user_id'])
                st.rerun()
        
        # Show preview
        preview = story['content'][:200] + "..." if len(story['content']) > 200 else story['content']
        st.markdown(preview)
        
        # Tags
        tags = parse_tags(story.get('tags'))
        if tags:
            st.markdown(" ".join([f"`{tag}`" for tag in tags]))
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("👁️ View Full", key=f"view_{story['story_id']}"):
                st.session_state['viewing_story'] = story['story_id']
        
        with col2:
            if st.button("✏️ Edit", key=f"edit_{story['story_id']}"):
                st.session_state['editing_story'] = story['story_id']
                if on_edit_callback:
                    on_edit_callback(story)
        
        with col3:
            if st.button("💾 Download", key=f"download_{story['story_id']}"):
                st.download_button(
                    label="Download as Markdown",
                    data=story['content'],
                    file_name=f"{story['title'].replace(' ', '_')}.md",
                    mime="text/markdown",
                    key=f"dl_btn_{story['story_id']}"
                )
        
        with col4:
            if st.button("🗑️ Delete", key=f"delete_{story['story_id']}", type="secondary"):
                st.session_state['deleting_story'] = story['story_id']
        
        st.divider()


def show_story_detail(story, db):
    """Show full story detail"""
    st.markdown(f"# {story['title']}")
    
    created = datetime.fromisoformat(story['created_at']).strftime("%B %d, %Y at %I:%M %p")
    updated = datetime.fromisoformat(story['updated_at']).strftime("%B %d, %Y at %I:%M %p")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Word Count", story['word_count'])
    with col2:
        st.metric("Creativity", f"{story['creativity']:.1f}")
    with col3:
        st.metric("Genre", story['genre'] or "N/A")
    
    st.caption(f"📅 Created: {created}")
    if created != updated:
        st.caption(f"🔄 Updated: {updated}")
    
    st.markdown("---")
    st.markdown("### Original Prompt")
    st.info(story['prompt'])
    
    st.markdown("### Story")
    st.markdown(story['content'])
    
    # Tags
    tags = parse_tags(story.get('tags'))
    if tags:
        st.markdown("### Tags")
        st.markdown(" ".join([f"`{tag}`" for tag in tags]))
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬅️ Back to Library", type="primary"):
            if 'viewing_story' in st.session_state:
                del st.session_state['viewing_story']
            st.rerun()
    
    with col2:
        st.download_button(
            "💾 Download",
            data=story['content'],
            file_name=f"{story['title'].replace(' ', '_')}.md",
            mime="text/markdown"
        )
    
    with col3:
        if st.button("✏️ Edit"):
            st.session_state['editing_story'] = story['story_id']
            if 'viewing_story' in st.session_state:
                del st.session_state['viewing_story']
            st.rerun()


def show_edit_form(story, db, user_id):
    """Show edit form for a story"""
    st.markdown(f"## ✏️ Editing: {story['title']}")
    
    with st.form("edit_story_form"):
        new_title = st.text_input("Title", value=story['title'])
        new_genre = st.selectbox(
            "Genre",
            ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Adventure", "Comedy", "Drama", "Thriller"],
            index=["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Adventure", "Comedy", "Drama", "Thriller"].index(story['genre']) if story['genre'] in ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Adventure", "Comedy", "Drama", "Thriller"] else 0
        )
        new_content = st.text_area("Content", value=story['content'], height=400)
        
        tags = parse_tags(story.get('tags'))
        new_tags_str = st.text_input("Tags (comma-separated)", value=", ".join(tags))
        
        col1, col2 = st.columns(2)
        
        with col1:
            save = st.form_submit_button("💾 Save Changes", type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Cancel")
        
        if save:
            new_tags = [tag.strip() for tag in new_tags_str.split(",") if tag.strip()]
            db.update_story(
                story['story_id'],
                user_id,
                title=new_title,
                content=new_content,
                genre=new_genre,
                tags=new_tags
            )
            st.success("Story updated successfully!")
            if 'editing_story' in st.session_state:
                del st.session_state['editing_story']
            st.rerun()
        
        if cancel:
            if 'editing_story' in st.session_state:
                del st.session_state['editing_story']
            st.rerun()


def show_history_page(user_id):
    """Display story history page with search and filters"""
    db = Database()
    
    st.title("📚 My Story Library")
    
    # Get stats
    stats = db.get_stats(user_id)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Stories", stats['total_stories'])
    with col2:
        st.metric("Total Words", f"{stats['total_words']:,}")
    with col3:
        st.metric("Favorites", stats['favorite_count'])
    with col4:
        st.metric("Genres", stats['genre_count'])
    
    st.divider()
    
    # Check if viewing a specific story
    if 'viewing_story' in st.session_state:
        story = db.get_story(st.session_state['viewing_story'], user_id)
        if story:
            show_story_detail(story, db)
            return
    
    # Check if editing a story
    if 'editing_story' in st.session_state:
        story = db.get_story(st.session_state['editing_story'], user_id)
        if story:
            show_edit_form(story, db, user_id)
            return
    
    # Check if deleting a story
    if 'deleting_story' in st.session_state:
        st.warning("Are you sure you want to delete this story?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Delete", type="primary"):
                db.delete_story(st.session_state['deleting_story'], user_id)
                del st.session_state['deleting_story']
                st.success("Story deleted!")
                st.rerun()
        with col2:
            if st.button("❌ Cancel"):
                del st.session_state['deleting_story']
                st.rerun()
        return
    
    # Search and filters
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search stories", placeholder="Search by title, content, or prompt...")
    
    with col2:
        genre_filter = st.selectbox(
            "Genre",
            ["All"] + ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Adventure", "Comedy", "Drama", "Thriller"]
        )
    
    with col3:
        show_favorites = st.checkbox("⭐ Favorites Only")
    
    # Get stories
    if search_query:
        genre = None if genre_filter == "All" else genre_filter
        stories = db.search_stories(user_id, search_query, genre=genre, favorite_only=show_favorites)
    else:
        stories = db.get_user_stories(user_id)
        
        # Apply filters
        if genre_filter != "All":
            stories = [s for s in stories if s['genre'] == genre_filter]
        if show_favorites:
            stories = [s for s in stories if s['is_favorite']]
    
    # Display stories
    if stories:
        st.markdown(f"### Found {len(stories)} {'story' if len(stories) == 1 else 'stories'}")
        
        for story in stories:
            show_story_card(story, db)
    else:
        st.info("No stories found. Generate your first story to get started!")
    
    # Genre breakdown
    if stats['genres']:
        st.markdown("### 📊 Your Genre Breakdown")
        genre_cols = st.columns(min(len(stats['genres']), 5))
        for idx, genre_stat in enumerate(stats['genres'][:5]):
            with genre_cols[idx]:
                st.metric(genre_stat['genre'], genre_stat['count'])
