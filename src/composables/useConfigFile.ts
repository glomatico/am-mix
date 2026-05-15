import { rpc } from "pyloid-js";

export const useConfigFile = () => {
  const initialize = async () => {
    await rpc.call("initialize_config_file");
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

  return {
    initialize,
    exists,
    getJsonConfig,
    update,
  };
};
