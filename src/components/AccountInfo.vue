<script setup lang="ts">
defineProps<{
  accountInfo: any;
}>();

</script>

<template>
  <v-row>
    <v-col cols="12" align="center">
      <v-avatar size="100" icon="mdi-account" />
    </v-col>

    <v-col cols="12" align="center">
      <v-chip v-if="accountInfo?.meta?.subscription?.active" icon="mdi-account">
        <v-icon icon="mdi-check" start />
        {{ $t('accountInfo.active') }}
      </v-chip>

      <v-chip v-else icon="mdi-account">
        <v-icon icon="mdi-close" start />
        {{ $t('accountInfo.inactive') }}
      </v-chip>
    </v-col>

    <v-col cols="12" align="center">
      <p class="ma-0 mb-2">
        {{ $t('accountInfo.storefront', { storefront: accountInfo?.meta?.subscription?.storefront }) }}
      </p>
      <p class="ma-0">
        {{ $t('accountInfo.restrictions', {
          restrictions: accountInfo?.data?.[0]?.attributes?.restrictions?.length
            ? $t('accountInfo.restricted')
            : $t('accountInfo.unrestricted'),
        }) }}
      </p>
    </v-col>
  </v-row>
</template>