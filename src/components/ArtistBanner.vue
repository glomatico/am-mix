<script setup lang="ts">
import { formatArtworkUrl, copyUrl } from '../composables/utils';

defineProps<{
  metadata: any;
}>();
</script>

<template>
  <v-card variant="text">
    <div class="pa-2">
      <v-row density="comfortable" align="center">
        <v-col cols="auto">
          <v-avatar :image="metadata.attributes?.artwork?.url
            ? formatArtworkUrl(metadata.attributes?.artwork?.url, 240, 240)
            : undefined
            " :alt="`
          ${$t('avatarAlt', { name: metadata.attributes.name })}
        `" :size="240" icon="mdi-account" />
        </v-col>

        <v-col style="min-width: 0">
          <v-row align="center">
            <v-col class="overflow-hidden">
              <h1 class="text-truncate font-weight-bold text-left ma-0">
                {{ metadata.attributes.name }}
              </h1>
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="auto">
          <v-btn icon="mdi-content-copy" size="small" variant="text" @click="copyUrl(metadata)" />
        </v-col>
      </v-row>
    </div>
  </v-card>
</template>
