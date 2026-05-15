<script setup lang="ts">
import CollectionCard from "./CollectionCard.vue";

defineProps<{
  metadatas: any[];
}>();


</script>

<template>
  <v-list>
    <template v-for="(metadata, index) in metadatas" :key="index">
      <CollectionCard :metadata="metadata" />

      <v-divider v-if="index < metadatas.length - 1" />
    </template>
  </v-list>
</template>
