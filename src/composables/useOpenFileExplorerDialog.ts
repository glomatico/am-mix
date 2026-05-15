import { rpc } from "pyloid-js";

export const useOpenFileExplorerDialog = () => {
  const openFileDialog = async (filter: string) => {
    return await rpc.call("open_file_dialog", { filter });
  };

  const openDirectoryDialog = async (initialDir?: string | null) => {
    const payload =
      initialDir != null && initialDir !== "" ? { dir: initialDir } : {};
    return (await rpc.call("select_directory_dialog", payload)) as
      | string
      | null
      | undefined;
  };

  return {
    openFileDialog,
    openDirectoryDialog,
  };
};
