"""
User Profile Management System for Personal DJ

This module handles user profiles that contain:
- Personal preferences (music genres, moods, energy levels)
- Interaction history and learned behaviors
- Personal memories and notes
- DJ personality customizations
- Exportable/importable profile data
"""

import json
import os
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class MusicPreferences:
    """User's music preferences and taste profile."""
    favorite_genres: List[str]
    disliked_genres: List[str]
    preferred_energy_levels: List[str]  # ["chill", "moderate", "high", "intense"]
    favorite_decades: List[str]
    preferred_moods: List[str]  # ["happy", "melancholy", "energetic", "romantic", etc.]
    volume_preference: float  # 0.0 to 1.0
    skip_explicit: bool
    preferred_languages: List[str]


@dataclass
class DJPersonality:
    """Customizable DJ personality traits."""
    name: str  # DJ name (e.g., "DJ Echo", "DJ Midnight")
    style: str  # "casual", "professional", "quirky", "mysterious"
    chattiness: str  # "minimal", "moderate", "chatty"
    humor_level: str  # "none", "light", "heavy"
    voice_tone: str  # "friendly", "cool", "energetic", "smooth"
    catchphrases: List[str]
    introduction_style: str


@dataclass
class UserMemory:
    """Individual memory/note about the user."""
    id: str
    content: str
    category: str  # "preference", "life_event", "music_memory", "personal_note"
    importance: int  # 1-5 scale
    created_date: str
    last_referenced: str
    tags: List[str]


@dataclass
class InteractionHistory:
    """Track user interactions and learned behaviors."""
    total_sessions: int
    favorite_request_types: List[str]
    common_times_of_use: List[str]  # ["morning", "afternoon", "evening", "late_night"]
    session_durations: List[float]  # in minutes
    most_played_tracks: List[Dict[str, Any]]
    skip_patterns: List[Dict[str, Any]]
    positive_feedback_keywords: List[str]
    negative_feedback_keywords: List[str]


