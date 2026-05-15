<script setup lang="ts">
import { ref } from 'vue';
import { useDownloadManager } from '../composables/useDownloadManager';
import AppSearchBar from './AppSearchBar.vue';
import DownloadsDrawer from './DownloadsDrawer.vue';
import MenuDrawer from './MenuDrawer.vue';

const { isActive } = useDownloadManager();

const isMenuDrawerVisible = ref(false);
const isDownloadsDrawerVisible = ref(false);
</script>

<template>
  <MenuDrawer v-model:visible="isMenuDrawerVisible" />

  <DownloadsDrawer v-model:visible="isDownloadsDrawerVisible" />

  <v-app-bar>
    <v-container>
      <v-row align="center">
        <v-col cols="auto">
          <v-btn icon="mdi-menu" @click="isMenuDrawerVisible = !isMenuDrawerVisible" />
        </v-col>

        <v-col>
          <AppSearchBar />
        </v-col>

        <v-col cols="auto">
          <v-badge :model-value="isActive" color="orange" dot>
            <v-btn icon="mdi-download" @click="isDownloadsDrawerVisible = !isDownloadsDrawerVisible" />
          </v-badge>
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>
