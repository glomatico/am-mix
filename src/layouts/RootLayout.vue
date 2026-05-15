<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AppBar from '../components/AppBar.vue';
import AppStatusContainer from '../components/AppStatusContainer.vue';
import { LoadingState } from '../composables/enums';
import { useAppStartup } from '../composables/useAppStartup';

const router = useRouter();

const {
  configFileResult,
  appleMusicApiResult,
  downloadManagerResult,
  isInitialized,
  hasError,
  initialize,
} = useAppStartup();

onMounted(async () => {
  await initialize();

  if (appleMusicApiResult.value.loadingState === LoadingState.IDLE) {
    router.push('/setup');
  }
});
</script>

<template>
  <v-app>
    <div>
      <v-container v-if="!isInitialized">
        <v-row>
          <v-col cols="12">
            <AppStatusContainer :loading-state="configFileResult.loadingState"
              :loading-title="$t('startup.loading.configFile')">
              <template #error>
                <v-alert type="error">
                  {{ $t('startup.error.configFile', { message: configFileResult.errorMessage }) }}
                </v-alert>
              </template>

              <AppStatusContainer :loading-state="appleMusicApiResult.loadingState"
                :loading-title="$t('startup.loading.appleMusicApi')">
                <template #error>
                  <v-alert type="error">
                    {{ $t('startup.error.appleMusicApi', { message: appleMusicApiResult.errorMessage }) }}
                  </v-alert>
                </template>

                <AppStatusContainer :loading-state="downloadManagerResult.loadingState"
                  :loading-title="$t('startup.loading.downloadManager')">
                  <template #error>
                    <v-alert type="error">
                      {{ $t('startup.error.downloadManager', { message: downloadManagerResult.errorMessage }) }}
                    </v-alert>
                  </template>
                </AppStatusContainer>
              </AppStatusContainer>
            </AppStatusContainer>
          </v-col>

          <v-col v-if="hasError" cols="12" align="center">
            <v-btn to="/setup" variant="outlined" rounded
              :disabled="configFileResult.loadingState !== LoadingState.SUCCESS">
              {{ $t('startup.goToSetup') }}
            </v-btn>
          </v-col>
        </v-row>
      </v-container>

      <template v-else>
        <AppBar />

        <v-main>
          <RouterView />
        </v-main>
      </template>
    </div>
  </v-app>
</template>
