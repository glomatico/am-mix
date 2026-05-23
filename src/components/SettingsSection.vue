<script setup lang="ts">
defineProps<{
  titleKey: string;
}>();
</script>

<template>
  <v-col cols="12">
    <h2 class="font-weight-bold ma-0 mb-2">
      {{ $t(titleKey) }}
    </h2>
    <v-divider />
  </v-col>
</template>
