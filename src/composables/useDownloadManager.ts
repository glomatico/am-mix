import { rpc, event } from "pyloid-js";
import { computed, ref } from "vue";

const queue = ref<Map<string, any>>(new Map());

let isListening = false;
let isInitialized = false;

const startListening = () => {
  if (isListening) return;

  isListening = true;

  event.listen("download_manager_queue_update", (update: any) => {
    console.log("download_manager_queue_update", update);

    const newQueue = new Map(queue.value);

    if (update.delete) {
      newQueue.delete(update.item.media_id);
    } else {
      newQueue.set(update.item.media_id, update.item);
    }

    queue.value = newQueue;
  });
};

export const useDownloadManager = () => {
  startListening();

  const hasErrors = computed(() => {
    return [...queue.value.values()].some((item) => item.status === "failed");
  });
  const isActive = computed(() => {
    return [...queue.value.values()].some((item) =>
      [
        "pending-fetching",
        "fetching",
        "pending-downloading",
        "downloading",
      ].includes(item.status),
    );
  });

  const initialize = async () => {
    if (isInitialized) return;

    isInitialized = true;

    await rpc.call("initialize_apple_music_interface");
    await rpc.call("initialize_apple_music_downloader");
    await rpc.call("initialize_download_manager");
  };

  const addToQueue = async (url: string) => {
    await rpc.call("download_manager_add_to_queue", { url });
  };

  const retryItem = async (itemId: string) => {
    await rpc.call("download_manager_retry_item", { item_id: itemId });
  };

  const clearQueue = async () => {
    await rpc.call("download_manager_clear_queue");
  };

  const retryFailedItems = async () => {
    const failedIds = [...queue.value.entries()]
      .filter(([, item]) => item.status === "failed")
      .map(([key]) => key);

    for (const mediaId of failedIds) {
      await retryItem(mediaId);
    }
  };

  const cancelItem = async (itemId: string) => {
    await rpc.call("download_manager_cancel_item", { item_id: itemId });
  };

  return {
    queue,
    hasErrors,
    isActive,
    initialize,
    addToQueue,
    retryItem,
    clearQueue,
    retryFailedItems,
    cancelItem,
  };
};
