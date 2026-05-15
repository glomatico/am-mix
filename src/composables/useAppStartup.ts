import { computed } from "vue";
import { LoadingState } from "./enums";
import { useAppleMusicApi } from "./useAppleMusicApi";
import { useConfigFile } from "./useConfigFile";
import { useDownloadManager } from "./useDownloadManager";
import { createResultRef } from "./utils";

export const useAppStartup = () => {
  const { initialize: initializeConfigFilePyloid, exists } = useConfigFile();
  const { initialize: initializeAppleMusicApiPyloid } = useAppleMusicApi();
  const { initialize: initializeDownloadManagerPyloid } = useDownloadManager();

  const configFileResult = createResultRef();
  const appleMusicApiResult = createResultRef();
  const downloadManagerResult = createResultRef();

  const isInitialized = computed(
    () =>
      configFileResult.value.loadingState === LoadingState.SUCCESS &&
      appleMusicApiResult.value.loadingState === LoadingState.SUCCESS &&
      downloadManagerResult.value.loadingState === LoadingState.SUCCESS,
  );
  const hasError = computed(
    () =>
      configFileResult.value.loadingState === LoadingState.ERROR ||
      appleMusicApiResult.value.loadingState === LoadingState.ERROR ||
      downloadManagerResult.value.loadingState === LoadingState.ERROR,
  );

  const initializeDownloadManager = async () => {
    downloadManagerResult.value.loadingState = LoadingState.LOADING;

    try {
      await initializeDownloadManagerPyloid();
    } catch (error) {
      downloadManagerResult.value.loadingState = LoadingState.ERROR;
      downloadManagerResult.value.errorMessage =
        error instanceof Error ? error.message : String(error);
      console.error("Error loading Download Manager:", error);
      return;
    }

    downloadManagerResult.value.loadingState = LoadingState.SUCCESS;
  };

  const initializeAppleMusicApi = async () => {
    appleMusicApiResult.value.loadingState = LoadingState.LOADING;

    try {
      await initializeAppleMusicApiPyloid();
    } catch (error) {
      appleMusicApiResult.value.loadingState = LoadingState.ERROR;
      appleMusicApiResult.value.errorMessage =
        error instanceof Error ? error.message : String(error);
      console.error("Error loading Apple Music API:", error);
      return;
    }

    appleMusicApiResult.value.loadingState = LoadingState.SUCCESS;
  };

  const initializeConfigFile = async (): Promise<Boolean> => {
    configFileResult.value.loadingState = LoadingState.LOADING;

    let result;

    try {
      await initializeConfigFilePyloid();
      result = await exists();
    } catch (error) {
      configFileResult.value.loadingState = LoadingState.ERROR;
      configFileResult.value.errorMessage =
        error instanceof Error ? error.message : String(error);
      console.error("Error loading config file:", error);
    }

    configFileResult.value.loadingState = LoadingState.SUCCESS;

    return result;
  };

  const initialize = async () => {
    const result = await initializeConfigFile();
    if (
      configFileResult.value.loadingState !== LoadingState.SUCCESS ||
      !result
    ) {
      return;
    }

    await initializeAppleMusicApi();
    if (appleMusicApiResult.value.loadingState !== LoadingState.SUCCESS) {
      return;
    }

    await initializeDownloadManager();
  };

  return {
    configFileResult,
    appleMusicApiResult,
    downloadManagerResult,
    isInitialized,
    hasError,
    initialize,
  };
};
