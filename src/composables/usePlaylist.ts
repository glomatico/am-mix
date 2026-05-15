import { ref } from "vue";
import { LoadingState } from "./enums";
import { useAppleMusicApi } from "./useAppleMusicApi";
import { createResultRef } from "./utils";

export const usePlaylist = () => {
  const { getPlaylist, getExtendedApiData } = useAppleMusicApi();

  const playlistId = ref("");
  const playlistResult = createResultRef();
  const playlistTracks = ref<any>(null);
  const playlistTracksData = ref<any[]>([]);

  const initialize = async () => {
    if (!playlistId.value.trim()) {
      return;
    }

    playlistResult.value.loadingState = LoadingState.LOADING;

    try {
      const response = await getPlaylist(playlistId.value);
      playlistResult.value.result = response.data[0];
      playlistTracks.value = response.data[0].relationships?.tracks || null;
      playlistTracksData.value =
        response.data[0].relationships?.tracks?.data || [];
    } catch (error) {
      console.error("Error loading playlist:", error);
      playlistResult.value.loadingState = LoadingState.ERROR;
      playlistResult.value.errorMessage =
        error instanceof Error ? error.message : String(error);
    }

    playlistResult.value.loadingState = LoadingState.SUCCESS;
  };

  const loadMore = async (): Promise<boolean | null> => {
    if (!playlistTracks.value) {
      return false;
    }

    try {
      let response;

      if (playlistTracks.value.next && playlistTracks.value.ref) {
        response = await getExtendedApiData(
          playlistTracks.value.next,
          playlistTracks.value.href,
        );
      } else {
        response = null;
      }

      if (response?.data?.length) {
        playlistTracksData.value.push(...response.data);
        playlistTracks.value = response;
        return true;
      }

      return false;
    } catch (error) {
      console.error("Error loading more playlist tracks:", error);
      return null;
    }
  };

  const loadScroll = async ({ done }: any) => {
    const result = await loadMore();

    if (result === true) {
      done("success");
    } else if (result === false) {
      done("empty");
    } else {
      done("error");
    }
  };

  return {
    playlistId,
    playlistResult,
    playlistTracksData,
    initialize,
    loadScroll,
  };
};
