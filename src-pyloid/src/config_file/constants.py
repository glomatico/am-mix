import inspect

from gamdl.api import AppleMusicApi, WrapperApi
from gamdl.interface import (
    AppleMusicBaseInterface,
    AppleMusicSongInterface,
    AppleMusicMusicVideoInterface,
    AppleMusicUploadedVideoInterface,
    CoverFormat,
    SyncedLyricsFormat,
    MusicVideoResolution,
    MusicVideoCodec,
    SongCodec,
    UploadedVideoQuality,
)
from gamdl.downloader import (
    AppleMusicBaseDownloader,
    AppleMusicDownloader,
    AppleMusicSongDownloader,
    AppleMusicMusicVideoDownloader,
    AppleMusicUploadedVideoDownloader,
    DownloadMode,
    RemuxMode,
    RemuxFormatMusicVideo,
)

from .types import ConfigOption, Config
from .enums import ApiMethod

apple_music_api_create_sig = inspect.signature(AppleMusicApi.create)
wrapper_api_create_sig = inspect.signature(WrapperApi.create)
apple_music_api_create_from_netscape_cookies_sig = inspect.signature(
    AppleMusicApi.create_from_netscape_cookies
)

base_interface_create_sig = inspect.signature(AppleMusicBaseInterface.create)
song_interface_init_sig = inspect.signature(AppleMusicSongInterface.__init__)
music_video_interface_init_sig = inspect.signature(
    AppleMusicMusicVideoInterface.__init__
)
uploaded_video_interface_init_sig = inspect.signature(
    AppleMusicUploadedVideoInterface.__init__
)

base_downloader_init_sig = inspect.signature(AppleMusicBaseDownloader.__init__)
song_downloader_init_sig = inspect.signature(AppleMusicSongDownloader.__init__)
music_video_downloader_init_sig = inspect.signature(
    AppleMusicMusicVideoDownloader.__init__
)
uploaded_video_downloader_init_sig = inspect.signature(
    AppleMusicUploadedVideoDownloader.__init__
)
downloader_init_sig = inspect.signature(AppleMusicDownloader.__init__)

DEFAULT_SETTINGS = Config(
    max_concurrent_downloads=ConfigOption(
        data_type=int,
        default_value=3,
    ),
    cookies=ConfigOption(
        data_type=str,
        default_value=apple_music_api_create_from_netscape_cookies_sig.parameters[
            "cookies_path"
        ].default,
    ),
    wrapper_base_url=ConfigOption(
        data_type=str,
        default_value=wrapper_api_create_sig.parameters["base_url"].default,
    ),
    media_user_token=ConfigOption(
        data_type=str,
        default_value="",
    ),
    api_method=ConfigOption(
        data_type=ApiMethod,
        default_value=ApiMethod.COOKIES,
    ),
    language=ConfigOption(
        data_type=str,
        default_value=apple_music_api_create_sig.parameters["language"].default,
    ),
    cover_format=ConfigOption(
        data_type=CoverFormat,
        default_value=base_interface_create_sig.parameters["cover_format"].default,
    ),
    cover_size=ConfigOption(
        data_type=int,
        default_value=base_interface_create_sig.parameters["cover_size"].default,
    ),
    wvd=ConfigOption(
        data_type=str,
        default_value=base_interface_create_sig.parameters["wvd_path"].default,
        nullable=True,
    ),
    synced_lyrics_format=ConfigOption(
        data_type=SyncedLyricsFormat,
        default_value=song_interface_init_sig.parameters[
            "synced_lyrics_format"
        ].default,
    ),
    song_codec=ConfigOption(
        data_type=SongCodec,
        default_value=song_interface_init_sig.parameters["codec_priority"].default,
        is_list=True,
    ),
    use_album_date=ConfigOption(
        data_type=bool,
        default_value=False,
    ),
    synced_lyrics_only=ConfigOption(
        data_type=bool,
        default_value=False,
    ),
    music_video_resolution=ConfigOption(
        data_type=MusicVideoResolution,
        default_value=music_video_interface_init_sig.parameters["resolution"].default,
    ),
    music_video_codec=ConfigOption(
        data_type=MusicVideoCodec,
        default_value=music_video_interface_init_sig.parameters[
            "codec_priority"
        ].default,
        is_list=True,
    ),
    uploaded_video_quality=ConfigOption(
        data_type=UploadedVideoQuality,
        default_value=uploaded_video_interface_init_sig.parameters["quality"].default,
    ),
    # Base Downloader options
    output=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters["output_path"].default,
    ),
    temp=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters["temp_path"].default,
    ),
    nm3u8dlre=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters["nm3u8dlre_path"].default,
        nullable=True,
    ),
    download_mode=ConfigOption(
        data_type=DownloadMode,
        default_value=base_downloader_init_sig.parameters["download_mode"].default,
    ),
    album_folder_template=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters[
            "album_folder_template"
        ].default,
    ),
    compilation_folder_template=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters[
            "compilation_folder_template"
        ].default,
    ),
    no_album_folder_template=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters[
            "no_album_folder_template"
        ].default,
    ),
    playlist_folder_template=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters[
            "playlist_folder_template"
        ].default,
    ),
    single_disc_file_template=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters[
            "single_disc_file_template"
        ].default,
    ),
    multi_disc_file_template=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters[
            "multi_disc_file_template"
        ].default,
    ),
    no_album_file_template=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters[
            "no_album_file_template"
        ].default,
    ),
    playlist_file_template=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters[
            "playlist_file_template"
        ].default,
    ),
    date_tag_template=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters["date_tag_template"].default,
    ),
    exclude_tags=ConfigOption(
        data_type=str,
        default_value=base_downloader_init_sig.parameters["exclude_tags"].default,
        is_list=True,
        nullable=True,
    ),
    truncate=ConfigOption(
        data_type=int,
        default_value=base_downloader_init_sig.parameters["truncate"].default,
        nullable=True,
    ),
    # Downloader options
    overwrite=ConfigOption(
        data_type=bool,
        default_value=False,
    ),
    save_cover=ConfigOption(
        data_type=bool,
        default_value=False,
    ),
    save_playlist=ConfigOption(
        data_type=bool,
        default_value=False,
    ),
    no_synced_lyrics=ConfigOption(
        data_type=bool,
        default_value=False,
    ),
    music_video_remux_format=ConfigOption(
        data_type=RemuxFormatMusicVideo,
        default_value=music_video_downloader_init_sig.parameters[
            "remux_format"
        ].default,
    ),
)
