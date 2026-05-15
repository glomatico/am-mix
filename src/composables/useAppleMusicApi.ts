import { rpc } from "pyloid-js";

export const useAppleMusicApi = () => {
  const initialize = async () => {
    await rpc.call("initialize_apple_music_api");
  };

  const getSearchResults = async (term: string, offset: number = 0) => {
    return await rpc.call("apple_music_api_get_search_results", {
      term,
      offset,
    });
  };

  const getExtendedApiData = async (nextUri: string, hrefUri: string) => {
    return await rpc.call("apple_music_api_get_extended_api_data", {
      next_uri: nextUri,
      href_uri: hrefUri,
    });
  };

  const getAlbum = async (albumId: string) => {
    return await rpc.call("apple_music_api_get_album", {
      album_id: albumId,
    });
  };

  const getPlaylist = async (playlistId: string) => {
    return await rpc.call("apple_music_api_get_playlist", {
      playlist_id: playlistId,
    });
  };

  const getArtist = async (artistId: string) => {
    return await rpc.call("apple_music_api_get_artist", {
      artist_id: artistId,
    });
  };

  return {
    initialize,
    getSearchResults,
    getExtendedApiData,
    getAlbum,
    getPlaylist,
    getArtist,
  };
};
