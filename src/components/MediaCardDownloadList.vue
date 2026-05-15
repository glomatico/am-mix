<script setup lang="ts">
import { useDownloadManager } from '../composables/useDownloadManager';
import MediaCardDownload from './MediaCardDownload.vue';

const { queue } = useDownloadManager();

</script>

<template>
  <v-list variant="text">
    <template v-for="(downloadItem, index) in queue.values()" :key="index">
      <MediaCardDownload :downloadItem="downloadItem" />

      <v-divider v-if="index < queue.size - 1" />
    </template>
  </v-list>
</template>
