import { ref } from "vue";
import { LoadingState } from "./enums";
import { useAppleMusicApi } from "./useAppleMusicApi";
import { createResultRef } from "./utils";

interface SearchResults {
  songs: any;
  "music-videos": any;
  albums: any;
  playlists: any;
  artists: any;
}

export const useSearch = () => {
  const { getSearchResults, getExtendedApiData } = useAppleMusicApi();

  const query = ref<string>("");
  const searchResult = createResultRef();
  const searchResults = {
    songs: null as any,
    "music-videos": null as any,
    albums: null as any,
    playlists: null as any,
    artists: null as any,
  };
  const searchResultsData: SearchResults = {
    songs: createResultRef(),
    "music-videos": createResultRef(),
    albums: createResultRef(),
    playlists: createResultRef(),
    artists: createResultRef(),
  };

  const initialize = async () => {
    if (!query.value.trim()) {
      return;
    }

    searchResult.value.loadingState = LoadingState.LOADING;

    try {
      const response = await getSearchResults(query.value);
      searchResult.value.result = response.results;

      for (const key of Object.keys(searchResultsData)) {
        searchResults[key as keyof SearchResults] = response.results?.[key];
        searchResultsData[key as keyof SearchResults].value.result =
          response.results?.[key]?.data || [];
      }
    } catch (error) {
      console.error("Error loading search results:", error);
      searchResult.value.errorMessage =
        error instanceof Error ? error.message : String(error);
      searchResult.value.loadingState = LoadingState.ERROR;
      return;
    }

    searchResult.value.loadingState = LoadingState.SUCCESS;
  };

  const loadMore = async (
    type: keyof SearchResults,
  ): Promise<boolean | null> => {
    const currentData = searchResults[type];

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

      if (response?.results?.[type]?.data?.length) {
        searchResults[type] = response.results[type];
        searchResultsData[type].value.result.push(
          ...response.results[type].data,
        );
        return true;
      }

      return false;
    } catch (error) {
      console.error(`Error loading more ${type} search results:`, error);
      return null;
    }
  };

  const createLoadScroll = (type: keyof SearchResults) => {
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

  return {
    query,
    searchResult,
    searchResultsData,
    initialize,
    createLoadScroll,
  };
};
