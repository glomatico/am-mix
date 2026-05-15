import { createRouter, createWebHistory } from "vue-router";
import RootLayout from "./layouts/RootLayout.vue";
import Album from "./pages/Album.vue";
import NotFound from "./pages/NotFound.vue";
import Playlist from "./pages/Playlist.vue";
import Search from "./pages/Search.vue";
import Settings from "./pages/Settings.vue";
import Setup from "./pages/Setup.vue";
import Artist from "./pages/Artist.vue";
import Root from "./pages/Root.vue";

const routes = [
  {
    path: "/",
    component: RootLayout,
    children: [
      {
        path: "",
        component: Root,
      },
      {
        path: "search/:query",
        component: Search,
      },
      {
        path: "search",
        component: Search,
      },
      {
        path: "settings",
        component: Settings,
      },
      {
        path: "album/:id",
        component: Album,
      },
      {
        path: "playlist/:id",
        component: Playlist,
      },
      {
        path: "artist/:id",
        component: Artist,
      },
      {
        path: ":pathMatch(.*)*",
        component: NotFound,
      },
    ],
  },
  {
    path: "/setup",
    component: Setup,
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
