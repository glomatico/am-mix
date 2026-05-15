import { ref } from "vue";
import { LoadingState } from "./enums";
import { useAppleMusicApi } from "./useAppleMusicApi";
import { createResultRef } from "./utils";
import { useDownloadManager } from "./useDownloadManager";

interface ArtistMedia {
  albums: any;
  ["music-videos"]: any;
  ["full-albums"]: any;
  ["compilation-albums"]: any;
  ["live-albums"]: any;
  ["singles"]: any;
  ["top-songs"]: any;
}

export const useArtist = () => {
  const { getArtist, getExtendedApiData } = useAppleMusicApi();
  const { addToQueue } = useDownloadManager();

  const artistId = ref<string>("");
  const artistResult = createResultRef();
  const artistMedias = ref<ArtistMedia>({
    albums: null,
    ["music-videos"]: null,
    ["full-albums"]: null,
    ["compilation-albums"]: null,
    ["live-albums"]: null,
    ["singles"]: null,
    ["top-songs"]: null,
  });
  const artistMediasData: ArtistMedia = {
    albums: createResultRef(),
    ["music-videos"]: createResultRef(),
    ["full-albums"]: createResultRef(),
    ["compilation-albums"]: createResultRef(),
    ["live-albums"]: createResultRef(),
    ["singles"]: createResultRef(),
    ["top-songs"]: createResultRef(),
  };

  const initialize = async () => {
    artistResult.value.loadingState = LoadingState.LOADING;

    try {
      const result = await getArtist(artistId.value);
      artistResult.value.result = result.data[0];

      for (const key of Object.keys(artistResult.value.result.relationships)) {
        const relationship = artistResult.value.result.relationships?.[key];
        artistMediasData[key as keyof ArtistMedia].result =
          relationship?.data || [];
        artistMedias.value[key as keyof ArtistMedia] = relationship;
        artistMediasData[key as keyof ArtistMedia].loadingState =
          LoadingState.SUCCESS;
      }

      for (const key of Object.keys(artistResult.value.result.views)) {
        const view = artistResult.value.result.views?.[key];
        artistMediasData[key as keyof ArtistMedia].result = view?.data || [];
        artistMedias.value[key as keyof ArtistMedia] = view;
        artistMediasData[key as keyof ArtistMedia].loadingState =
          LoadingState.SUCCESS;
      }
    } catch (error) {
      console.error("Error loading search results:", error);
      artistResult.value.errorMessage =
        error instanceof Error ? error.message : String(error);
      artistResult.value.loadingState = LoadingState.ERROR;
      return;
    }

    artistResult.value.loadingState = LoadingState.SUCCESS;
  };

  const loadMore = async (type: keyof ArtistMedia): Promise<boolean | null> => {
    const currentData = artistMedias.value[type];

    if (!currentData) {
      return false;
    }

    try {
      let response;

      if (currentData.next && currentData.href) {
        response = await getExtendedApiData(currentData.next, currentData.href);
      } else {
        response = null;
      }

      if (response?.data) {
        artistMediasData[type].result.push(...response.data);
        artistMedias.value[type] = response;
        return true;
      }

      return false;
    } catch (error) {
      console.error(`Error loading more ${type} search results:`, error);
      return null;
    }
  };

  const createLoadScroll = (type: keyof ArtistMedia) => {
    return async ({ done }: any) => {
      const result = await loadMore(type);

      if (result === true) {
        done("success");
      } else if (result === false) {
        done("empty");
      } else {
        done("error");
      }
    };
  };

  const addAllToDownloadQueue = async (type: keyof ArtistMedia) => {
    artistMediasData[type].loadingState = LoadingState.LOADING;

    let result = await loadMore(type);
    while (result === true) {
      result = await loadMore(type);
    }

    if (result === null) {
      artistMediasData[type].loadingState = LoadingState.ERROR;
      return;
    }

    artistMediasData[type].loadingState = LoadingState.SUCCESS;

    const items = artistMediasData[type].result;
    await Promise.all(
      items.map((item: any) => addToQueue(item.attributes.url)),
    );
  };

  return {
    artistId,
    artistResult,
    artistMediasData,
    initialize,
    createLoadScroll,
    addAllToDownloadQueue,
  };
};
