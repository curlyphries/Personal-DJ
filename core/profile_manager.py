"""
Profile Management CLI for Personal DJ

This module provides command-line tools for managing user profiles,
including creating, editing, importing, and exporting profiles.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

from core.user_profile import UserProfile


class ProfileManager:
    """Command-line interface for managing user profiles."""
    
    def __init__(self):
        self.current_profile = None
    
    def create_profile(self, name: str) -> bool:
        """Create a new user profile."""
        try:
            profile = UserProfile(name)
            
            print(f"\n🎵 Creating new Personal DJ profile: '{name}'")
            print("Let's personalize your DJ experience!\n")
            
            # DJ Personality Setup
            print("=== DJ Personality ===")
            dj_name = input(f"DJ Name (default: DJ Echo): ").strip() or "DJ Echo"
            profile.update_dj_personality("name", dj_name)
            
            print("\nChoose DJ Style:")
            print("1. Casual - Relaxed and friendly")
            print("2. Professional - Polished and smooth")
            print("3. Quirky - Fun and unpredictable")
            print("4. Mysterious - Cool and enigmatic")
            
            style_choice = input("Enter choice (1-4): ").strip()
            styles = {"1": "casual", "2": "professional", "3": "quirky", "4": "mysterious"}
            style = styles.get(style_choice, "casual")
            profile.update_dj_personality("style", style)
            
            print("\nChattiness Level:")
            print("1. Minimal - Brief introductions only")
            print("2. Moderate - Some commentary between songs")
            print("3. Chatty - Lots of interaction and stories")
            
            chat_choice = input("Enter choice (1-3): ").strip()
            chattiness = {"1": "minimal", "2": "moderate", "3": "chatty"}
            profile.update_dj_personality("chattiness", chattiness.get(chat_choice, "moderate"))
            
            # Music Preferences
            print("\n=== Music Preferences ===")
            
            print("Favorite genres (comma-separated, e.g., rock, jazz, electronic):")
            genres = input("> ").strip()
            if genres:
                genre_list = [g.strip() for g in genres.split(",")]
                profile.update_music_preference("favorite_genres", genre_list)
            
            print("\nPreferred energy levels (comma-separated: chill, moderate, high, intense):")
            energy = input("> ").strip()
            if energy:
                energy_list = [e.strip() for e in energy.split(",")]
                profile.update_music_preference("preferred_energy_levels", energy_list)
            
            print("\nFavorite decades (comma-separated, e.g., 80s, 90s, 2000s):")
            decades = input("> ").strip()
            if decades:
                decade_list = [d.strip() for d in decades.split(",")]
                profile.update_music_preference("favorite_decades", decade_list)
            
            # Personal Notes/Memories
            print("\n=== Personal Notes ===")
            print("Add some personal notes to help your DJ remember you better.")
            print("(Press Enter on empty line to finish)")
            
            while True:
                note = input("Add a note: ").strip()
                if not note:
                    break
                
                print("Category:")
                print("1. Music Memory (concerts, favorite songs, etc.)")
                print("2. Life Event (important moments)")
                print("3. Personal Preference (general likes/dislikes)")
                print("4. Other")
                
                cat_choice = input("Choose category (1-4): ").strip()
                categories = {"1": "music_memory", "2": "life_event", "3": "preference", "4": "personal_note"}
                category = categories.get(cat_choice, "personal_note")
                
                importance = input("Importance (1-5, 5 being most important): ").strip()
                try:
                    importance = int(importance)
                    importance = max(1, min(5, importance))
                except:
                    importance = 3
                
                profile.add_memory(note, category, importance)
                print("✓ Note added!\n")
            
            profile.save_profile()
            print(f"\n🎉 Profile '{name}' created successfully!")
            print(f"Your DJ {dj_name} is ready to spin some tunes!")
            
            return True
            
        except Exception as e:
            print(f"Error creating profile: {e}")
            return False
    
    def list_profiles(self):
        """List all available profiles."""
        profiles = UserProfile.list_profiles()
        
        if not profiles:
            print("No profiles found. Create one with: python -m core.profile_manager create <name>")
            return
        
        print("\n🎵 Available Personal DJ Profiles:")
        print("=" * 40)
        
        for profile_name in profiles:
            try:
                profile = UserProfile(profile_name)
                summary = profile.get_profile_summary()
                
                print(f"\n📀 {summary['name']}")
                print(f"   DJ: {summary['dj_name']} ({summary['dj_style']})")
                print(f"   Genres: {', '.join(summary['favorite_genres'][:3]) if summary['favorite_genres'] else 'Not set'}")
                print(f"   Memories: {summary['total_memories']}")
                print(f"   Sessions: {summary['total_sessions']}")
                print(f"   Last Updated: {summary['last_updated'][:10]}")
                
            except Exception as e:
                print(f"\n❌ {profile_name} (Error loading: {e})")
    
    def export_profile(self, profile_name: str, export_path: str = None):
        """Export a profile for sharing."""
        try:
            profile = UserProfile(profile_name)
            
            if not export_path:
                export_path = f"{profile_name}_personal_dj_profile.json"
            
            if profile.export_profile(export_path):
                print(f"✅ Profile '{profile_name}' exported to: {export_path}")
                print("\n📤 Share this file with family and friends!")
                print("They can import it with: python -m core.profile_manager import <file>")
            else:
                print(f"❌ Failed to export profile '{profile_name}'")
                
        except Exception as e:
            print(f"Error exporting profile: {e}")
    
    def import_profile(self, import_path: str, new_name: str = None, merge: bool = False):
        """Import a profile from file."""
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                print(f"❌ File not found: {import_path}")
                return
            
            # Load the file to get the profile name
            with open(import_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            original_name = data.get("profile_name", "imported_profile")
            profile_name = new_name or original_name
            
            # Check if profile already exists
            existing_profiles = UserProfile.list_profiles()
            if profile_name in existing_profiles and not merge:
                overwrite = input(f"Profile '{profile_name}' already exists. Overwrite? (y/N): ").strip().lower()
                if overwrite != 'y':
                    print("Import cancelled.")
                    return
            
            profile = UserProfile(profile_name)
            
            if profile.import_profile(import_path, merge):
                action = "merged with" if merge else "imported as"
                print(f"✅ Profile successfully {action} '{profile_name}'")
                
                # Show summary
                summary = profile.get_profile_summary()
                print(f"\n📀 Profile Summary:")
                print(f"   DJ: {summary['dj_name']} ({summary['dj_style']})")
                print(f"   Memories: {summary['total_memories']}")
                print(f"   Favorite Genres: {', '.join(summary['favorite_genres'][:5]) if summary['favorite_genres'] else 'None set'}")
            else:
                print(f"❌ Failed to import profile")
                
        except Exception as e:
            print(f"Error importing profile: {e}")
    
    def edit_profile(self, profile_name: str):
        """Interactive profile editing."""
        try:
            profile = UserProfile(profile_name)
            
            while True:
                print(f"\n🎵 Editing Profile: {profile_name}")
                print("=" * 40)
                print("1. Update DJ Personality")
                print("2. Update Music Preferences")
                print("3. Add Memory/Note")
                print("4. View Memories")
                print("5. Delete Memory")
                print("6. View Profile Summary")
                print("7. Save and Exit")
                
                choice = input("\nChoose option (1-7): ").strip()
                
                if choice == "1":
                    self._edit_dj_personality(profile)
                elif choice == "2":
                    self._edit_music_preferences(profile)
                elif choice == "3":
                    self._add_memory(profile)
                elif choice == "4":
                    self._view_memories(profile)
                elif choice == "5":
                    self._delete_memory(profile)
                elif choice == "6":
                    self._show_profile_summary(profile)
                elif choice == "7":
                    profile.save_profile()
                    print("✅ Profile saved!")
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
        except Exception as e:
            print(f"Error editing profile: {e}")
    
    def _edit_dj_personality(self, profile: UserProfile):
        """Edit DJ personality settings."""
        print("\n=== DJ Personality ===")
        current = profile.dj_personality
        
        print(f"Current DJ Name: {current.name}")
        new_name = input("New DJ Name (press Enter to keep current): ").strip()
        if new_name:
            profile.update_dj_personality("name", new_name)
        
        print(f"\nCurrent Style: {current.style}")
        print("Styles: casual, professional, quirky, mysterious")
        new_style = input("New Style (press Enter to keep current): ").strip()
        if new_style in ["casual", "professional", "quirky", "mysterious"]:
            profile.update_dj_personality("style", new_style)
        
        print(f"\nCurrent Chattiness: {current.chattiness}")
        print("Levels: minimal, moderate, chatty")
        new_chat = input("New Chattiness (press Enter to keep current): ").strip()
        if new_chat in ["minimal", "moderate", "chatty"]:
            profile.update_dj_personality("chattiness", new_chat)
    
    def _edit_music_preferences(self, profile: UserProfile):
        """Edit music preferences."""
        print("\n=== Music Preferences ===")
        prefs = profile.music_preferences
        
        print(f"Current Favorite Genres: {', '.join(prefs.favorite_genres)}")
        new_genres = input("New Favorite Genres (comma-separated, or press Enter to keep): ").strip()
        if new_genres:
            genre_list = [g.strip() for g in new_genres.split(",")]
            profile.update_music_preference("favorite_genres", genre_list)
        
        print(f"\nCurrent Energy Levels: {', '.join(prefs.preferred_energy_levels)}")
        new_energy = input("New Energy Levels (comma-separated, or press Enter to keep): ").strip()
        if new_energy:
            energy_list = [e.strip() for e in new_energy.split(",")]
            profile.update_music_preference("preferred_energy_levels", energy_list)
    
    def _add_memory(self, profile: UserProfile):
        """Add a new memory to the profile."""
        print("\n=== Add Memory ===")
        content = input("Memory/Note: ").strip()
        if not content:
            return
        
        print("Categories: music_memory, life_event, preference, personal_note")
        category = input("Category: ").strip() or "personal_note"
        
        try:
            importance = int(input("Importance (1-5): ").strip() or "3")
            importance = max(1, min(5, importance))
        except:
            importance = 3
        
        tags = input("Tags (comma-separated, optional): ").strip()
        tag_list = [t.strip() for t in tags.split(",")] if tags else []
        
        memory_id = profile.add_memory(content, category, importance, tag_list)
        print(f"✅ Memory added with ID: {memory_id}")
    
    def _view_memories(self, profile: UserProfile):
        """View all memories in the profile."""
        print("\n=== Memories ===")
        
        if not profile.memories:
            print("No memories found.")
            return
        
        for i, memory in enumerate(profile.memories, 1):
            print(f"\n{i}. [{memory.category}] Importance: {memory.importance}/5")
            print(f"   {memory.content}")
            if memory.tags:
                print(f"   Tags: {', '.join(memory.tags)}")
            print(f"   Created: {memory.created_date[:10]}")
    
    def _delete_memory(self, profile: UserProfile):
        """Delete a memory from the profile."""
        if not profile.memories:
            print("No memories to delete.")
            return
        
        self._view_memories(profile)
        
        try:
            index = int(input("\nEnter memory number to delete (0 to cancel): ")) - 1
            if index == -1:
                return
            
            if 0 <= index < len(profile.memories):
                deleted = profile.memories.pop(index)
                print(f"✅ Deleted memory: {deleted.content[:50]}...")
            else:
                print("Invalid memory number.")
        except ValueError:
            print("Invalid input.")
    
    def _show_profile_summary(self, profile: UserProfile):
        """Show profile summary."""
        summary = profile.get_profile_summary()
        
        print(f"\n📀 Profile Summary: {summary['name']}")
        print("=" * 40)
        print(f"DJ Name: {summary['dj_name']}")
        print(f"DJ Style: {summary['dj_style']}")
        print(f"Favorite Genres: {', '.join(summary['favorite_genres']) if summary['favorite_genres'] else 'None set'}")
        print(f"Total Memories: {summary['total_memories']}")
        print(f"Total Sessions: {summary['total_sessions']}")
        print(f"Created: {summary['created'][:10]}")
        print(f"Last Updated: {summary['last_updated'][:10]}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Personal DJ Profile Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create profile
    create_parser = subparsers.add_parser("create", help="Create a new profile")
    create_parser.add_argument("name", help="Profile name")
    
    # List profiles
    list_parser = subparsers.add_parser("list", help="List all profiles")
    
    # Export profile
    export_parser = subparsers.add_parser("export", help="Export a profile")
    export_parser.add_argument("name", help="Profile name to export")
    export_parser.add_argument("--output", "-o", help="Output file path")
    
    # Import profile
    import_parser = subparsers.add_parser("import", help="Import a profile")
    import_parser.add_argument("file", help="Profile file to import")
    import_parser.add_argument("--name", "-n", help="New profile name")
    import_parser.add_argument("--merge", "-m", action="store_true", help="Merge with existing profile")
    
    # Edit profile
    edit_parser = subparsers.add_parser("edit", help="Edit a profile")
    edit_parser.add_argument("name", help="Profile name to edit")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = ProfileManager()
    
    if args.command == "create":
        manager.create_profile(args.name)
    elif args.command == "list":
        manager.list_profiles()
    elif args.command == "export":
        manager.export_profile(args.name, args.output)
    elif args.command == "import":
        manager.import_profile(args.file, args.name, args.merge)
    elif args.command == "edit":
        manager.edit_profile(args.name)


if __name__ == "__main__":
    main()