class UserProfile:
    """Complete user profile management."""
    
    def __init__(self, profile_name: str = "default"):
        self.profile_name = profile_name
        self.profile_dir = Path("profiles")
        self.profile_file = self.profile_dir / f"{profile_name}.json"
        
        # Initialize default profile data
        self.music_preferences = MusicPreferences(
            favorite_genres=[],
            disliked_genres=[],
            preferred_energy_levels=["moderate"],
            favorite_decades=[],
            preferred_moods=[],
            volume_preference=0.7,
            skip_explicit=False,
            preferred_languages=["English"]
        )
        
        self.dj_personality = DJPersonality(
            name="DJ Echo",
            style="casual",
            chattiness="moderate",
            humor_level="light",
            voice_tone="friendly",
            catchphrases=[],
            introduction_style="Welcome back! Ready for some great music?"
        )
        
        self.memories: List[UserMemory] = []
        self.interaction_history = InteractionHistory(
            total_sessions=0,
            favorite_request_types=[],
            common_times_of_use=[],
            session_durations=[],
            most_played_tracks=[],
            skip_patterns=[],
            positive_feedback_keywords=[],
            negative_feedback_keywords=[]
        )
        
        self.created_date = datetime.datetime.now().isoformat()
        self.last_updated = datetime.datetime.now().isoformat()
        self.version = "1.0"
        
        # Load existing profile if it exists
        self.load_profile()
    
    def add_memory(self, content: str, category: str = "personal_note", 
                   importance: int = 3, tags: List[str] = None) -> str:
        """Add a new memory/note about the user."""
        if tags is None:
            tags = []
        
        memory_id = f"mem_{len(self.memories)}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        memory = UserMemory(
            id=memory_id,
            content=content,
            category=category,
            importance=importance,
            created_date=datetime.datetime.now().isoformat(),
            last_referenced=datetime.datetime.now().isoformat(),
            tags=tags
        )
        
        self.memories.append(memory)
        self.last_updated = datetime.datetime.now().isoformat()
        return memory_id
    
    def get_memories_by_category(self, category: str) -> List[UserMemory]:
        """Retrieve memories by category."""
        return [mem for mem in self.memories if mem.category == category]
    
    def get_memories_by_importance(self, min_importance: int = 3) -> List[UserMemory]:
        """Get memories above a certain importance level."""
        return [mem for mem in self.memories if mem.importance >= min_importance]
    
    def search_memories(self, query: str) -> List[UserMemory]:
        """Search memories by content or tags."""
        query_lower = query.lower()
        results = []
        
        for memory in self.memories:
            if (query_lower in memory.content.lower() or 
                any(query_lower in tag.lower() for tag in memory.tags)):
                memory.last_referenced = datetime.datetime.now().isoformat()
                results.append(memory)
        
        return results
    
    def update_music_preference(self, preference_type: str, value: Any):
        """Update a specific music preference."""
        if hasattr(self.music_preferences, preference_type):
            setattr(self.music_preferences, preference_type, value)
            self.last_updated = datetime.datetime.now().isoformat()
    
    def update_dj_personality(self, trait: str, value: Any):
        """Update DJ personality trait."""
        if hasattr(self.dj_personality, trait):
            setattr(self.dj_personality, trait, value)
            self.last_updated = datetime.datetime.now().isoformat()
    
    def record_interaction(self, interaction_type: str, data: Dict[str, Any]):
        """Record user interaction for learning."""
        self.interaction_history.total_sessions += 1
        
        # Update interaction patterns based on type
        if interaction_type == "track_played":
            self.interaction_history.most_played_tracks.append(data)
        elif interaction_type == "track_skipped":
            self.interaction_history.skip_patterns.append(data)
        elif interaction_type == "positive_feedback":
            if "keywords" in data:
                self.interaction_history.positive_feedback_keywords.extend(data["keywords"])
        elif interaction_type == "negative_feedback":
            if "keywords" in data:
                self.interaction_history.negative_feedback_keywords.extend(data["keywords"])
        
        self.last_updated = datetime.datetime.now().isoformat()
    
    def get_personalized_prompt_context(self) -> str:
        """Generate context for DJ prompts based on user profile."""
        context_parts = []
        
        # Add DJ personality
        context_parts.append(f"You are {self.dj_personality.name}, a {self.dj_personality.style} DJ with a {self.dj_personality.voice_tone} tone.")
        
        # Add music preferences
        if self.music_preferences.favorite_genres:
            context_parts.append(f"The user loves: {', '.join(self.music_preferences.favorite_genres)}.")
        
        if self.music_preferences.disliked_genres:
            context_parts.append(f"The user dislikes: {', '.join(self.music_preferences.disliked_genres)}.")
        
        # Add important memories
        important_memories = self.get_memories_by_importance(4)
        if important_memories:
            memory_texts = [mem.content for mem in important_memories[:3]]  # Top 3 most important
            context_parts.append(f"Remember these important things about the user: {'; '.join(memory_texts)}.")
        
        # Add interaction patterns
        if self.interaction_history.positive_feedback_keywords:
            recent_positive = list(set(self.interaction_history.positive_feedback_keywords[-10:]))
            context_parts.append(f"The user responds positively to: {', '.join(recent_positive)}.")
        
        return " ".join(context_parts)
    
    def save_profile(self):
        """Save profile to JSON file."""
        self.profile_dir.mkdir(exist_ok=True)
        
        profile_data = {
            "profile_name": self.profile_name,
            "music_preferences": asdict(self.music_preferences),
            "dj_personality": asdict(self.dj_personality),
            "memories": [asdict(mem) for mem in self.memories],
            "interaction_history": asdict(self.interaction_history),
            "created_date": self.created_date,
            "last_updated": self.last_updated,
            "version": self.version
        }
        
        with open(self.profile_file, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=2, ensure_ascii=False)
    
    def load_profile(self):
        """Load profile from JSON file."""
        if not self.profile_file.exists():
            return
        
        try:
            with open(self.profile_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.profile_name = data.get("profile_name", self.profile_name)
            self.created_date = data.get("created_date", self.created_date)
            self.last_updated = data.get("last_updated", self.last_updated)
            self.version = data.get("version", self.version)
            
            # Load music preferences
            if "music_preferences" in data:
                self.music_preferences = MusicPreferences(**data["music_preferences"])
            
            # Load DJ personality
            if "dj_personality" in data:
                self.dj_personality = DJPersonality(**data["dj_personality"])
            
            # Load memories
            if "memories" in data:
                self.memories = [UserMemory(**mem_data) for mem_data in data["memories"]]
            
            # Load interaction history
            if "interaction_history" in data:
                self.interaction_history = InteractionHistory(**data["interaction_history"])
                
        except Exception as e:
            print(f"Error loading profile: {e}")
    
    def export_profile(self, export_path: str) -> bool:
        """Export profile to a shareable file."""
        try:
            export_data = {
                "profile_name": self.profile_name,
                "music_preferences": asdict(self.music_preferences),
                "dj_personality": asdict(self.dj_personality),
                "memories": [asdict(mem) for mem in self.memories],
                "created_date": self.created_date,
                "last_updated": self.last_updated,
                "version": self.version,
                "export_date": datetime.datetime.now().isoformat(),
                "export_note": "Personal DJ Profile - Import this file to restore your personalized DJ experience"
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exporting profile: {e}")
            return False
    
    def import_profile(self, import_path: str, merge: bool = False) -> bool:
        """Import profile from a file."""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not merge:
                # Complete replacement
                self.profile_name = data.get("profile_name", self.profile_name)
                self.music_preferences = MusicPreferences(**data["music_preferences"])
                self.dj_personality = DJPersonality(**data["dj_personality"])
                self.memories = [UserMemory(**mem_data) for mem_data in data["memories"]]
                self.created_date = data.get("created_date", self.created_date)
            else:
                # Merge mode - combine memories and preferences
                imported_memories = [UserMemory(**mem_data) for mem_data in data["memories"]]
                existing_contents = {mem.content for mem in self.memories}
                
                for mem in imported_memories:
                    if mem.content not in existing_contents:
                        self.memories.append(mem)
                
                # Merge preferences (imported ones take priority)
                imported_prefs = MusicPreferences(**data["music_preferences"])
                self.music_preferences.favorite_genres = list(set(
                    self.music_preferences.favorite_genres + imported_prefs.favorite_genres
                ))
                self.music_preferences.disliked_genres = list(set(
                    self.music_preferences.disliked_genres + imported_prefs.disliked_genres
                ))
            
            self.last_updated = datetime.datetime.now().isoformat()
            self.save_profile()
            return True
            
        except Exception as e:
            print(f"Error importing profile: {e}")
            return False
    
    @classmethod
    def list_profiles(cls) -> List[str]:
        """List all available profiles."""
        profile_dir = Path("profiles")
        if not profile_dir.exists():
            return []
        
        return [f.stem for f in profile_dir.glob("*.json")]
    
    def get_profile_summary(self) -> Dict[str, Any]:
        """Get a summary of the profile for display."""
        return {
            "name": self.profile_name,
            "dj_name": self.dj_personality.name,
            "dj_style": self.dj_personality.style,
            "favorite_genres": self.music_preferences.favorite_genres,
            "total_memories": len(self.memories),
            "total_sessions": self.interaction_history.total_sessions,
            "created": self.created_date,
            "last_updated": self.last_updated
        }
