import { ref } from "vue";
import { LoadingState } from "./enums";
import { ResultRef, ResultRefInterface } from "./types";

export const createResultRef = (): ResultRef => {
  return ref<ResultRefInterface>({
    loadingState: LoadingState.IDLE,
  });
};

export const formatDuration = (durationMs: number): string => {
  const totalSeconds = Math.floor(durationMs / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
};

export const formatArtworkUrl = (
  url: string,
  width: number,
  height: number,
): string => {
  return url.replace("{w}", width.toString()).replace("{h}", height.toString());
};

export const getAlbumIdFromUrl = (url: string): string | null => {
  // Extract the primary numeric ID from Apple Music album URLs that include a track ID
  // e.g., "https://music.apple.com/de/album/bad/559334659?i=559334751" -> "559334659"
  const match = url.match(/\/album\/[^/]+\/(\d+)\?i=/);
  return match?.[1] || null;
};

export const copyUrl = (metadata: any) => {
  navigator.clipboard.writeText(metadata.attributes.url);
};
