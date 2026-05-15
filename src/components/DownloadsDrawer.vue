<script setup lang="ts">
import { useDownloadManager } from '../composables/useDownloadManager';
import MediaCardDownloadList from './MediaCardDownloadList.vue';


const visible = defineModel<boolean>("visible");
const { queue, hasErrors, clearQueue, retryFailedItems } = useDownloadManager();
</script>

<template>
  <v-navigation-drawer v-model="visible" temporary :permanent="$vuetify.display.lgAndUp" location="right" width="320">
    <v-toolbar :elevation="4" color="surface">
      <v-container>
        <v-row align="center" density="comfortable">
          <v-col cols="auto">
            <v-btn icon="mdi-close" @click="visible = false" variant="text" size="x-small" />
          </v-col>

          <v-col>
            <v-toolbar-title>
              {{ $t("downloadDrawer.title") }}
            </v-toolbar-title>
          </v-col>
        </v-row>
      </v-container>
    </v-toolbar>

    <v-container>
      <v-row>
        <v-col cols="12">
          <v-btn
            :disabled="queue.size === 0"
            block
            variant="outlined"
            rounded
            prepend-icon="mdi-playlist-remove"
            @click="clearQueue"
          >
            {{ $t("downloadDrawer.clearQueue") }}
          </v-btn>
        </v-col>

        <v-col cols="12">
          <v-btn
            :disabled="!hasErrors"
            block
            variant="outlined"
            rounded
            prepend-icon="mdi-refresh"
            @click="retryFailedItems"
          >
            {{ $t("downloadDrawer.retryFailed") }}
          </v-btn>
        </v-col>

        <v-col cols="12">
          <MediaCardDownloadList />
        </v-col>
      </v-row>
    </v-container>
  </v-navigation-drawer>
</template>
