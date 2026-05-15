<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useDownloadManager } from '../composables/useDownloadManager';

const router = useRouter();

const { addToQueue } = useDownloadManager();

const query = ref('');

const handleSearch = () => {
  const queryTrimmed = query.value.trim();
  if (queryTrimmed.startsWith('https://music.apple.com')) {
    addToQueue(queryTrimmed);
    query.value = '';
  } else if (queryTrimmed) {
    router.push(`/search/${encodeURIComponent(queryTrimmed)}`);
  }
};
</script>

<template>
  <v-text-field v-model="query" rounded :placeholder="$t('searchBar.placeholder')" hide-details variant="outlined"
    density="compact" @keyup.enter="handleSearch" />
</template>
