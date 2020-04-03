<template>
  <v-container v-if="!$store.state.user.room" class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-form @submit.prevent="joinRoom" :value="!!validInput">
        <v-card max-width="344">
          <v-card-title>
            {{ $t("home.title") }}
            <v-icon class="ml-2" :color="$socket.connected ? 'success' : 'error'">
              mdi-checkbox-blank-circle
            </v-icon>
          </v-card-title>
          <v-card-text>
            <v-text-field
              v-model="username"
              :label="$t('home.username.label')"
              prepend-icon="mdi-account-circle"
              hide-details
            />
            <v-text-field v-model="room" :label="$t('home.room.label')" prepend-icon="mdi-home" hide-details />
            <v-text-field
              v-model="password"
              :label="$t('home.password.label')"
              prepend-icon="mdi-key"
              type="password"
              :hint="$t('home.password.hint')"
              persistent-hint
            />
            <v-checkbox v-model="join_room" :label="$t('home.existing_room.label')" hide-details></v-checkbox>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text color="primary" type="submit" :disabled="!validInput">
              {{ join_room ? $t("home.join_room") : $t("home.create_room") }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-row>
  </v-container>
  <game v-else-if="$store.getters.game" />
  <lobby v-else />
</template>

<script>
import { retrieveSession, SET_SESSION } from "../store/modules/user";
import { INIT_ROOM, SET_GAME, SET_ROOM_USERS } from "../store/modules/room";
import Lobby from "../components/Lobby";
import Game from "../components/Game";
export default {
  components: { Game, Lobby },
  data() {
    return {
      username: "",
      room: "",
      password: "",
      join_room: false
    };
  },
  created() {
    const session = retrieveSession();
    if (session) {
      this.username = session.username || "";
      this.room = session.room || "";
    }
  },
  computed: {
    validInput() {
      return this.username && this.room;
    }
  },
  sockets: {
    room_created(data) {
      this.$store.dispatch(SET_SESSION, data).then(() => {
        this.$store.dispatch(INIT_ROOM, data.room).then(() => {});
      });
    },
    room_joined(data) {
      this.$store.dispatch(SET_SESSION, data).then(() => {
        this.$store.dispatch(INIT_ROOM, data.room).then(() => {});
      });
    },
    room_user_joined(data) {
      this.$store.dispatch(SET_ROOM_USERS, data.room).then(() => {
        this.$store.commit(SET_GAME, data.room.game);
      });
    },
    room_left(data) {
      this.$store.dispatch(SET_ROOM_USERS, data.room).then(() => {
        this.$store.commit(SET_GAME, data.room.game);
      });
    },
    game_update(game) {
      this.$store.commit(SET_GAME, game);
    }
  },
  methods: {
    joinRoom() {
      let data = {
        username: this.username,
        room: this.room,
        password: this.password
      };
      if (this.join_room) {
        this.$socket.client.emit("join_game_room", data);
      } else {
        this.$socket.client.emit("create_game_room", data);
      }
      this.password = "";
    }
  }
};
</script>
