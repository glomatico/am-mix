<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import AppStatusContainer from '../components/AppStatusContainer.vue';
import CollectionBanner from '../components/CollectionBanner.vue';
import MediaCardList from '../components/MediaCardList.vue';
import { usePlaylist } from '../composables/usePlaylist';

const route = useRoute();

const {
  playlistId,
  playlistResult,
  playlistTracksData,
  initialize,
  loadScroll,
} = usePlaylist();

onMounted(async () => {
  playlistId.value = route.params.id as string;
  await initialize();
});
</script>

<template>
  <v-container>
    <AppStatusContainer :loading-state="playlistResult.loadingState" :loading-title="$t('playlist.loading')">
      <template #error>
        <v-alert type="error">
          {{ $t('playlist.error', { message: playlistResult.errorMessage }) }}
        </v-alert>
      </template>

      <v-row>
        <v-col cols="12">
          <v-btn icon="mdi-arrow-left" @click="$router.back()" variant="text" />
        </v-col>

        <v-col cols="12">
          <CollectionBanner :metadata="playlistResult.result" />
        </v-col>

        <v-col cols="12">
          <v-infinite-scroll @load="loadScroll" class="overflow-x-hidden">
            <MediaCardList :metadatas="playlistTracksData" append-index />
          </v-infinite-scroll>
        </v-col>
      </v-row>
    </AppStatusContainer>
  </v-container>
</template>
