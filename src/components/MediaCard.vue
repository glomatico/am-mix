<script setup lang="ts">
import { useDownloadManager } from '../composables/useDownloadManager';
import { copyUrl, formatArtworkUrl, formatDuration, getAlbumIdFromUrl } from '../composables/utils';

const props = defineProps<{
  metadata: any;
  artworkSize: number;
  artworkAspectRatio: number;
  index?: number;
}>();

const albumId = getAlbumIdFromUrl(props.metadata.attributes?.url);

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
  <v-card variant="text" @click="handleDownload(metadata.attributes?.url)" :disabled="!metadata.attributes.playParams">
    <div class="pa-2">
      <v-row>
        <v-col cols="12">
          <v-row density="comfortable" align="center">
            <v-col v-if="index !== undefined" cols="auto">
              <v-btn icon variant="text" readonly>
                {{ index }}
              </v-btn>
            </v-col>

            <v-col v-else cols="auto">
              <v-img :src="metadata.attributes?.artwork?.url
                ? formatArtworkUrl(metadata.attributes?.artwork?.url, artworkSize, artworkSize)
                : undefined
                " :alt="`
          ${$t('coverAlt', { title: metadata?.attributes?.name || $t('unknownTitle') })}
        `" :aspect-ratio="artworkAspectRatio" :width="artworkSize" rounded />
            </v-col>

            <v-col style="min-width: 0">
              <v-row align="center">
                <v-col class="overflow-hidden">
                  <h3 class="text-truncate font-weight-bold text-left ma-0 mb-1">
                    {{ metadata.attributes.name }}
                  </h3>

                  <p class="text-truncate text-label-medium text-left ma-0 mb-1">
                    {{ metadata.attributes.artistName }}
                  </p>

                  <p class="text-truncate text-label-medium text-left ma-0">
                    {{ formatDuration(metadata.attributes.durationInMillis) }}
                  </p>
                </v-col>
              </v-row>
            </v-col>

            <v-col cols="auto">
              <v-btn icon size="small" variant="text">
                <v-icon size="small">mdi-dots-vertical</v-icon>

                <v-menu activator="parent">
                  <v-list>
                    <v-list-item prepend-icon="mdi-download" :title="$t('mediaCard.download')"
                      @click="handleDownload(metadata.attributes?.url)" />

                    <v-list-item prepend-icon="mdi-content-copy" :title="$t('mediaCard.copyLink')"
                      @click="copyUrl(metadata)" />

                    <v-list-item v-if="albumId" prepend-icon="mdi-album" :title="$t('mediaCard.viewAlbum')"
                      :to="`/album/${albumId}`" />
                  </v-list>
                </v-menu>
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div>
  </v-card>
</template>
