<script lang="ts" setup>
import { computed, ref } from 'vue';

const props = defineProps<{
  tabs: Record<string, string>,
}>();

const tabKeys = computed(() => Object.keys(props.tabs));
const tab = ref<string>(tabKeys.value[0]!);
</script>

<template>
  <v-row>
    <v-col cols="12">
      <v-tabs v-model="tab" align-tabs="center">
        <v-tab class="text-none" v-for="tabKey in tabKeys" :key="tabKey" :value="tabKey">
          {{ tabs[tabKey] }}
        </v-tab>
      </v-tabs>

      <v-divider thickness="2" />
    </v-col>

    <v-col cols="12">
      <v-tabs-window v-model="tab">
        <v-tabs-window-item v-for="tabKey in tabKeys" :key="tabKey" :value="tabKey">
          <slot :name="tabKey" />
        </v-tabs-window-item>
      </v-tabs-window>
    </v-col>
  </v-row>
</template>
