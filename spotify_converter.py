#!/usr/bin/env python3
"""
Enhanced Spotify to YouTube Playlist Converter
Converts Spotify playlist export to YouTube search terms for yt-dlp
"""

import csv
import re
import sys
import json
import os
import subprocess
import argparse
from pathlib import Path
from urllib.parse import quote

def check_and_install_dependencies():
    """Check and install missing dependencies"""
    print("Checking dependencies...")
    
    # Check for yt-dlp
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        print("✓ yt-dlp is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠ yt-dlp not found. Installing...")
        try:
            # Try pacman first (Arch-based systems)
            subprocess.run(['sudo', 'pacman', '-S', 'yt-dlp', '--noconfirm'], check=True)
            print("✓ yt-dlp installed via pacman")
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Fallback to pip
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'yt-dlp'], check=True)
                print("✓ yt-dlp installed via pip")
            except subprocess.CalledProcessError:
                print("❌ Failed to install yt-dlp. Please install manually:")
                print("  Arch: sudo pacman -S yt-dlp")
                print("  Other: pip install yt-dlp")
                sys.exit(1)
    
    # Check for ffmpeg (needed for audio conversion)
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✓ ffmpeg is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠ ffmpeg not found. Installing...")
        try:
            subprocess.run(['sudo', 'pacman', '-S', 'ffmpeg', '--noconfirm'], check=True)
            print("✓ ffmpeg installed via pacman")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Failed to install ffmpeg. Please install manually:")
            print("  Arch: sudo pacman -S ffmpeg")
            print("  Ubuntu/Debian: sudo apt install ffmpeg")

