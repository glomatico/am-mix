<script setup lang="ts">
import type { Component } from 'vue';
import { computed, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';
import AppStatusContainer from '../components/AppStatusContainer.vue';
import AppTabs from '../components/AppTabs.vue';
import ArtistBanner from '../components/ArtistBanner.vue';
import CollectionCardList from '../components/CollectionCardList.vue';
import MediaCardList from '../components/MediaCardList.vue';
import { useArtist } from '../composables/useArtist';

const route = useRoute();
const { t } = useI18n();

const {
  artistId,
  artistResult,
  artistMediasData,
  initialize,
  createLoadScroll,
  addAllToDownloadQueue,
} = useArtist();

type ArtistMediaKey =
  | 'top-songs'
  | 'music-videos'
  | 'singles'
  | 'full-albums'
  | 'compilation-albums'
  | 'live-albums'
  | 'albums';

const artistTabs: {
  slot: string;
  dataKey: ArtistMediaKey;
  list: Component;
  tabLabelKey: string;
  loadingKey: string;
  errorKey: string;
  emptyKey: string;
}[] = [
  {
    slot: 'topSongs',
    dataKey: 'top-songs',
    list: MediaCardList,
    tabLabelKey: 'artistPage.tabs.topSongs',
    loadingKey: 'artistPage.loading.topSongs',
    errorKey: 'artistPage.error.topSongs',
    emptyKey: 'searchPage.noSongsFound',
  },
  {
    slot: 'musicVideos',
    dataKey: 'music-videos',
    list: MediaCardList,
    tabLabelKey: 'artistPage.tabs.musicVideos',
    loadingKey: 'artistPage.loading.musicVideos',
    errorKey: 'artistPage.error.musicVideos',
    emptyKey: 'searchPage.noMusicVideosFound',
  },
  {
    slot: 'singles',
    dataKey: 'singles',
    list: CollectionCardList,
    tabLabelKey: 'artistPage.tabs.singles',
    loadingKey: 'artistPage.loading.singles',
    errorKey: 'artistPage.error.singles',
    emptyKey: 'searchPage.noAlbumsFound',
  },
  {
    slot: 'mainAlbums',
    dataKey: 'full-albums',
    list: CollectionCardList,
    tabLabelKey: 'artistPage.tabs.mainAlbums',
    loadingKey: 'artistPage.loading.mainAlbums',
    errorKey: 'artistPage.error.mainAlbums',
    emptyKey: 'searchPage.noAlbumsFound',
  },
  {
    slot: 'compilationAlbums',
    dataKey: 'compilation-albums',
    list: CollectionCardList,
    tabLabelKey: 'artistPage.tabs.compilationAlbums',
    loadingKey: 'artistPage.loading.compilationAlbums',
    errorKey: 'artistPage.error.compilationAlbums',
    emptyKey: 'searchPage.noAlbumsFound',
  },
  {
    slot: 'liveAlbums',
    dataKey: 'live-albums',
    list: CollectionCardList,
    tabLabelKey: 'artistPage.tabs.liveAlbums',
    loadingKey: 'artistPage.loading.liveAlbums',
    errorKey: 'artistPage.error.liveAlbums',
    emptyKey: 'searchPage.noAlbumsFound',
  },
  {
    slot: 'allAlbums',
    dataKey: 'albums',
    list: CollectionCardList,
    tabLabelKey: 'artistPage.tabs.allAlbums',
    loadingKey: 'artistPage.loading.allAlbums',
    errorKey: 'artistPage.error.allAlbums',
    emptyKey: 'searchPage.noAlbumsFound',
  },
];

const artistTabLabels = computed(() =>
  Object.fromEntries(artistTabs.map((tab) => [tab.slot, t(tab.tabLabelKey)])),
);

onMounted(async () => {
  artistId.value = route.params.id as string;
  await initialize();
});
</script>

<template>
  <v-container>
    <AppStatusContainer :loading-state="artistResult.loadingState" :loading-title="$t('artistPage.loading.artist')">
      <template #error>
        <v-alert type="error">
          {{ $t('artistPage.error.artist', { message: artistResult.errorMessage }) }}
        </v-alert>
      </template>

      <v-row>
        <v-col cols="12">
          <v-btn icon="mdi-arrow-left" variant="text" @click="$router.back()" />
        </v-col>

        <v-col cols="12">
          <ArtistBanner :metadata="artistResult.result" />
        </v-col>

        <v-col>
          <AppTabs :tabs="artistTabLabels">
            <template v-for="tab in artistTabs" :key="tab.slot" #[tab.slot]>
              <AppStatusContainer
                :empty="!artistMediasData[tab.dataKey].result.length"
                :loading-state="artistMediasData[tab.dataKey].loadingState"
                :loading-title="$t(tab.loadingKey)"
              >
                <template #empty>
                  <v-alert type="info">
                    {{ $t(tab.emptyKey) }}
                  </v-alert>
                </template>

                <template #error>
                  <v-alert type="error">
                    {{ $t(tab.errorKey, { message: artistMediasData[tab.dataKey].errorMessage }) }}
                  </v-alert>
                </template>

                <v-row>
                  <v-col cols="12">
                    <v-btn
                      block
                      variant="outlined"
                      rounded
                      prepend-icon="mdi-download-multiple"
                      @click="addAllToDownloadQueue(tab.dataKey)"
                    >
                      {{ $t('artistPage.downloadAll') }}
                    </v-btn>
                  </v-col>

                  <v-col cols="12">
                    <v-infinite-scroll @load="({ done }) => createLoadScroll(tab.dataKey)({ done })">
                      <component :is="tab.list" :metadatas="artistMediasData[tab.dataKey].result" />
                    </v-infinite-scroll>
                  </v-col>
                </v-row>
              </AppStatusContainer>
            </template>
          </AppTabs>
        </v-col>
      </v-row>
    </AppStatusContainer>
  </v-container>
</template>
