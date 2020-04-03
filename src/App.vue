<template>
  <v-app>
    <app-header
      v-if="inRoom"
      @toggleDrawer="toggleDrawer"
      @toggleRightDrawer="toggleRightDrawer"
      @toggleGameMenuDrawer="toggleGameMenuDrawer"
      :breakpoint="breakpoint"
    />

    <v-navigation-drawer v-if="inRoom" v-model="drawer" :clipped="breakpoint" app width="270">
      <app-menu />
    </v-navigation-drawer>

    <v-navigation-drawer v-if="inRoom" v-model="rightDrawer" :clipped="breakpoint" app right ref="chat">
      <app-chat @updated="scrollToBottom" />
    </v-navigation-drawer>

    <v-content>
      <transition name="fade" mode="out-in">
        <router-view></router-view>
      </transition>
    </v-content>

    <app-snackbar />
  </v-app>
</template>

<script>
import AppHeader from "./components/general/AppHeader";
import AppMenu from "./components/general/AppMenu";
import AppSnackbar from "./components/general/AppSnackbar";
import AppChat from "./components/general/AppChat";
import { CLEAR_SESSION, GET_SESSION, retrieveSession } from "./store/modules/user";
export default {
  components: { AppHeader, AppMenu, AppSnackbar, AppChat },
  data() {
    return {
      drawer: this.breakpoint,
      rightDrawer: false,
      gameMenuDrawer: false
    };
  },
  created() {
    this.$store.dispatch(GET_SESSION).then(() => {
      this.$socket.client.emit("check_active_game_room", retrieveSession());
    });
  },
  mounted() {
    this.scrollToBottom();
  },
  sockets: {
    room_reset() {
      this.$store.commit(CLEAR_SESSION);
    }
  },
  computed: {
    inRoom() {
      return !!this.$store.state.user.room;
    },
    breakpoint() {
      return this.$vuetify.breakpoint.lgAndUp;
    }
  },
  methods: {
    toggleDrawer() {
      this.drawer = !this.drawer;
    },
    toggleRightDrawer() {
      this.rightDrawer = !this.rightDrawer;
    },
    toggleGameMenuDrawer() {
      this.gameMenuDrawer = !this.gameMenuDrawer;
    },
    scrollToBottom() {
      let chat = this.$refs.chat;
      if (chat) {
        chat = chat.$el.firstElementChild;
        chat.scrollTop = chat.scrollHeight + 60;
      }
    }
  }
};
</script>

<style src="./assets/css/styles.scss" lang="scss"></style>