def clean_title(title):
    """Clean up track title for better YouTube search results"""
    # Remove common problematic parts
    title = re.sub(r'\(feat\..*?\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\(ft\..*?\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\(with.*?\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\(.*?remix.*?\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\(.*?version.*?\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\(.*?edit.*?\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\[.*?\]', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def clean_artist(artist):
    """Clean up artist name"""
    # Remove featuring artists and clean up
    artist = re.sub(r'\s*[,&]\s*.*$', '', artist)
    artist = re.sub(r'\s*feat\..*$', '', artist, flags=re.IGNORECASE)
    artist = re.sub(r'\s*ft\..*$', '', artist, flags=re.IGNORECASE)
    return artist.strip()

def should_add_artist(artist, title):
    """Check if artist name should be added to search (avoid duplication)"""
    if not artist or artist == 'Unknown Artist':
        return False
    
    # Check if artist name is already in the title
    artist_lower = artist.lower()
    title_lower = title.lower()
    
    # Direct match
    if artist_lower in title_lower:
        return False
    
    # Check for partial matches (first word of artist in title)
    artist_first_word = artist_lower.split()[0]
    if len(artist_first_word) > 2 and artist_first_word in title_lower:
        return False
    
    return True

def process_csv_export(csv_file):
    """Process Exportify CSV file"""
    songs = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, 1):
                # Exportify CSV has these columns
                track_name = row.get('Track Name', '').strip()
                artist_name = row.get('Artist Name(s)', '').strip()
                
                if not track_name:
                    print(f"⚠ Row {row_num}: No track name found, skipping")
                    continue
                
                # Clean up names
                if artist_name:
                    artist_name = clean_artist(artist_name)
                    track_name = clean_title(track_name)
                    
                    # Only add artist if it's not already in the title
                    if should_add_artist(artist_name, track_name):
                        search_term = f"{artist_name} {track_name}"
                    else:
                        search_term = track_name
                else:
                    # If no artist, just use the track name
                    track_name = clean_title(track_name)
                    search_term = track_name
                
                songs.append({
                    'artist': artist_name or 'Unknown Artist',
                    'title': track_name,
                    'search': search_term
                })
                
    except FileNotFoundError:
        print(f"❌ File not found: {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        sys.exit(1)
    
    return songs

def process_text_list(text_file):
    """Process plain text list of songs"""
    songs = []
    
    try:
        with open(text_file, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith('#'):  # Skip empty lines and comments
                    continue
                    
                # Try to parse "Artist - Title" format
                if ' - ' in line:
                    parts = line.split(' - ', 1)
                    artist_name = clean_artist(parts[0].strip())
                    track_name = clean_title(parts[1].strip())
                    
                    # Only add artist if it's not already in the title
                    if should_add_artist(artist_name, track_name):
                        search_term = f"{artist_name} {track_name}"
                    else:
                        search_term = track_name
                else:
                    # Treat whole line as search term (no artist info)
                    artist_name = ""
                    track_name = clean_title(line)
                    search_term = track_name
                    
                songs.append({
                    'artist': artist_name or 'Unknown Artist',
                    'title': track_name,
                    'search': search_term
                })
                
    except FileNotFoundError:
        print(f"❌ File not found: {text_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading text file: {e}")
        sys.exit(1)
    
    return songs

def interactive_input():
    """Get playlist information interactively"""
    print("\n🎵 Interactive Playlist Creator")
    print("=" * 40)
    
    songs = []
    print("Enter songs in format 'Artist - Title' (or just 'Title')")
    print("Press Enter with empty line to finish, or 'q' to quit")
    
    while True:
        try:
            song_input = input(f"Song {len(songs) + 1}: ").strip()
            
            if not song_input or song_input.lower() == 'q':
                break
                
            if ' - ' in song_input:
                parts = song_input.split(' - ', 1)
                artist_name = clean_artist(parts[0].strip())
                track_name = clean_title(parts[1].strip())
                
                # Only add artist if it's not already in the title
                if should_add_artist(artist_name, track_name):
                    search_term = f"{artist_name} {track_name}"
                else:
                    search_term = track_name
            else:
                artist_name = ""
                track_name = clean_title(song_input)
                search_term = track_name
                
            songs.append({
                'artist': artist_name or 'Unknown Artist',
                'title': track_name,
                'search': search_term
            })
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            sys.exit(0)
    
    return songs

def generate_youtube_searches(songs, search_quality='best'):
    """Generate YouTube search URLs for each song"""
    search_urls = []
    
    for song in songs:
        # Create different search strategies based on quality setting
        if search_quality == 'best':
            search_query = f"{song['search']} official audio"
        elif search_quality == 'fast':
            search_query = song['search']
        else:  # balanced
            search_query = f"{song['search']} official"
            
        search_url = f"ytsearch1:{search_query}"
        search_urls.append(search_url)
        
    return search_urls

def save_yt_dlp_batch_file(search_urls, output_file='youtube_downloads.txt'):
    """Save URLs in format for yt-dlp batch download"""
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for url in search_urls:
                file.write(url + '\n')
        
        print(f"✓ Created {output_file} with {len(search_urls)} songs")
        return output_file
    except Exception as e:
        print(f"❌ Error creating batch file: {e}")
        sys.exit(1)

def create_download_script(batch_file, output_dir='./Music', audio_format='mp3', quality='best'):
    """Create a shell script to download all songs"""
    
    # Quality settings for yt-dlp
    quality_settings = {
        'best': '--audio-quality 0',
        'good': '--audio-quality 2', 
        'fast': '--audio-quality 5'
    }
    
    quality_option = quality_settings.get(quality, '--audio-quality 0')
    
    script_content = f'''#!/bin/bash

# Auto-generated YouTube music download script
# Downloads songs from Spotify playlist export

OUTPUT_DIR="{output_dir}"
BATCH_FILE="{batch_file}"

# Colors
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

echo -e "${{GREEN}}🎵 Starting batch music download...${{NC}}"
echo -e "${{BLUE}}Output directory: $OUTPUT_DIR${{NC}}"
echo -e "${{BLUE}}Batch file: $BATCH_FILE${{NC}}"
echo -e "${{BLUE}}Audio format: {audio_format}${{NC}}"
echo -e "${{BLUE}}Quality: {quality}${{NC}}"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Count total songs
TOTAL_SONGS=$(wc -l < "$BATCH_FILE")
echo -e "${{YELLOW}}Total songs to download: $TOTAL_SONGS${{NC}}"

# Download all songs with yt-dlp
yt-dlp \\
    --extract-audio \\
    --audio-format {audio_format} \\
    {quality_option} \\
    --output "$OUTPUT_DIR/%(uploader)s - %(title)s.%(ext)s" \\
    --embed-metadata \\
    --add-metadata \\
    --embed-thumbnail \\
    --batch-file "$BATCH_FILE" \\
    --ignore-errors \\
    --no-overwrites \\
    --continue \\
    --retries 3 \\
    --fragment-retries 3 \\
    --progress \\
    --console-title

echo -e "${{GREEN}}✅ Batch download completed!${{NC}}"
echo -e "${{YELLOW}}📁 Check $OUTPUT_DIR for your downloaded music${{NC}}"

# Show download summary
DOWNLOADED=$(find "$OUTPUT_DIR" -name "*.{audio_format}" | wc -l)
echo -e "${{BLUE}}Downloaded: $DOWNLOADED/$TOTAL_SONGS songs${{NC}}"

if [ $DOWNLOADED -lt $TOTAL_SONGS ]; then
    echo -e "${{YELLOW}}⚠ Some songs may have failed to download. Check the log above.${{NC}}"
fi
'''
    
    script_file = 'download_spotify_music.sh'
    try:
        with open(script_file, 'w') as file:
            file.write(script_content)
        
        # Make script executable
        os.chmod(script_file, 0o755)
        print(f"✓ Created executable script: {script_file}")
        return script_file
    except Exception as e:
        print(f"❌ Error creating download script: {e}")
        sys.exit(1)

def save_playlist_info(songs, filename='playlist_info.json'):
    """Save playlist information as JSON for reference"""
    playlist_data = {
        'total_songs': len(songs),
        'songs': songs,
        'created_at': subprocess.check_output(['date']).decode().strip()
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(playlist_data, file, indent=2, ensure_ascii=False)
        print(f"✓ Saved playlist info to {filename}")
    except Exception as e:
        print(f"⚠ Could not save playlist info: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Enhanced Spotify to YouTube Playlist Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s playlist.csv                    # Process CSV export
  %(prog)s songs.txt --format flac        # Process text file, download as FLAC
  %(prog)s --interactive                  # Interactive mode
  %(prog)s playlist.csv --quality fast --output ./Downloads
        '''
    )
    
    parser.add_argument('input_file', nargs='?', help='Input file (CSV or TXT)')
    parser.add_argument('-i', '--interactive', action='store_true', 
                       help='Interactive mode - enter songs manually')
    parser.add_argument('-o', '--output', default='./Music',
                       help='Output directory for downloaded music (default: ./Music)')
    parser.add_argument('-f', '--format', choices=['mp3', 'flac', 'm4a', 'ogg'], default='mp3',
                       help='Audio format (default: mp3)')
    parser.add_argument('-q', '--quality', choices=['best', 'good', 'fast'], default='best',
                       help='Download quality (default: best)')
    parser.add_argument('--no-deps-check', action='store_true',
                       help='Skip dependency checking')
    parser.add_argument('--batch-only', action='store_true',
                       help='Only create batch file, don\'t create download script')
    
    args = parser.parse_args()
    
    # Show help if no arguments provided
    if not args.input_file and not args.interactive:
        parser.print_help()
        print("\nFor CSV files: Use exportify.net to export your Spotify playlist")
        print("For TXT files: Create a text file with 'Artist - Song' on each line")
        sys.exit(1)
    
    # Check dependencies unless skipped
    if not args.no_deps_check:
        check_and_install_dependencies()
    
    # Get songs based on input method
    if args.interactive:
        print("🎵 Interactive mode selected")
        songs = interactive_input()
    else:
        input_file = args.input_file
        if not os.path.exists(input_file):
            print(f"❌ File not found: {input_file}")
            sys.exit(1)
        
        # Determine file type and process accordingly
        if input_file.lower().endswith('.csv'):
            print(f"📊 Processing Spotify CSV export: {input_file}")
            songs = process_csv_export(input_file)
        else:
            print(f"📝 Processing text file: {input_file}")
            songs = process_text_list(input_file)
    
    if not songs:
        print("❌ No songs found!")
        sys.exit(1)
    
    print(f"\n✓ Found {len(songs)} songs")
    
    # Show preview of songs
    print(f"\n🎵 Preview of songs to download:")
    for i, song in enumerate(songs[:5]):
        artist_display = f"{song['artist']} - " if song['artist'] != 'Unknown Artist' else ""
        print(f"  {i+1}. {artist_display}{song['title']}")
    if len(songs) > 5:
        print(f"  ... and {len(songs) - 5} more")
    
    # Generate YouTube search URLs
    print(f"\n🔍 Generating YouTube search URLs (quality: {args.quality})...")
    search_urls = generate_youtube_searches(songs, args.quality)
    
    # Save batch file for yt-dlp
    batch_file = save_yt_dlp_batch_file(search_urls)
    
    # Save playlist info
    save_playlist_info(songs)
    
    if not args.batch_only:
        # Create download script
        script_file = create_download_script(batch_file, args.output, args.format, args.quality)
        
        print(f"\n{'='*50}")
        print("🚀 Setup complete! Now run:")
        print(f"  ./{script_file}")
        print(f"\n🛠 Or manually with yt-dlp:")
        print(f"  yt-dlp -x --audio-format {args.format} -a {batch_file}")
        print(f"\n📊 This will download {len(songs)} songs as {args.format.upper()} files")
        print(f"📁 Output directory: {args.output}")
    else:
        print(f"\n📄 Batch file created: {batch_file}")
        print("Use --batch-only flag removed to also create download script")

if __name__ == "__main__":
    main()
