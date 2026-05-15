<script setup lang="ts">
import { LoadingState } from '../composables/enums';

const props = defineProps<{
  loadingTitle?: string;
  loadingState?: LoadingState;
  empty?: boolean;
}>();
</script>

<template>
  <v-row>
    <template v-if="props.loadingState === LoadingState.IDLE" />

    <v-col v-else-if="props.loadingState === LoadingState.LOADING" align="center" cols="12">
      <v-row>
        <v-col cols="12">
          <p class="text-center ma-0">
            {{
              props.loadingTitle || $t('loading.default')
            }}
          </p>
        </v-col>

        <v-col cols="12">
          <v-progress-linear indeterminate />
        </v-col>
      </v-row>
    </v-col>

    <v-col v-else-if="props.loadingState === LoadingState.ERROR" cols="12">
      <slot name="error" />
    </v-col>

    <v-col v-else-if="props.empty" cols="12">
      <slot name="empty" />
    </v-col>

    <v-col v-else cols="12">
      <slot />
    </v-col>
  </v-row>
</template>
