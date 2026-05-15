<script setup lang="ts">
import { onMounted } from 'vue';
import Settings from '../components/Settings.vue';
import { LoadingState } from '../composables/enums';
import { useSettings } from '../composables/useSettings';

const {
  settingsResult,
  initialize,
} = useSettings();

onMounted(async () => {
  await initialize();
});
</script>

<template>
  <v-container>
    <Settings v-if="settingsResult.loadingState === LoadingState.SUCCESS" :json-config="settingsResult.result" />
  </v-container>
</template>
