import { rpc } from "pyloid-js";

export const useConfigFile = () => {
  const initialize = async (ignoreError: boolean = false) => {
    await rpc.call("initialize_config_file", { ignore_error: ignoreError });
  };

  const exists = async () => {
    return await rpc.call("config_file_exists");
  };

  const getJsonConfig = async () => {
    return await rpc.call("config_file_get_json_config");
  };

  const update = async (update: any) => {
    await rpc.call("config_file_update", { update });
  };

  const getVersion = async () => {
    return await rpc.call("get_version");
  };

  return {
    initialize,
    exists,
    getJsonConfig,
    update,
    getVersion,
  };
};
