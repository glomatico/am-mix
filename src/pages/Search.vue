<script lang="ts" setup>
import type { Component } from 'vue';
import { computed, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import AppStatusContainer from '../components/AppStatusContainer.vue';
import AppTabs from '../components/AppTabs.vue';
import ArtistCardList from '../components/ArtistCardList.vue';
import CollectionCardList from '../components/CollectionCardList.vue';
import MediaCardList from '../components/MediaCardList.vue';
import { useSearch } from '../composables/useSearch';

const router = useRouter();
const { t } = useI18n();
const {
  query,
  searchResult,
  searchResultsData,
  initialize,
  createLoadScroll,
} = useSearch();

const routeQuery = computed(() => (router.currentRoute.value.params.query as string) || '');

watch(
  routeQuery,
  (newQuery) => {
    query.value = newQuery;
    if (newQuery) {
      initialize();
    }
  },
  { immediate: true },
);

type SearchDataKey = 'songs' | 'music-videos' | 'albums' | 'playlists' | 'artists';

const searchTabs: {
  slot: string;
  dataKey: SearchDataKey;
  list: Component;
  tabLabelKey: string;
  emptyKey: string;
}[] = [
  {
    slot: 'songs',
    dataKey: 'songs',
    list: MediaCardList,
    tabLabelKey: 'searchPage.tabs.songs',
    emptyKey: 'searchPage.noSongsFound',
  },
  {
    slot: 'musicVideos',
    dataKey: 'music-videos',
    list: MediaCardList,
    tabLabelKey: 'searchPage.tabs.musicVideos',
    emptyKey: 'searchPage.noMusicVideosFound',
  },
  {
    slot: 'albums',
    dataKey: 'albums',
    list: CollectionCardList,
    tabLabelKey: 'searchPage.tabs.albums',
    emptyKey: 'searchPage.noAlbumsFound',
  },
  {
    slot: 'playlists',
    dataKey: 'playlists',
    list: CollectionCardList,
    tabLabelKey: 'searchPage.tabs.playlists',
    emptyKey: 'searchPage.noPlaylistsFound',
  },
  {
    slot: 'artists',
    dataKey: 'artists',
    list: ArtistCardList,
    tabLabelKey: 'searchPage.tabs.artists',
    emptyKey: 'searchPage.noArtistsFound',
  },
];

const searchTabLabels = computed(() =>
  Object.fromEntries(searchTabs.map((tab) => [tab.slot, t(tab.tabLabelKey)])),
);
</script>

<template>
  <v-container>
    <v-row v-if="!routeQuery">
      <v-col cols="12" align="center">
        <v-icon size="120"> mdi-magnify </v-icon>

        <p class="font-weight-bold text-display-small ma-0 mb-2 mt-2">
          {{ $t('searchPage.title') }}
        </p>

        <p class="ma-0">
          {{ $t('searchPage.subtitle') }}
        </p>
      </v-col>
    </v-row>

    <AppStatusContainer v-else :loading-state="searchResult.loadingState" :loading-title="$t('searchPage.loading')">
      <template #error>
        <v-alert type="error">
          {{ $t('searchPage.error', { message: searchResult.errorMessage }) }}
        </v-alert>
      </template>

      <AppTabs :tabs="searchTabLabels">
        <template v-for="tab in searchTabs" :key="tab.slot" #[tab.slot]>
          <AppStatusContainer :empty="!searchResultsData[tab.dataKey].value.result?.length">
            <template #empty>
              <v-alert type="info">
                {{ $t(tab.emptyKey) }}
              </v-alert>
            </template>

            <v-infinite-scroll
              class="overflow-x-hidden"
              @load="({ done }) => createLoadScroll(tab.dataKey)({ done })"
            >
              <component :is="tab.list" :metadatas="searchResultsData[tab.dataKey].value.result" />
            </v-infinite-scroll>
          </AppStatusContainer>
        </template>
      </AppTabs>
    </AppStatusContainer>
  </v-container>
</template>
