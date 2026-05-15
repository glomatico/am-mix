<script setup lang="ts">
import ArtistCard from "./ArtistCard.vue";

defineProps<{
  metadatas: any[];
}>();


</script>

<template>
  <v-list>
    <template v-for="(metadata, index) in metadatas" :key="index">
      <ArtistCard :metadata="metadata" />

      <v-divider v-if="index < metadatas.length - 1" />
    </template>
  </v-list>
</template>
