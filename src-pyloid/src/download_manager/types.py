from dataclasses import dataclass
from enum import Enum
from gamdl.downloader.types import DownloadItem as GamdlDownloadItem


class DownloadStatus(str, Enum):
    PENDING_FETCHING = "pending-fetching"
    FETCHING = "fetching"
    PENDING_DOWNLOADING = "pending-downloading"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class DownloadManagerItem:
    media_id: str
    download_item: GamdlDownloadItem | None
    status: DownloadStatus = DownloadStatus.PENDING_FETCHING
    error: Exception | None = None
