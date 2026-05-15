import { ref } from "vue";
import { LoadingState } from "./enums";
import { useAppleMusicApi } from "./useAppleMusicApi";
import { createResultRef } from "./utils";

export const useAlbum = () => {
  const { getAlbum } = useAppleMusicApi();

  const albumId = ref("");
  const albumResult = createResultRef();

  const initialize = async () => {
    albumResult.value.loadingState = LoadingState.LOADING;

    try {
      const result = await getAlbum(albumId.value);
      albumResult.value.result = result.data[0];
    } catch (error) {
      console.error("Error loading album:", error);
      albumResult.value.loadingState = LoadingState.ERROR;
      albumResult.value.errorMessage =
        error instanceof Error ? error.message : String(error);
    }

    albumResult.value.loadingState = LoadingState.SUCCESS;
  };

  return {
    albumId,
    albumResult,
    initialize,
  };
};
