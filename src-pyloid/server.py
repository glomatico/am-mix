import asyncio
import inspect
import threading
from pathlib import Path
from typing import Any

from gamdl.api import AppleMusicApi, WrapperApi
from gamdl.api.exceptions import GamdlApiResponseError
from gamdl.downloader import (
    AppleMusicBaseDownloader,
    AppleMusicDownloader,
    AppleMusicMusicVideoDownloader,
    AppleMusicSongDownloader,
    AppleMusicUploadedVideoDownloader,
)
from gamdl.interface import (
    AppleMusicBaseInterface,
    AppleMusicInterface,
    AppleMusicMusicVideoInterface,
    AppleMusicSongInterface,
    AppleMusicUploadedVideoInterface,
)
from pyloid.browser_window import BrowserWindow
from pyloid.rpc import PyloidRPC, RPCError
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QInputDialog, QLineEdit, QWidget
from src.config_file import ApiMethod, ConfigFile
from src.download_manager.manager import DownloadManager

from src import __version__


class CustomRpc(PyloidRPC):
    def __init__(self):
        super().__init__()

        self.window: BrowserWindow = None

        self._functions["initialize_config_file"] = self.initialize_config_file
        self._functions["initialize_apple_music_api"] = self.initialize_apple_music_api
        self._functions["initialize_apple_music_interface"] = (
            self._initialize_apple_music_interface
        )
        self._functions["initialize_apple_music_downloader"] = (
            self.initialize_apple_music_downloader
        )
        self._functions["initialize_download_manager"] = (
            self.initialize_download_manager
        )
        self._functions["open_file_dialog"] = self.open_file_dialog
        self._functions["select_directory_dialog"] = self.select_directory_dialog
        self._functions["open_url"] = self.open_url
        self._functions["get_version"] = self.get_version

    def _raise_rpc_error(self, e: Exception) -> None:
        raise RPCError(message=str(e))

    def _bind_methods(
        self,
        cls: object,
        prefix: str,
    ) -> None:
        for method_name in dir(cls):
            if method_name.startswith("_"):
                continue

            if isinstance(getattr(type(cls), method_name, None), property):
                continue

            method = getattr(cls, method_name)

            if not callable(method):
                continue

            async def rpc_method(*args, __method=method, **kwargs):
                try:
                    if inspect.iscoroutinefunction(__method):
                        return await __method(*args, **kwargs)
                    else:
                        return await asyncio.to_thread(__method, *args, **kwargs)
                except Exception as e:
                    self._raise_rpc_error(e)

            rpc_method.__signature__ = inspect.signature(method)

            self._functions[f"{prefix}_{method_name}"] = rpc_method

    async def initialize_config_file(self, ignore_error: bool = False) -> None:
        self.config_file = ConfigFile()

        if self.config_file.parse_errors and not ignore_error:
            # raise Exception(list(self.config_file.parse_errors.values())[0])
            raise RPCError(
                message=(
                    "Failed to parse Config File:\n"
                    + "\n".join(
                        f"{file}: {error}"
                        for file, error in self.config_file.parse_errors.items()
                    )
                )
            )

        self._bind_methods(self.config_file, "config_file")

    async def initialize_apple_music_api(self) -> None:
        config = self.config_file.config

        try:
            if config.api_method == ApiMethod.WRAPPER:
                self.wrapper_api = await WrapperApi.create(
                    base_url=config.wrapper_base_url,
                    get_credentials_func=self.wrapper_credentials_handler,
                    get_2fa_code=self.wrapper_2fa_handler,
                )
            else:
                self.wrapper_api = None

            if config.api_method == ApiMethod.COOKIES:
                self.apple_music_api = await AppleMusicApi.create_from_netscape_cookies(
                    cookies_path=config.cookies,
                    language=config.language,
                )
            elif config.api_method == ApiMethod.WRAPPER:
                self.apple_music_api = await AppleMusicApi.create_from_wrapper(
                    wrapper_api=self.wrapper_api,
                )
            else:
                self.apple_music_api = await AppleMusicApi.create(
                    media_user_token=config.media_user_token,
                    language=config.language,
                    storefront=None,
                )
        except Exception as e:
            self._raise_rpc_error(e)

        self._bind_methods(
            self.apple_music_api,
            "apple_music_api",
        )

    async def _initialize_apple_music_interface(self) -> None:
        config = self.config_file.config

        try:
            base = await AppleMusicBaseInterface.create(
                self.apple_music_api,
                cover_format=config.cover_format,
                cover_size=config.cover_size,
                wvd_path=config.wvd,
                wrapper_api=self.wrapper_api,
            )
        except Exception as e:
            self._raise_rpc_error(e)

        song = AppleMusicSongInterface(
            base,
            synced_lyrics_format=config.synced_lyrics_format,
            codec_priority=config.song_codec,
            use_album_date=config.use_album_date,
            skip_stream_info=config.synced_lyrics_only,
        )
        music_video = AppleMusicMusicVideoInterface(
            base,
            resolution=config.music_video_resolution,
            codec_priority=config.music_video_codec,
        )
        uploaded_video = AppleMusicUploadedVideoInterface(
            base,
            quality=config.uploaded_video_quality,
        )

        self.apple_music_interface = AppleMusicInterface(
            song,
            music_video,
            uploaded_video,
        )

    async def initialize_apple_music_downloader(self) -> None:
        config = self.config_file.config

        base = AppleMusicBaseDownloader(
            self.apple_music_interface,
            output_path=config.output,
            temp_path=config.temp,
            nm3u8dlre_path=config.nm3u8dlre,
            download_mode=config.download_mode,
            album_folder_template=config.album_folder_template,
            compilation_folder_template=config.compilation_folder_template,
            no_album_folder_template=config.no_album_folder_template,
            playlist_folder_template=config.playlist_folder_template,
            single_disc_file_template=config.single_disc_file_template,
            multi_disc_file_template=config.multi_disc_file_template,
            no_album_file_template=config.no_album_file_template,
            playlist_file_template=config.playlist_file_template,
            date_tag_template=config.date_tag_template,
            exclude_tags=config.exclude_tags,
            truncate=config.truncate,
            silent=True,
        )

        song = AppleMusicSongDownloader(base)
        music_video = AppleMusicMusicVideoDownloader(
            base,
            remux_format=config.music_video_remux_format,
        )
        uploaded_video = AppleMusicUploadedVideoDownloader(base)

        self.apple_music_downloader = AppleMusicDownloader(
            song,
            music_video,
            uploaded_video,
            overwrite=config.overwrite,
            save_cover=config.save_cover,
            save_playlist=config.save_playlist,
            no_synced_lyrics=config.no_synced_lyrics,
            synced_lyrics_only=config.synced_lyrics_only,
        )

    async def queue_callback(self, payload: dict[str, Any]) -> None:
        """Payload shape: ``{"delete": bool, "item": dict}`` (see DownloadManager._notify_queue_change)."""
        if self.window:
            try:
                self.window.invoke("download_manager_queue_update", payload)
            except Exception as e:
                print(f"[CustomRpc] Error invoking queue update: {e}")

    async def initialize_download_manager(self) -> None:
        self.download_manager = DownloadManager(
            downloader=self.apple_music_downloader,
            max_concurrent_tasks=self.config_file.config.max_concurrent_downloads,
            queue_callback=self.queue_callback,
        )

        self._bind_methods(
            self.download_manager,
            "download_manager",
        )

    async def open_file_dialog(
        self,
        filter: str,
    ) -> str | None:
        return self.pyloid.open_file_dialog(filter=filter)

    async def select_directory_dialog(
        self,
        dir: str | None = None,
    ) -> str | None:
        return self.pyloid.select_directory_dialog(dir=dir)

    async def open_url(self, url: str, folder: bool = False) -> None:
        if folder:
            path_obj = Path(url)
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path_obj.parent)))
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(url))

    async def get_version(self) -> str:
        return __version__

    def _dialog_parent(self) -> QWidget | None:
        if self.window is None:
            return None

        return self.window._window._window

    def _qt_input_text(
        self,
        title: str,
        label: str,
        *,
        password: bool = False,
    ) -> str | None:
        result: list[str | None] = [None]

        def show_dialog() -> None:
            echo = (
                QLineEdit.EchoMode.Password if password else QLineEdit.EchoMode.Normal
            )
            text, ok = QInputDialog.getText(
                self._dialog_parent(),
                title,
                label,
                echo=echo,
            )
            result[0] = text.strip() if ok and text.strip() else None

        if threading.current_thread() is threading.main_thread():
            show_dialog()
        else:
            finished = threading.Event()

            def show_dialog_and_finish() -> None:
                try:
                    show_dialog()
                finally:
                    finished.set()

            parent = self._dialog_parent()
            QTimer.singleShot(
                0,
                parent or QApplication.instance(),
                show_dialog_and_finish,
            )
            finished.wait()
        return result[0]

    def wrapper_credentials_handler(self) -> tuple[str, str]:
        username = self._qt_input_text(
            "Apple Music Login",
            "Apple ID:",
        )
        if username is None:
            raise GamdlApiResponseError("Wrapper login cancelled")

        password = self._qt_input_text(
            "Apple Music Login",
            "Password:",
            password=True,
        )
        if password is None:
            raise GamdlApiResponseError("Wrapper login cancelled")

        return username, password

    def wrapper_2fa_handler(self) -> str:
        code = self._qt_input_text(
            "Two-Factor Authentication",
            "Verification code:",
        )
        if code is None:
            raise GamdlApiResponseError("Wrapper 2FA cancelled")
        return code
