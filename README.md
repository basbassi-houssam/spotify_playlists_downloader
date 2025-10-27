# 🎵 Spotify to YouTube Playlist Converter

Convert your Spotify playlists to downloadable YouTube audio files with a single command. This tool takes Spotify playlist exports and automatically downloads the songs from YouTube using yt-dlp.

## ✨ Features

- 📊 **Multiple Input Formats**: CSV exports, plain text files, or interactive mode
- 🎯 **Smart Search**: Intelligently cleans and optimizes search terms for better YouTube matches
- 🎚️ **Quality Options**: Choose between best, good, or fast quality downloads
- 📁 **Format Support**: MP3, FLAC, M4A, or OGG audio formats
- 🔄 **Batch Processing**: Download entire playlists with a single script
- 🛠️ **Auto-Setup**: Automatically checks and installs dependencies (yt-dlp, ffmpeg)
- 📝 **Metadata**: Embeds thumbnails and metadata in downloaded files

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- Internet connection

The script will automatically install `yt-dlp` and `ffmpeg` if they're missing.

### Installation

```bash
# Clone the repository
git clone https://github.com/basbassi-houssam/spotify_playlists_downloader.git
cd spotify_playlists_downloader

# Make it executable
chmod +x spotify_converter.py
```

## 📖 Usage

### Method 1: Using Spotify CSV Export (Recommended)

