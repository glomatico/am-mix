import asyncio
import inspect
import logging
from collections.abc import Awaitable, Callable
from typing import Any

import aiojobs
from gamdl.downloader import AppleMusicDownloader
from gamdl.interface import GamdlInterfaceFlatFilterExcludedError

from .types import DownloadManagerItem, DownloadStatus

log = logging.getLogger(__name__)

ACTIVE_STATUSES = {
    DownloadStatus.PENDING_FETCHING,
    DownloadStatus.FETCHING,
    DownloadStatus.PENDING_DOWNLOADING,
    DownloadStatus.DOWNLOADING,
}

PENDING_STATUSES = {
    DownloadStatus.PENDING_FETCHING,
    DownloadStatus.PENDING_DOWNLOADING,
}

FINISHED_STATUSES = {
    DownloadStatus.COMPLETED,
    DownloadStatus.FAILED,
}


class DownloadManager:
    """Download queue with concurrency cap via aiojobs.Scheduler."""

    def __init__(
        self,
        downloader: AppleMusicDownloader,
        max_concurrent_tasks: int = 3,
        queue_callback: (
            Callable[[dict[str, Any]], None | Awaitable[None]] | None
        ) = None,
    ):
        self.downloader = downloader
        self.max_concurrent_tasks = max_concurrent_tasks
        self.queue_callback = queue_callback

        self._queue_dict: dict[str, DownloadManagerItem] = {}
        self._job_dict: dict[str, aiojobs.Job] = {}

        self._scheduler = aiojobs.Scheduler(
            limit=self.max_concurrent_tasks,
            pending_limit=0,
        )

        self.downloader.base.interface.flat_filter_function = (
            self._interface_flat_filter
        )

    async def _interface_flat_filter(self, media_metadata: dict) -> bool | None:
        media_id = media_metadata.get("id")
        if not media_id:
            return None

        existing_item = self._queue_dict.get(media_id)

        if existing_item and existing_item.status in ACTIVE_STATUSES:
            return True

        return None

    def _serialize_item(self, media_id: str) -> dict | None:
        item = self._queue_dict.get(media_id)

        if not item:
            return None

        media_metadata = (
            item.download_item.media.media_metadata
            if item.download_item and item.download_item.media.media_metadata
            else {}
        )

        attributes = media_metadata.get("attributes", {})

        return {
            "media_id": media_id,
            "status": item.status.value,
            "error_message": str(item.error) if item.error else None,
            "media_title": attributes.get("name") or media_id,
            "media_cover": attributes.get("artwork", {}).get("url"),
            "media_artist": attributes.get("artistName"),
            "media_final_path": (
                item.download_item.final_path if item.download_item else None
            ),
        }

    async def _notify_queue_change(self, media_id: str, delete: bool = False) -> None:
        if not self.queue_callback:
            return

        serialized = self._serialize_item(media_id)

        if not serialized:
            serialized = {
                "media_id": media_id,
                "status": None,
                "error_message": None,
                "media_title": media_id,
                "media_cover": None,
                "media_artist": None,
                "media_final_path": None,
            }

        result = self.queue_callback(
            {
                "delete": delete,
                "item": serialized,
            }
        )

        if inspect.isawaitable(result):
            await result

    async def clear_queue(self) -> None:
        for media_id in list(self._queue_dict.keys()):
            existing_item = self._queue_dict.get(media_id)
            if existing_item and existing_item.status in FINISHED_STATUSES:
                self._queue_dict.pop(media_id, None)
                self._job_dict.pop(media_id, None)
                await self._notify_queue_change(media_id, delete=True)

    async def retry_item(self, item_id: str) -> None:
        item = self._queue_dict.get(item_id)

        if not item or item.status != DownloadStatus.FAILED:
            return

        item_url = (
            item.download_item.media.media_metadata.get("attributes", {}).get("url")
            if item.download_item and item.download_item.media.media_metadata
            else None
        )

        self._queue_dict.pop(item_id, None)
        self._job_dict.pop(item_id, None)

        await self._notify_queue_change(item_id, delete=True)
        await self.add_to_queue(item_url or item_id)

    async def cancel_item(self, item_id: str) -> None:
        item = self._queue_dict.get(item_id)

        if not item or item.status not in PENDING_STATUSES:
            return

        job = self._job_dict.pop(item_id, None)
        self._queue_dict.pop(item_id, None)
        await self._notify_queue_change(item_id, delete=True)

        if job and not job.closed:
            await job.close()

    async def add_to_queue(self, url: str) -> None:
        existing_item = self._queue_dict.get(url)

        if existing_item and existing_item.status in ACTIVE_STATUSES:
            return

        self._queue_dict[url] = DownloadManagerItem(
            media_id=url,
            download_item=None,
            status=DownloadStatus.PENDING_FETCHING,
        )

        await self._notify_queue_change(url)

        self._job_dict[url] = await self._scheduler.spawn(self._fetch_item(url))

    async def _fetch_item(self, url: str) -> None:
        try:
            fetch_item = self._queue_dict.get(url)

            if not fetch_item or fetch_item.status != DownloadStatus.PENDING_FETCHING:
                return

            fetch_item.status = DownloadStatus.FETCHING
            await self._notify_queue_change(url)

            collected_items = []

            try:
                async for download_item in self.downloader.get_download_item_from_url(
                    url
                ):
                    if download_item.media.partial:
                        continue

                    if isinstance(
                        download_item.media.error,
                        GamdlInterfaceFlatFilterExcludedError,
                    ):
                        continue

                    collected_items.append(download_item)

            except asyncio.CancelledError:
                fetch_item.status = DownloadStatus.FAILED
                fetch_item.error = RuntimeError("Download canceled")
                await self._notify_queue_change(url)
                raise

            except Exception as e:
                log.exception("Failed to fetch item from %s", url)
                fetch_item.status = DownloadStatus.FAILED
                fetch_item.error = e
                await self._notify_queue_change(url)
                return

            for download_item in collected_items:
                media_id = download_item.media.media_id

                existing_item = self._queue_dict.get(media_id)

                if existing_item and existing_item.status in ACTIVE_STATUSES:
                    continue

                self._queue_dict[media_id] = DownloadManagerItem(
                    media_id=media_id,
                    download_item=download_item,
                    status=DownloadStatus.PENDING_DOWNLOADING,
                )

                await self._notify_queue_change(media_id)

                self._job_dict[media_id] = await self._scheduler.spawn(
                    self._download_item(media_id)
                )

            self._queue_dict.pop(url, None)
            await self._notify_queue_change(url, delete=True)

        finally:
            self._job_dict.pop(url, None)

    async def _download_item(self, media_id: str) -> None:
        try:
            queue_item = self._queue_dict.get(media_id)

            if (
                not queue_item
                or queue_item.status != DownloadStatus.PENDING_DOWNLOADING
            ):
                return

            if not queue_item.download_item:
                queue_item.status = DownloadStatus.FAILED
                queue_item.error = RuntimeError("Missing download item")
                await self._notify_queue_change(media_id)
                return

            queue_item.status = DownloadStatus.DOWNLOADING
            await self._notify_queue_change(media_id)

            try:
                log.debug("Downloading %s", media_id)
                await self.downloader.download(queue_item.download_item)

                queue_item.status = DownloadStatus.COMPLETED
                await self._notify_queue_change(media_id)

            except asyncio.CancelledError:
                queue_item.status = DownloadStatus.FAILED
                queue_item.error = RuntimeError("Download canceled")
                await self._notify_queue_change(media_id)
                raise

            except Exception as e:
                log.exception("Download failed for %s", media_id)
                queue_item.status = DownloadStatus.FAILED
                queue_item.error = e
                await self._notify_queue_change(media_id)

        finally:
            self._job_dict.pop(media_id, None)

    async def shutdown(self) -> None:
        if not self._scheduler.closed:
            await self._scheduler.close()

        self._job_dict.clear()

        for media_id, item in self._queue_dict.items():
            if item.status in ACTIVE_STATUSES:
                item.status = DownloadStatus.FAILED
                item.error = RuntimeError("Download manager was shut down")
                await self._notify_queue_change(media_id)
