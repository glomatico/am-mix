<script setup lang="ts">
import { useOpenFileExplorerDialog } from '../composables/useOpenFileExplorerDialog';

const { openFileDialog, openDirectoryDialog } = useOpenFileExplorerDialog();

const filePath = defineModel<string | null>("filePath");

const props = defineProps<{
  label: string;
  filter?: string;
  pickDirectory?: boolean;
  nullable?: boolean;
}>();

const handleClick = async () => {
  const result = props.pickDirectory
    ? await openDirectoryDialog(filePath.value)
    : await openFileDialog(props.filter ?? "*");
  if (result) {
    filePath.value = result;
  }
};
</script>

<template>
  <v-text-field variant="outlined" rounded v-model="filePath" :label="label" hide-details>
    <template #append>
      <v-btn icon="mdi-pencil" variant="text" @click="handleClick" />
      <v-btn v-if="nullable" icon="mdi-close" variant="text" @click="filePath = null" />
    </template>
  </v-text-field>
</template>
