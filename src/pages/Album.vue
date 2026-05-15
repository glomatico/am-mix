<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import AppStatusContainer from '../components/AppStatusContainer.vue';
import CollectionBanner from '../components/CollectionBanner.vue';
import MediaCardList from '../components/MediaCardList.vue';
import { useAlbum } from '../composables/useAlbum';

const route = useRoute();

const { albumId, albumResult, initialize } = useAlbum();

onMounted(async () => {
  albumId.value = route.params.id as string;
  await initialize();
});
</script>

<template>
  <v-container>
    <AppStatusContainer :loading-state="albumResult.loadingState" :loading-title="$t('album.loading')">
      <template #error>
        <v-alert type="error">
          {{ $t('album.error', { message: albumResult.errorMessage }) }}
        </v-alert>
      </template>

      <v-row>
        <v-col cols="12">
          <v-btn icon="mdi-arrow-left" @click="$router.back()" variant="text" />
        </v-col>

        <v-col cols="12">
          <CollectionBanner :metadata="albumResult.result" />
        </v-col>

        <v-col cols="12">
          <MediaCardList :metadatas="albumResult.result?.relationships.tracks.data" append-index />
        </v-col>
      </v-row>
    </AppStatusContainer>
  </v-container>
</template>
