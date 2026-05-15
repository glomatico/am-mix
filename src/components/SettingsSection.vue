<script setup lang="ts">
defineProps<{
  titleKey: string;
}>();
</script>

<template>
  <v-col cols="12">
    <p class="font-weight-bold text-headline-small ma-0 mb-2">
      {{ $t(titleKey) }}
    </p>
    <v-divider />
  </v-col>
</template>
