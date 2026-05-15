<script setup lang="ts">
import { onMounted } from 'vue';
import AppStatusContainer from '../components/AppStatusContainer.vue';
import Settings from '../components/Settings.vue';
import { useSettings } from '../composables/useSettings';

const {
  settingsResult,
  initialize,
} = useSettings();

onMounted(async () => {
  await initialize();
});
</script>

<template>
  <v-app>
    <div>
      <v-container>
        <AppStatusContainer :loading-state="settingsResult.loadingState"
          :loading-title="$t('startup.loading.configFile')">
          <template #error>
            <v-alert type="error">
              {{ $t('startup.error.configFile', { message: settingsResult.errorMessage }) }}
            </v-alert>
          </template>

          <v-row>
            <v-col cols="12" align="center">
              <h1 class="ma-0 mb-2">{{ $t('setupPage.title', { appName: $t('appName') }) }}</h1>

              <v-divider thickness="2" />

              <p class="ma-0 mt-2">{{ $t('setupPage.subtitle') }}</p>
            </v-col>

            <v-col cols="12">
              <v-card>
                <v-sheet class="pa-2">
                  <Settings :json-config="settingsResult.result" />
                </v-sheet>
              </v-card>
            </v-col>
          </v-row>
        </AppStatusContainer>
      </v-container>
    </div>
  </v-app>
</template>
