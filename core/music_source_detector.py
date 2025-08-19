"""
Music Source Detection System for Personal DJ

This module identifies and tracks music sources including:
- Navidrome streaming server
- Local file playback
- External streaming URLs
- Different media players (mpv, vlc, ffplay)
- System audio sources
"""

import os
import re
import urllib.parse
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MusicSource:
    """Information about a music source."""
    source_type: str  # "navidrome", "local_file", "stream_url", "unknown"
    source_name: str  # Human-readable name
    player: str  # "mpv", "vlc", "ffplay", etc.
    details: Dict[str, str]  # Additional metadata
    icon: str  # Emoji or icon for display


class MusicSourceDetector:
    """Detects and categorizes music sources."""
    
    def __init__(self, logger):
        self.logger = logger
        self.known_sources = {}
        self._load_source_patterns()
    
    def _load_source_patterns(self):
        """Load patterns for detecting different music sources."""
        self.source_patterns = {
            'navidrome': {
                'url_patterns': [
                    r'.*navidrome.*',
                    r'.*/rest/stream.*',
                    r'.*/api/stream.*',
                    r'.*:4533.*'  # Default Navidrome port
                ],
                'icon': '🎵',
                'name': 'Navidrome Server'
            },
            'spotify': {
                'url_patterns': [
                    r'.*spotify\.com.*',
                    r'.*open\.spotify\.com.*'
                ],
                'icon': '🎧',
                'name': 'Spotify'
            },
            'youtube': {
                'url_patterns': [
                    r'.*youtube\.com.*',
                    r'.*youtu\.be.*',
                    r'.*youtube-nocookie\.com.*'
                ],
                'icon': '📺',
                'name': 'YouTube'
            },
            'soundcloud': {
                'url_patterns': [
                    r'.*soundcloud\.com.*'
                ],
                'icon': '☁️',
                'name': 'SoundCloud'
            },
            'radio_stream': {
                'url_patterns': [
                    r'.*\.m3u8?$',
                    r'.*\.pls$',
                    r'.*radio.*',
                    r'.*stream.*'
                ],
                'icon': '📻',
                'name': 'Radio Stream'
            }
        }
        
        self.file_extensions = {
            'audio': ['.mp3', '.flac', '.wav', '.ogg', '.m4a', '.aac', '.wma', '.opus'],
            'playlist': ['.m3u', '.m3u8', '.pls', '.xspf']
        }
    
    def detect_source(self, track_path: str, player: str = "unknown") -> MusicSource:
        """Detect the source of a music track."""
        if not track_path:
            return MusicSource(
                source_type="unknown",
                source_name="Unknown Source",
                player=player,
                details={},
                icon="❓"
            )
        
        # Check if it's a URL
        if track_path.startswith(('http://', 'https://')):
            return self._detect_url_source(track_path, player)
        
        # Check if it's a local file
        if os.path.exists(track_path) or track_path.startswith(('/', 'C:', '\\', './')):
            return self._detect_local_source(track_path, player)
        
        # Fallback for unknown sources
        return MusicSource(
            source_type="unknown",
            source_name="Unknown Source",
            player=player,
            details={"path": track_path},
            icon="❓"
        )
    
    def _detect_url_source(self, url: str, player: str) -> MusicSource:
        """Detect source from URL."""
        parsed_url = urllib.parse.urlparse(url)
        hostname = parsed_url.hostname or ""
        
        # Check against known patterns
        for source_type, config in self.source_patterns.items():
            for pattern in config['url_patterns']:
                if re.match(pattern, url, re.IGNORECASE):
                    details = {
                        "url": url,
                        "hostname": hostname,
                        "port": str(parsed_url.port) if parsed_url.port else "default"
                    }
                    
                    # Special handling for Navidrome
                    if source_type == 'navidrome':
                        details.update(self._extract_navidrome_details(url))
                    
                    return MusicSource(
                        source_type=source_type,
                        source_name=config['name'],
                        player=player,
                        details=details,
                        icon=config['icon']
                    )
        
        # Generic streaming URL
        return MusicSource(
            source_type="stream_url",
            source_name=f"Stream ({hostname})",
            player=player,
            details={"url": url, "hostname": hostname},
            icon="🌐"
        )
    
    def _detect_local_source(self, file_path: str, player: str) -> MusicSource:
        """Detect source from local file path."""
        path_obj = Path(file_path)
        
        details = {
            "path": file_path,
            "filename": path_obj.name,
            "directory": str(path_obj.parent),
            "exists": str(path_obj.exists())
        }
        
        # Check file extension
        suffix = path_obj.suffix.lower()
        if suffix in self.file_extensions['audio']:
            details["file_type"] = "audio"
            icon = "🎵"
        elif suffix in self.file_extensions['playlist']:
            details["file_type"] = "playlist"
            icon = "📋"
        else:
            details["file_type"] = "unknown"
            icon = "📄"
        
        # Try to extract metadata from path
        source_name = self._guess_local_source_name(file_path)
        
        return MusicSource(
            source_type="local_file",
            source_name=source_name,
            player=player,
            details=details,
            icon=icon
        )
    
    def _extract_navidrome_details(self, url: str) -> Dict[str, str]:
        """Extract Navidrome-specific details from URL."""
        details = {}
        
        # Parse query parameters
        parsed = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed.query)
        
        # Common Navidrome parameters
        if 'id' in query_params:
            details['track_id'] = query_params['id'][0]
        if 'u' in query_params:
            details['username'] = query_params['u'][0]
        if 'c' in query_params:
            details['client'] = query_params['c'][0]
        
        # Detect API version
        if '/rest/' in url:
            details['api_version'] = 'Subsonic API'
        elif '/api/' in url:
            details['api_version'] = 'Native API'
        
        return details
    
    def _guess_local_source_name(self, file_path: str) -> str:
        """Guess a friendly name for local file source."""
        path_obj = Path(file_path)
        
        # Check for common music directory patterns
        parts = path_obj.parts
        
        # Look for music-related directory names
        music_indicators = ['music', 'audio', 'songs', 'tracks', 'library', 'collection']
        for i, part in enumerate(parts):
            if any(indicator in part.lower() for indicator in music_indicators):
                if i < len(parts) - 1:
                    return f"Local Music ({parts[i + 1]})"
        
        # Check if it's in user directories
        if 'Users' in parts or 'home' in parts:
            return "Personal Music Library"
        
        # Check for drive letters (Windows)
        if len(parts) > 0 and ':' in parts[0]:
            return f"Local Files ({parts[0]})"
        
        # Default
        return "Local File"
    
    def get_player_info(self, player_executable: str) -> Dict[str, str]:
        """Get information about the media player being used."""
        player_info = {
            'mpv': {
                'name': 'MPV Media Player',
                'icon': '🎬',
                'description': 'Free, open source, and cross-platform media player',
                'features': ['Hardware acceleration', 'Extensive format support', 'Command-line control']
            },
            'vlc': {
                'name': 'VLC Media Player',
                'icon': '🔶',
                'description': 'Free and open source cross-platform multimedia player',
                'features': ['Universal codec support', 'Streaming capabilities', 'Cross-platform']
            },
            'ffplay': {
                'name': 'FFplay',
                'icon': '⚡',
                'description': 'Simple media player using FFmpeg libraries',
                'features': ['Lightweight', 'Part of FFmpeg suite', 'Command-line based']
            },
            'windows_media_player': {
                'name': 'Windows Media Player',
                'icon': '🪟',
                'description': 'Built-in Windows media player',
                'features': ['Windows integration', 'Library management', 'Visualization']
            }
        }
        
        return player_info.get(player_executable, {
            'name': f'{player_executable.title()} Player',
            'icon': '🎵',
            'description': f'Media player: {player_executable}',
            'features': ['Audio playback']
        })
    
    def format_source_info(self, source: MusicSource, include_details: bool = False) -> str:
        """Format source information for display."""
        player_info = self.get_player_info(source.player)
        
        # Basic info
        info_parts = [
            f"{source.icon} {source.source_name}",
            f"via {player_info.get('icon', '🎵')} {player_info.get('name', source.player)}"
        ]
        
        if include_details and source.details:
            detail_parts = []
            
            if source.source_type == "navidrome":
                if 'hostname' in source.details:
                    detail_parts.append(f"Server: {source.details['hostname']}")
                if 'api_version' in source.details:
                    detail_parts.append(f"API: {source.details['api_version']}")
            
            elif source.source_type == "local_file":
                if 'directory' in source.details:
                    detail_parts.append(f"Location: {Path(source.details['directory']).name}")
                if 'file_type' in source.details:
                    detail_parts.append(f"Type: {source.details['file_type'].title()}")
            
            elif source.source_type == "stream_url":
                if 'hostname' in source.details:
                    detail_parts.append(f"Host: {source.details['hostname']}")
            
            if detail_parts:
                info_parts.append(f"({', '.join(detail_parts)})")
        
        return " ".join(info_parts)
    
    def get_source_statistics(self) -> Dict[str, int]:
        """Get statistics about music sources used."""
        return {
            source_type: len([s for s in self.known_sources.values() if s.source_type == source_type])
            for source_type in ['navidrome', 'local_file', 'stream_url', 'unknown']
        }
    
    def register_source(self, track_path: str, source: MusicSource):
        """Register a detected source for statistics."""
        self.known_sources[track_path] = source
        self.logger.info(f"Registered music source: {self.format_source_info(source)}")