1. Export your Spotify playlist using [Exportify](https://exportify.net/)
2. Download the CSV file
3. Run the converter:

```bash
./spotify_converter.py playlist.csv
```

4. Execute the generated download script:

```bash
./download_spotify_music.sh
```

### Method 2: Using a Text File

Create a text file with one song per line in the format `Artist - Title`:

```text
The Beatles - Hey Jude
Pink Floyd - Comfortably Numb
Queen - Bohemian Rhapsody
```

Then run:

```bash
./spotify_converter.py songs.txt
```

### Method 3: Interactive Mode

Enter songs manually through an interactive prompt:

```bash
./spotify_converter.py --interactive
```

## 🎛️ Command Line Options

```bash
./spotify_converter.py [INPUT_FILE] [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --interactive` | Interactive mode - enter songs manually | - |
| `-o, --output DIR` | Output directory for downloaded music | `./Music` |
| `-f, --format FORMAT` | Audio format: mp3, flac, m4a, ogg | `mp3` |
| `-q, --quality QUALITY` | Download quality: best, good, fast | `best` |
| `--no-deps-check` | Skip dependency checking | - |
| `--batch-only` | Only create batch file, not download script | - |

### Examples

```bash
# Download as FLAC with best quality
./spotify_converter.py playlist.csv --format flac --quality best

# Fast download to custom directory
./spotify_converter.py songs.txt --quality fast --output ~/Downloads/Music

# Create batch file only (manual download later)
./spotify_converter.py playlist.csv --batch-only

# Interactive mode with custom settings
./spotify_converter.py --interactive --format m4a --output ./MyMusic
```

## 📁 Output Files

The script generates several files:

- `youtube_downloads.txt` - Batch file with YouTube search URLs
- `download_spotify_music.sh` - Executable download script
- `playlist_info.json` - Playlist metadata and song list
- `./Music/` - Downloaded audio files (or custom directory)

## 🎯 How It Works

1. **Input Processing**: Reads your playlist from CSV, TXT, or interactive input
2. **Smart Cleaning**: Removes duplicates, featured artists, and remix tags for cleaner searches
3. **Search Generation**: Creates optimized YouTube search queries
4. **Batch File Creation**: Generates a yt-dlp compatible batch file
5. **Download Script**: Creates an executable shell script for easy downloading
6. **Execution**: Run the script to download all songs with proper metadata

## 🔧 Troubleshooting

### Dependencies Not Installing

Manually install dependencies:

```bash
# Arch Linux
sudo pacman -S yt-dlp ffmpeg

# Ubuntu/Debian
sudo apt install yt-dlp ffmpeg

# macOS (with Homebrew)
brew install yt-dlp ffmpeg

# Using pip (all platforms)
pip install yt-dlp
```
# 🎵 Spotify to YouTube Playlist Converter

Convert your Spotify playlists to downloadable YouTube audio files with a single command. This tool takes Spotify playlist exports and automatically downloads the songs from YouTube using yt-dlp.

## ✨ Features

- 📊 **Multiple Input Formats**: CSV exports, plain text files, or interactive mode
- 🎯 **Smart Search**: Intelligently cleans and optimizes search terms for better YouTube matches
- 🎚️ **Quality Options**: Choose between best, good, or fast quality downloads
- 📁 **Format Support**: MP3, FLAC, M4A, or OGG audio formats
- 🔄 **Batch Processing**: Download entire playlists with a single script
- 🛠️ **Auto-Setup**: Automatically checks and installs dependencies (yt-dlp, ffmpeg)
- 📝 **Metadata**: Embeds thumbnails and metadata in downloaded files

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- Internet connection

The script will automatically install `yt-dlp` and `ffmpeg` if they're missing.

### Installation

```bash
# Clone the repository
git clone https://github.com/basbassi-houssam/spotify_playlists_downloader.git
cd spotify_playlists_downloader

# Make it executable
chmod +x spotify_converter.py
```

## 📖 Usage

### Method 1: Using Spotify CSV Export (Recommended)

1. Export your Spotify playlist using [Exportify](https://exportify.net/)
2. Download the CSV file
3. Run the converter:

```bash
./spotify_converter.py playlist.csv
```

4. Execute the generated download script:

```bash
./download_spotify_music.sh
```

### Method 2: Using a Text File

Create a text file with one song per line in the format `Artist - Title`:

```text
The Beatles - Hey Jude
Pink Floyd - Comfortably Numb
Queen - Bohemian Rhapsody
```

Then run:

```bash
./spotify_converter.py songs.txt
```

### Method 3: Interactive Mode

Enter songs manually through an interactive prompt:

```bash
./spotify_converter.py --interactive
```

## 🎛️ Command Line Options

```bash
./spotify_converter.py [INPUT_FILE] [OPTIONS]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --interactive` | Interactive mode - enter songs manually | - |
| `-o, --output DIR` | Output directory for downloaded music | `./Music` |
| `-f, --format FORMAT` | Audio format: mp3, flac, m4a, ogg | `mp3` |
| `-q, --quality QUALITY` | Download quality: best, good, fast | `best` |
| `--no-deps-check` | Skip dependency checking | - |
| `--batch-only` | Only create batch file, not download script | - |

### Examples

```bash
# Download as FLAC with best quality
./spotify_converter.py playlist.csv --format flac --quality best

# Fast download to custom directory
./spotify_converter.py songs.txt --quality fast --output ~/Downloads/Music

# Create batch file only (manual download later)
./spotify_converter.py playlist.csv --batch-only

# Interactive mode with custom settings
./spotify_converter.py --interactive --format m4a --output ./MyMusic
```

## 📁 Output Files

The script generates several files:

- `youtube_downloads.txt` - Batch file with YouTube search URLs
- `download_spotify_music.sh` - Executable download script
- `playlist_info.json` - Playlist metadata and song list
- `./Music/` - Downloaded audio files (or custom directory)

## 🎯 How It Works

1. **Input Processing**: Reads your playlist from CSV, TXT, or interactive input
2. **Smart Cleaning**: Removes duplicates, featured artists, and remix tags for cleaner searches
3. **Search Generation**: Creates optimized YouTube search queries
4. **Batch File Creation**: Generates a yt-dlp compatible batch file
5. **Download Script**: Creates an executable shell script for easy downloading
6. **Execution**: Run the script to download all songs with proper metadata

## 🔧 Troubleshooting

### Dependencies Not Installing

Manually install dependencies:

```bash
# Arch Linux
sudo pacman -S yt-dlp ffmpeg

# Ubuntu/Debian
sudo apt install yt-dlp ffmpeg

# macOS (with Homebrew)
brew install yt-dlp ffmpeg

# Using pip (all platforms)
pip install yt-dlp
```

### Songs Not Found

- Try different quality settings (`--quality fast` uses broader searches)
- Check if song names are correct in your input file
- Some songs may not be available on YouTube

### Download Fails

- Ensure stable internet connection
- The script uses `--ignore-errors` flag, so partial downloads will continue
- Check yt-dlp is up to date: `yt-dlp -U`

## 📝 Input File Formats

### CSV Format (Exportify)

The CSV should have these columns:
- `Track Name`
- `Artist Name(s)`

### Text Format

```text
Artist - Song Title
Another Artist - Another Song
# Comments start with #
Song Without Artist Info
```

## 🎨 Advanced Usage

### Custom yt-dlp Options

Edit the generated `download_spotify_music.sh` script to add custom yt-dlp options:

```bash
yt-dlp \
    --your-custom-options \
    --batch-file youtube_downloads.txt
```

### Manual Download

Use the batch file directly with yt-dlp:

```bash
yt-dlp -x --audio-format mp3 -a youtube_downloads.txt
```

## 📊 Quality Settings

- **best**: Highest quality audio (slower downloads, larger files)
- **good**: Balanced quality and speed (recommended for most users)
- **fast**: Lower quality, faster downloads (smaller files)

## ⭐ Star This Project

If you find this tool useful, please consider giving it a star on GitHub! It helps others discover the project and motivates continued development.

[![GitHub stars](https://img.shields.io/github/stars/basbassi-houssam/spotify_playlists_downloader?style=social)](https://github.com/basbassi-houssam/spotify_playlists_downloader/stargazers)

## ☕ Support the Project

If this tool saved you time or you'd like to support its development, consider buying me a coffee!

[![PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/paypalme/BasbassiHoussam)
[![Ko-fi](https://img.shields.io/badge/Support-Ko--fi-red.svg)](https://ko-fi.com/basbassihoussam)

Every contribution helps maintain and improve this project. Thank you! 🙏

## ⚠️ Legal Notice

This tool is for personal use only. Ensure you have the right to download and store the content. Respect copyright laws and YouTube's Terms of Service.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📄 License

MIT License - Feel free to use and modify as needed.

## 🙏 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful download engine
- [Exportify](https://exportify.net/) - Spotify playlist export tool
- [FFmpeg](https://ffmpeg.org/) - Audio processing

---

**Made with ❤️ for music lovers who want to own their playlists**
The CSV should have these columns:
- `Track Name`
- `Artist Name(s)`

### Text Format

```text
Artist - Song Title
Another Artist - Another Song
# Comments start with #
Song Without Artist Info
```

## 🎨 Advanced Usage

### Custom yt-dlp Options

Edit the generated `download_spotify_music.sh` script to add custom yt-dlp options:

```bash
yt-dlp \
    --your-custom-options \
    --batch-file youtube_downloads.txt
```

### Manual Download

Use the batch file directly with yt-dlp:

```bash
yt-dlp -x --audio-format mp3 -a youtube_downloads.txt
```

## 📊 Quality Settings

- **best**: Highest quality audio (slower downloads, larger files)
- **good**: Balanced quality and speed (recommended for most users)
- **fast**: Lower quality, faster downloads (smaller files)

## ⭐ Star This Project

If you find this tool useful, please consider giving it a star on GitHub! It helps others discover the project and motivates continued development.

[![GitHub stars](https://img.shields.io/github/stars/basbassi-houssam/spotify_playlists_downloader?style=social)](https://github.com/basbassi-houssam/spotify_playlists_downloader/stargazers)

## ☕ Support the Project

If this tool saved you time or you'd like to support its development, consider buying me a coffee!

[![PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/paypalme/BasbassiHoussam)
[![Ko-fi](https://img.shields.io/badge/Support-Ko--fi-red.svg)](https://ko-fi.com/basbassihoussam)

Every contribution helps maintain and improve this project. Thank you! 🙏

## ⚠️ Legal Notice

This tool is for personal use only. Ensure you have the right to download and store the content. Respect copyright laws and YouTube's Terms of Service.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📄 License

MIT License - Feel free to use and modify as needed.

## 🙏 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful download engine
- [Exportify](https://exportify.net/) - Spotify playlist export tool
- [FFmpeg](https://ffmpeg.org/) - Audio processing

---

**Made with ❤️ for music lovers who want to own their playlists**
