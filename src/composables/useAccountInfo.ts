import { LoadingState } from "./enums";
import { useAppleMusicApi } from "./useAppleMusicApi";
import { createResultRef } from "./utils";

export const useAccountInfo = () => {
  const { accountInfo } = useAppleMusicApi();

  const accountInfoResult = createResultRef();

  const initialize = async () => {
    accountInfoResult.value.loadingState = LoadingState.LOADING;

    try {
      accountInfoResult.value.result = await accountInfo();
      accountInfoResult.value.loadingState = LoadingState.SUCCESS;
    } catch (error) {
      console.error("Error fetching account info:", error);
      accountInfoResult.value.errorMessage = "Failed to fetch account info.";
      accountInfoResult.value.loadingState = LoadingState.ERROR;
    }
  };

  return {
    accountInfoResult,
    initialize,
  };
};
