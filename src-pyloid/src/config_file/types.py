from dataclasses import dataclass
from typing import Any


@dataclass
class ConfigOption:
    data_type: type
    default_value: Any
    nullable: bool = False
    is_list: bool = False


@dataclass
class Config:
    # Application Options
    max_concurrent_downloads: Any = None
    # API options
    cookies: Any = None
    wrapper_base_url: Any = None
    media_user_token: Any = None
    api_method: Any = None
    language: Any = None
    # Base Interface options
    cover_format: Any = None
    cover_size: Any = None
    wvd: Any = None
    synced_lyrics_format: Any = None
    song_codec: Any = None
    use_album_date: Any = None
    synced_lyrics_only: Any = None
    # Music Video Interface options
    music_video_resolution: Any = None
    music_video_codec: Any = None
    # Uploaded Video Interface options
    uploaded_video_quality: Any = None
    # Base Downloader options
    output: Any = None
    temp: Any = None
    nm3u8dlre: Any = None
    download_mode: Any = None
    album_folder_template: Any = None
    compilation_folder_template: Any = None
    no_album_folder_template: Any = None
    playlist_folder_template: Any = None
    single_disc_file_template: Any = None
    multi_disc_file_template: Any = None
    no_album_file_template: Any = None
    playlist_file_template: Any = None
    date_tag_template: Any = None
    exclude_tags: Any = None
    truncate: Any = None
    # Downloader options
    overwrite: Any = None
    save_cover: Any = None
    save_playlist: Any = None
    no_synced_lyrics: Any = None
    # Music Video Downloader options
    music_video_remux_format: Any = None
