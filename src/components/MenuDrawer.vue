<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const { t } = useI18n();

const visible = defineModel<boolean>('visible');

const menuItems = [
  {
    title: t('menu.home'),
    icon: 'mdi-home',
    path: '/',
  },
  {
    title: t('menu.search'),
    icon: 'mdi-magnify',
    path: '/search',
  },
  {
    title: t('menu.settings'),
    icon: 'mdi-cog',
    path: '/settings',
  },
];

const activeItem = computed(() => {
  const currentPath = route.path;
  const active = menuItems.find(item => {
    return currentPath === item.path || currentPath.startsWith(item.path + '/');
  });
  return active?.path || null;
});
</script>

<template>
  <v-navigation-drawer v-model="visible" :permanent="$vuetify.display.lgAndUp" temporary location="left">
    <v-toolbar :elevation="4" color="surface">
      <v-container>
        <v-row align="center" density="comfortable">
          <v-col cols="auto">
            <v-btn icon="mdi-close" @click="visible = false" variant="text" size="x-small" />
          </v-col>

          <v-col>
            <v-toolbar-title class="font-weight-bold">
              {{ $t("appName") }}
            </v-toolbar-title>
          </v-col>
        </v-row>
      </v-container>
    </v-toolbar>

    <v-list nav :selected="[activeItem]">
      <v-list-item v-for="item in menuItems" :key="item.path" :title="item.title" :prepend-icon="item.icon"
        :value="item.path" @click="router.push(item.path)" />
    </v-list>
  </v-navigation-drawer>
</template>
