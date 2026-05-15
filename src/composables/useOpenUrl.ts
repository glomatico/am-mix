import { rpc } from "pyloid-js";

export const useOpenUrl = () => {
  const openUrl = async (url: string, folder: boolean = false) => {
    return await rpc.call("open_url", { url, folder });
  };

  return {
    openUrl,
  };
};
