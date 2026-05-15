<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import admBadge from "../assets/badges/adm.svg";
import atmosBadge from "../assets/badges/atmos.svg";
import hiresLosslessBadge from "../assets/badges/hires-lossless.svg";
import losslessBadge from "../assets/badges/lossless.svg";
import lossyBadge from "../assets/badges/lossy.svg";
import spatialBadge from "../assets/badges/spatial.svg";

type AlbumBadge = {
  trait: string;
  src: string;
  altKey: string;
};

const BADGE_DEFINITIONS: AlbumBadge[] = [
  { trait: "lossy-stereo", src: lossyBadge, altKey: "collectionBanner.badges.lossy" },
  { trait: "lossless", src: losslessBadge, altKey: "collectionBanner.badges.lossless" },
  {
    trait: "hi-res-lossless",
    src: hiresLosslessBadge,
    altKey: "collectionBanner.badges.hiresLossless",
  },
  { trait: "atmos", src: atmosBadge, altKey: "collectionBanner.badges.atmos" },
  { trait: "adm", src: admBadge, altKey: "collectionBanner.badges.adm" },
  { trait: "spatial", src: spatialBadge, altKey: "collectionBanner.badges.spatial" },
];

const props = defineProps<{
  attributes?: Record<string, unknown>;
}>();

const { t } = useI18n();

const badges = computed(() => {
  if (!props.attributes) {
    return [];
  }

  const traits = [...((props.attributes.audioTraits as string[] | undefined) ?? [])];

  if (props.attributes.isMasteredForItunes) {
    traits.push("adm");
  }

  return BADGE_DEFINITIONS.filter((badge) => traits.includes(badge.trait));
});
</script>

<template>
  <v-row density="compact" v-if="badges.length" class="album-badges">
    <v-col v-for="badge in badges" :key="badge.trait" cols="auto">
      <img :src="badge.src" :alt="t(badge.altKey)" :class="{ 'invert': $vuetify.theme.current.dark }" />
    </v-col>
  </v-row>
</template>

<style scoped>
.invert {
  filter: invert(1);
}
</style>
