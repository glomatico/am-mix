<script setup lang="ts">
import { ref } from 'vue';
import { LoadingState } from '../composables/enums';
import { useSettings } from '../composables/useSettings';
import FileDialogField from './FileDialogField.vue';
import SettingsSection from './SettingsSection.vue';

const { updateResult, update } = useSettings();

const props = defineProps<{
  jsonConfig: any;
}>();

const newJsonConfig = ref({ ...props.jsonConfig });

const handleSave = async () => {
  await update(newJsonConfig.value);
  if (updateResult.value.loadingState === LoadingState.SUCCESS) {
    window.location.href = '/';
  }
};
</script>

<template>
  <v-row>
    <v-col cols="12">
      <v-card variant="text" :disabled="updateResult.loadingState === LoadingState.LOADING">
        <v-row>
          <SettingsSection title-key="settings.sections.general" />

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.max_concurrent_downloads" type="number"
              hide-details :label="$t('settings.application.maxConcurrentDownloads')" />
          </v-col>

          <SettingsSection title-key="settings.sections.appleMusic" />

          <v-col cols="12" md="6">
            <v-radio-group v-model="newJsonConfig.api_method" :label="$t('settings.api.method.title')">
              <v-radio :label="$t('settings.api.method.wrapper')" value="wrapper" />
              <v-radio :label="$t('settings.api.method.cookies')" value="cookies" />
              <v-radio :label="$t('settings.api.method.mediaUserToken')" value="media-user-token" />
            </v-radio-group>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-if="newJsonConfig.api_method === 'wrapper'"
              v-model="newJsonConfig.wrapper_account_url" hide-details
              :label="$t('settings.api.wrapper_account_url')" />

            <v-text-field variant="outlined" rounded v-else-if="newJsonConfig.api_method === 'media-user-token'"
              v-model="newJsonConfig.media_user_token" hide-details :label="$t('settings.api.method.mediaUserToken')" />

            <FileDialogField v-else v-model:file-path="newJsonConfig.cookies" :label="$t('settings.api.cookies')"
              filter="*.txt" />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.language" hide-details
              :label="$t('settings.api.language')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.wrapper_m3u8_ip" hide-details
              :label="$t('settings.baseInterface.wrapperM3u8Ip')" />
          </v-col>

          <v-col cols="12" md="6">
            <FileDialogField v-model:file-path="newJsonConfig.wvd" :label="$t('settings.baseInterface.wvd')"
              filter="*.wvd" nullable />
          </v-col>

          <SettingsSection title-key="settings.sections.output" />

          <v-col cols="12" md="6">
            <FileDialogField v-model:file-path="newJsonConfig.output" pick-directory
              :label="$t('settings.baseDownloader.output')" />
          </v-col>

          <v-col cols="12" md="6">
            <FileDialogField v-model:file-path="newJsonConfig.temp" pick-directory
              :label="$t('settings.baseDownloader.temp')" />
          </v-col>

          <v-col cols="12" md="6">
            <FileDialogField v-model:file-path="newJsonConfig.nm3u8dlre" :label="$t('settings.baseDownloader.nm3u8dlre')"
              filter="*" />
          </v-col>

          <v-col cols="12" md="6">
            <FileDialogField v-model:file-path="newJsonConfig.mp4decrypt"
              :label="$t('settings.baseDownloader.mp4decrypt')" filter="*" />
          </v-col>

          <v-col cols="12" md="6">
            <FileDialogField v-model:file-path="newJsonConfig.ffmpeg" :label="$t('settings.baseDownloader.ffmpeg')"
              filter="*" />
          </v-col>

          <v-col cols="12" md="6">
            <FileDialogField v-model:file-path="newJsonConfig.mp4box" :label="$t('settings.baseDownloader.mp4box')"
              filter="*" />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.wrapper_decrypt_ip" clearable hide-details
              :label="$t('settings.baseDownloader.wrapperDecryptIp')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-radio-group v-model="newJsonConfig.download_mode"
              :label="$t('settings.baseDownloader.downloadMode.title')">
              <v-radio :label="$t('settings.baseDownloader.downloadMode.ytdlp')" value="ytdlp" />
              <v-radio :label="$t('settings.baseDownloader.downloadMode.nm3u8dlre')" value="nm3u8dlre" />
            </v-radio-group>
          </v-col>

          <v-col cols="12" md="6">
            <v-combobox variant="outlined" rounded v-model="newJsonConfig.exclude_tags" multiple chips clearable
              hide-details :label="$t('settings.baseDownloader.excludeTags')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.truncate" type="number" hide-details
              :label="$t('settings.baseDownloader.truncate')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-switch v-model="newJsonConfig.overwrite" :label="$t('settings.downloader.overwrite')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-switch v-model="newJsonConfig.save_playlist" :label="$t('settings.downloader.savePlaylist')" />
          </v-col>

          <SettingsSection title-key="settings.sections.folderTemplates" />

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.album_folder_template" hide-details
              :label="$t('settings.baseDownloader.albumFolderTemplate')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.compilation_folder_template" hide-details
              :label="$t('settings.baseDownloader.compilationFolderTemplate')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.no_album_folder_template" hide-details
              :label="$t('settings.baseDownloader.noAlbumFolderTemplate')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.playlist_folder_template" hide-details
              :label="$t('settings.baseDownloader.playlistFolderTemplate')" />
          </v-col>

          <SettingsSection title-key="settings.sections.fileTemplates" />

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.single_disc_file_template" hide-details
              :label="$t('settings.baseDownloader.singleDiscFileTemplate')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.multi_disc_file_template" hide-details
              :label="$t('settings.baseDownloader.multiDiscFileTemplate')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.no_album_file_template" hide-details
              :label="$t('settings.baseDownloader.noAlbumFileTemplate')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.playlist_file_template" hide-details
              :label="$t('settings.baseDownloader.playlistFileTemplate')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.date_tag_template" hide-details
              :label="$t('settings.baseDownloader.dateTagTemplate')" />
          </v-col>

          <SettingsSection title-key="settings.sections.cover" />

          <v-col cols="12" md="6">
            <v-radio-group v-model="newJsonConfig.cover_format" :label="$t('settings.baseInterface.coverFormat.title')">
              <v-radio :label="'jpg'" value="jpg" />
              <v-radio :label="'png'" value="png" />
              <v-radio :label="'raw'" value="raw" />
            </v-radio-group>
          </v-col>

          <v-col cols="12" md="6">
            <v-text-field variant="outlined" rounded v-model="newJsonConfig.cover_size" type="number" hide-details
              :label="$t('settings.baseInterface.coverSize')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-switch v-model="newJsonConfig.save_cover" :label="$t('settings.downloader.saveCover')" />
          </v-col>

          <SettingsSection title-key="settings.sections.song" />

          <v-col cols="12" md="6">
            <v-radio-group v-model="newJsonConfig.synced_lyrics_format"
              :label="$t('settings.baseInterface.syncedLyricsFormat.title')">
              <v-radio :label="'lrc'" value="lrc" />
              <v-radio :label="'srt'" value="srt" />
              <v-radio :label="'ttml'" value="ttml" />
            </v-radio-group>
          </v-col>

          <v-col cols="12" md="6">
            <v-combobox variant="outlined" rounded v-model="newJsonConfig.song_codec" multiple chips clearable
              hide-details :label="$t('settings.baseInterface.songCodec')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-switch v-model="newJsonConfig.use_album_date" :label="$t('settings.baseInterface.useAlbumDate')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-switch v-model="newJsonConfig.synced_lyrics_only"
              :label="$t('settings.baseInterface.syncedLyricsOnly')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-switch v-model="newJsonConfig.no_synced_lyrics" :label="$t('settings.baseInterface.noSyncedLyrics')" />
          </v-col>

          <SettingsSection title-key="settings.sections.musicVideo" />

          <v-col cols="12" md="6">
            <v-radio-group v-model="newJsonConfig.music_video_resolution"
              :label="$t('settings.musicVideoInterface.musicVideoResolution.title')">
              <v-radio :label="'240p'" value="240p" />
              <v-radio :label="'360p'" value="360p" />
              <v-radio :label="'480p'" value="480p" />
              <v-radio :label="'540p'" value="540p" />
              <v-radio :label="'720p'" value="720p" />
              <v-radio :label="'1080p'" value="1080p" />
              <v-radio :label="'1440p'" value="1440p" />
              <v-radio :label="'2160p'" value="2160p" />
            </v-radio-group>
          </v-col>

          <v-col cols="12" md="6">
            <v-combobox variant="outlined" rounded v-model="newJsonConfig.music_video_codec" multiple chips clearable
              hide-details :label="$t('settings.musicVideoInterface.musicVideoCodec')" />
          </v-col>

          <v-col cols="12" md="6">
            <v-radio-group v-model="newJsonConfig.music_video_remux_mode"
              :label="$t('settings.musicVideoDownloader.musicVideoRemuxMode.title')">
              <v-radio :label="$t('settings.musicVideoDownloader.musicVideoRemuxMode.ffmpeg')" value="ffmpeg" />
              <v-radio :label="$t('settings.musicVideoDownloader.musicVideoRemuxMode.mp4box')" value="mp4box" />
            </v-radio-group>
          </v-col>

          <v-col cols="12" md="6">
            <v-radio-group v-model="newJsonConfig.music_video_remux_format"
              :label="$t('settings.musicVideoDownloader.musicVideoRemuxFormat.title')">
              <v-radio :label="$t('settings.musicVideoDownloader.musicVideoRemuxFormat.mp4')" value="mp4" />
              <v-radio :label="$t('settings.musicVideoDownloader.musicVideoRemuxFormat.m4v')" value="m4v" />
            </v-radio-group>
          </v-col>

          <SettingsSection title-key="settings.sections.uploadedVideo" />

          <v-col cols="12" md="6">
            <v-radio-group v-model="newJsonConfig.uploaded_video_quality"
              :label="$t('settings.uploadedVideoInterface.uploadedVideoQuality.title')">
              <v-radio :label="$t('settings.uploadedVideoInterface.uploadedVideoQuality.best')" value="best" />
              <v-radio :label="$t('settings.uploadedVideoInterface.uploadedVideoQuality.ask')" value="ask" />
            </v-radio-group>
          </v-col>
        </v-row>
      </v-card>
    </v-col>

    <v-col cols="12" align="center" :loading="updateResult.loadingState === LoadingState.LOADING">
      <v-btn @click="handleSave" variant="outlined" rounded>
        {{ $t("settings.saveConfigFile") }}
      </v-btn>
    </v-col>

    <v-col v-if="updateResult.loadingState === LoadingState.ERROR" cols="12">
      <v-alert type="error">
        {{ `${$t('settings.error.saveConfigFile', { message: updateResult.errorMessage })}` }}
      </v-alert>
    </v-col>
  </v-row>
</template>
