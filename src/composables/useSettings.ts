import { LoadingState } from "./enums";
import { useConfigFile } from "./useConfigFile";
import { createResultRef } from "./utils";

export const useSettings = () => {
  const {
    initialize: initializePyloid,
    getJsonConfig,
    update: updatePyloid,
  } = useConfigFile();

  const settingsResult = createResultRef();
  const updateResult = createResultRef();

  const initialize = async () => {
    settingsResult.value.loadingState = LoadingState.LOADING;

    try {
      await initializePyloid();
      settingsResult.value.result = await getJsonConfig();
    } catch (error) {
      settingsResult.value.loadingState = LoadingState.ERROR;
      settingsResult.value.errorMessage =
        error instanceof Error ? error.message : String(error);
      console.error("Error loading config file:", error);
      return;
    }

    settingsResult.value.loadingState = LoadingState.SUCCESS;
  };

  const update = async (config: any) => {
    updateResult.value.loadingState = LoadingState.LOADING;

    try {
      await updatePyloid(config);
      updateResult.value.loadingState = LoadingState.SUCCESS;
    } catch (error) {
      updateResult.value.loadingState = LoadingState.ERROR;
      updateResult.value.errorMessage =
        error instanceof Error ? error.message : String(error);
      console.error("Error updating config file:", error);
      return;
    }
  };

  return {
    settingsResult,
    updateResult,
    initialize,
    update,
  };
};
