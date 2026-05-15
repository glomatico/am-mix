<script setup lang="ts">
import { useDownloadManager } from '../composables/useDownloadManager';
import { copyUrl, formatArtworkUrl } from '../composables/utils';

defineProps<{
  metadata: any;
}>();

const { addToQueue } = useDownloadManager();

const handleDownload = async (url: string) => {
  try {
    if (!url) {
      console.error("No URL found for this item");
      return;
    }
    await addToQueue(url);
  } catch (error) {
    console.error("Failed to add item to download queue:", error);
  }
};
</script>

<template>
  <v-card variant="text">
    <div class="pa-2">
      <v-row density="comfortable" align="center">
        <v-col cols="auto">
          <v-img :src="metadata.attributes?.artwork?.url
            ? formatArtworkUrl(metadata.attributes?.artwork?.url, 240, 240)
            : undefined
            " :alt="`
          ${$t('coverAlt', { title: metadata?.attributes?.name || $t('unknownTitle') })}
        `" :aspect-ratio="1" :width="240" rounded />
        </v-col>

        <v-col style="min-width: 0">
          <v-row align="center">
            <v-col class="overflow-hidden">
              <h1 class="text-truncate font-weight-bold text-left ma-0 mb-1">
                {{ metadata?.attributes?.name || $t("unknownTitle") }}
              </h1>

              <p v-if="metadata?.attributes?.trackCount" class="text-truncate text-label-medium text-left ma-0 mb-1">
                {{ $t('collectionCard.trackCount', { count: metadata.attributes.trackCount }) }}
              </p>
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="auto">
          <v-btn icon size="small" variant="text">
            <v-icon size="small">mdi-dots-vertical</v-icon>
            <v-menu activator="parent">
              <v-list>
                <v-list-item
                  prepend-icon="mdi-download"
                  :title="$t('mediaCard.download')"
                  @click="handleDownload(metadata.attributes?.url)"
                />

                <v-list-item
                  prepend-icon="mdi-content-copy"
                  :title="$t('mediaCard.copyLink')"
                  @click="copyUrl(metadata)"
                />
              </v-list>
            </v-menu>
          </v-btn>
        </v-col>
      </v-row>
    </div>
  </v-card>
</template>
