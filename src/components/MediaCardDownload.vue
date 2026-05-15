<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useDownloadManager } from '../composables/useDownloadManager';
import { useOpenUrl } from '../composables/useOpenUrl';
import { formatArtworkUrl } from '../composables/utils';

type DownloadStatus =
  | 'pending-fetching'
  | 'fetching'
  | 'pending-downloading'
  | 'downloading'
  | 'completed'
  | 'failed';

const props = defineProps<{
  downloadItem: any;
}>();

const { t } = useI18n();
const { retryItem, cancelItem } = useDownloadManager();
const { openUrl } = useOpenUrl();

const statusMap: Record<DownloadStatus, { text: string; icon: string }> = {
  'pending-fetching': {
    text: t('downloadItem.pendingFetching'),
    icon: 'mdi-clock-outline',
  },
  'pending-downloading': {
    text: t('downloadItem.pendingDownloading'),
    icon: 'mdi-clock-outline',
  },
  fetching: {
    text: t('downloadItem.fetching'),
    icon: 'mdi-cloud-download',
  },
  downloading: {
    text: t('downloadItem.downloading'),
    icon: 'mdi-download',
  },
  completed: {
    text: t('downloadItem.completed'),
    icon: 'mdi-check',
  },
  failed: {
    text: t('downloadItem.failed'),
    icon: 'mdi-close',
  },
};

const statusInfo = computed(() => {
  return statusMap[props.downloadItem.status as DownloadStatus] ?? {
    text: props.downloadItem.status,
    icon: 'mdi-help-circle-outline',
  };
});
const canOpen = computed(() => {
  return props.downloadItem.media_final_path && props.downloadItem.status === 'completed';
});
</script>

<template>
  <v-card variant="text">
    <v-sheet class="pa-2">
      <v-row density="comfortable" align="center">
        <v-col style="min-width: 0">
          <v-row density="comfortable" align="center">
            <v-col cols="auto">
              <v-avatar :image="downloadItem.media_cover
                ? formatArtworkUrl(downloadItem.media_cover, 40, 40)
                : undefined
                " :alt="$t('coverAlt', {
                  title: downloadItem.media_title || $t('unknownTitle'),
                })" :size="40" rounded />
            </v-col>

            <v-col style="min-width: 0">
              <p class="text-truncate font-weight-bold text-left ma-0 mb-2">
                {{ downloadItem.media_title || $t('unknownTitle') }}
              </p>

              <p class="text-truncate text-label-medium text-left ma-0">
                {{ downloadItem.media_artist || $t('unknownArtist') }}
              </p>
            </v-col>

            <v-col cols="12">
              <p class="text-truncate text-label-medium text-left ma-0 mb-2">
                <v-icon :icon="statusInfo.icon" size="small" />
                {{ statusInfo.text }}
              </p>

              <p v-if="downloadItem.error_message" class="text-truncate text-label-medium text-left ma-0">
                <v-tooltip :text="downloadItem.error_message">
                  <template #activator="{ props }">
                    <span v-bind="props">{{ downloadItem.error_message }}</span>
                  </template>
                </v-tooltip>
              </p>
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="auto">
          <v-btn icon size="x-small" variant="text">
            <v-icon size="x-small">mdi-dots-vertical</v-icon>

            <v-menu activator="parent">
              <v-list>
                <v-list-item
                  :disabled="downloadItem.status !== 'failed'"
                  prepend-icon="mdi-reload"
                  :title="$t('downloadItem.retry')"
                  @click="retryItem(downloadItem.media_id)"
                />

                <v-list-item
                  :disabled="!['pending-fetching', 'pending-downloading'].includes(downloadItem.status)"
                  prepend-icon="mdi-cancel"
                  :title="$t('downloadItem.cancel')"
                  @click="cancelItem(downloadItem.media_id)"
                />

                <v-list-item
                  :disabled="!canOpen"
                  prepend-icon="mdi-play"
                  :title="$t('downloadItem.play')"
                  @click="openUrl(downloadItem.media_final_path)"
                />

                <v-list-item
                  :disabled="!canOpen"
                  prepend-icon="mdi-folder-open"
                  :title="$t('downloadItem.openFolder')"
                  @click="openUrl(downloadItem.media_final_path, true)"
                />
              </v-list>
            </v-menu>
          </v-btn>
        </v-col>
      </v-row>
    </v-sheet>
  </v-card>
</template>
