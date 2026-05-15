<script setup lang="ts">
import MediaCard from "./MediaCard.vue";

defineProps<{
  metadatas: any[];
  appendIndex?: boolean;
}>();


</script>

<template>
  <v-list>
    <template v-for="(metadata, index) in metadatas" :key="index">
      <template v-if="metadata?.type == 'songs'">
        <MediaCard :metadata="metadata" :artwork-size="80" :artwork-aspect-ratio="1"
          :index="appendIndex ? index + 1 : undefined" />
      </template>

      <template v-else>
        <MediaCard :metadata="metadata" :artwork-size="160" :artwork-aspect-ratio="16 / 9"
          :index="appendIndex ? index + 1 : undefined" />
      </template>

      <v-divider v-if="index < metadatas.length - 1" />
    </template>
  </v-list>
</template>
