<img src="src/assets/logo.svg" alt="am-mix Logo" width="100%" height="200" align="center"/>

# am-mix

Desktop app for downloading media from [Apple Music](https://music.apple.com).

Powered by [gamdl](https://github.com/glomatico/gamdl) on the backend and built with [Vue](https://vuejs.org/) + [Pyloid](https://github.com/pyloid/docs).

**Discord:** <https://discord.gg/aBjMEZ9tnq>

> [!WARNING]
> **Early development** - features and behavior may change; some flows are still experimental. Use at your own risk.

<img src="screenshot.png"/>

## ✨ Features

- 🔍 **Search & URLs** - Search Apple Music or paste song, music video, uploaded video, album, and playlist links.
- 📥 **Download Queue** - Concurrent downloads with retry and cancel.
- 🎵 **Songs & Lyrics** - Download songs in various formats with synced lyrics.
- 🎬 **Music Videos & Posts** - Music videos up to 4K and artist uploaded videos.
- 🎤 **Artist Pages** - Browse catalogs and queue an entire tab at once.

## 📋 Prerequisites

### Required

- **Active Apple Music subscription**
- **Apple Music authentication** (configure one method in [Settings](#settings) on first launch):
  - **Cookies** - export your browser cookies in Netscape format while logged in at [Apple Music](https://music.apple.com):
    - **Firefox**: [Export Cookies](https://addons.mozilla.org/addon/export-cookies-txt)
    - **Chromium**: [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
  - **Media user token** - paste your token from the browser (advanced)
  - **Wrapper** - use a [wrapper](https://github.com/WorldObservationLog/wrapper) server instead of cookies. This is useful for wrapper-based login and required for some experimental song codecs; see [gamdl's wrapper docs](https://github.com/glomatico/gamdl#wrapper).

### Dependencies

#### Wrapper

Use the [wrapper](https://github.com/WorldObservationLog/wrapper) for wrapper authentication and non-web song codecs such as `aac`, `aac-he`, `atmos`, `ac3`, or `alac`.

Cookies are not required when using the wrapper API method.

#### N_m3u8DL-RE

Use [N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE/releases/latest) only if you set Download Mode to `nm3u8dlre` for faster downloads.

Add it to your system **PATH** or set its path in [Settings](#settings) (`~/.am-mix/config.yml`).

## 📦 Installation

1. Download the latest release from [GitHub](https://github.com/glomatico/am-mix/releases/latest).
2. Extract the zip file.
3. Run the `am-mix` executable.

## ⚙️ Settings

Configure your settings in the Settings page or using the config file (`~/.am-mix/config.yml`).

### Template Variables

**Tags for templates and exclude-tags:**

- `album`, `album_artist`, `album_id`
- `artist`, `artist_id`
- `composer`, `composer_id`
- `date` (supports strftime format: `{date:%Y}`)
- `disc`, `disc_total`
- `media_type`
- `playlist_artist`, `playlist_id`, `playlist_title`, `playlist_track`
- `title`, `title_id`
- `track`, `track_total`

**Tags for exclude-tags only:**

- `album_sort`, `artist_sort`, `composer_sort`, `title_sort`
- `comment`, `compilation`, `copyright`, `cover`, `gapless`, `genre`, `genre_id`, `lyrics`, `rating`, `storefront`, `xid`
- `all` (special: skip all tagging)

### Song Codecs

**Web:**

- `aac-web` - AAC 256kbps 44.1kHz
- `aac-he-web` - AAC-HE 64kbps 44.1kHz

**Non-web** (wrapper recommended; may not work without wrapper due to API limitations):

- `aac` - AAC 256kbps up to 48kHz
- `aac-he` - AAC-HE 64kbps up to 48kHz
- `aac-binaural` - AAC 256kbps binaural
- `aac-downmix` - AAC 256kbps downmix
- `aac-he-binaural` - AAC-HE 64kbps binaural
- `aac-he-downmix` - AAC-HE 64kbps downmix
- `atmos` - Dolby Atmos 768kbps
- `ac3` - AC3 640kbps
- `alac` - ALAC up to 24-bit/192kHz
- `ask` - Interactive codec selection

### Music Video Codecs

- `h264`
- `h265`
- `ask` - Interactive codec selection

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.
