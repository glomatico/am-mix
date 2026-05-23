<script setup lang="ts">
import { onMounted } from 'vue';
import Settings from '../components/Settings.vue';
import { LoadingState } from '../composables/enums';
import { useSettings } from '../composables/useSettings';
import AccountInfo from '../components/AccountInfo.vue';
import { useAccountInfo } from '../composables/useAccountInfo';

const {
  settingsResult,
  initialize: initializeSettings,
} = useSettings();

const {
  accountInfoResult,
  initialize: initializeAccountInfo,
} = useAccountInfo();

onMounted(async () => {
  await initializeSettings();
  await initializeAccountInfo();
});
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="ma-0 mb-2">{{ $t('accountInfo.title') }}</h1>

        <v-divider />
      </v-col>

      <v-col cols="12">
        <AccountInfo v-if="accountInfoResult.loadingState === LoadingState.SUCCESS"
          :account-info="accountInfoResult.result" />
      </v-col>

      <v-col cols="12">
        <h1 class="ma-0 mb-2">{{ $t('menu.settings') }}</h1>

        <v-divider />
      </v-col>

      <v-col cols="12">
        <Settings v-if="settingsResult.loadingState === LoadingState.SUCCESS" :json-config="settingsResult.result" />
      </v-col>
    </v-row>
  </v-container>
</template>
