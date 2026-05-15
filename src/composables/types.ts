import { Ref } from "vue";
import { LoadingState } from "./enums";

export interface ResultRefInterface {
  loadingState: LoadingState;
  errorMessage?: string;
  result?: any;
}

export type ResultRef = Ref<ResultRefInterface>;
