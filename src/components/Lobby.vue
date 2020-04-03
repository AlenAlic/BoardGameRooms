<template>
  <v-container>
    <v-row>
      <v-col>
        <h2 class="text-center">{{ $t("lobby.title") }}</h2>
      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col v-for="game in $store.state.games.available" :key="game.tag">
        <v-card class="mx-auto" max-width="344" width="100%">
          <v-card-title>
            {{ game.name }}
          </v-card-title>
          <v-card-subtitle> {{ game.min_players }}-{{ game.max_players }} {{ $t("lobby.players") }} </v-card-subtitle>
          <v-card-text>
            {{ $t(`${game.tag}.description`) }}
          </v-card-text>
          <v-card-actions v-if="$store.getters.user_id === $store.getters.admin">
            <v-spacer />
            <v-btn
              text
              color="primary"
              @click="setupGame(game)"
              :disabled="$store.state.room.users.length < game.min_players"
            >
              {{ $t("lobby.play") }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <modal
        v-model="setupModal"
        :title="game.name"
        :accept="$t('lobby.create_game.create')"
        @yes="createGame"
        :accept-disabled="users.length < game.min_players || users.length > game.max_players"
      >
        <v-card-subtitle> {{ game.min_players }}-{{ game.max_players }} {{ $t("lobby.players") }} </v-card-subtitle>
        <v-card-text>
          <div>{{ $t("lobby.create_game.text") }}</div>
          <div>{{ users.length }}/{{ game.max_players }} {{ $t("lobby.create_game.selected") }}</div>
          <v-list flat dense>
            <v-list-item-group v-model="users" multiple mandatory :max="game.max_players">
              <v-list-item
                v-for="user in $store.state.room.users"
                :key="user.user_id"
                :value="user.user_id"
                :disabled="user.user_id === $store.state.room.admin"
              >
                <template v-slot:default="{ active, toggle }">
                  <v-list-item-action>
                    <v-checkbox
                      :input-value="active"
                      color="primary"
                      @click="toggle"
                      :disabled="user.user_id === $store.state.room.admin"
                    />
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title>{{ user.username }}</v-list-item-title>
                  </v-list-item-content>
                </template>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card-text>
      </modal>
    </v-row>
  </v-container>
</template>

<script>
import { SET_GAMES_LIST } from "../store/modules/games";
import Modal from "../components/modal/Modal";
import { SET_GAME } from "../store/modules/room";
export default {
  components: { Modal },
  data() {
    return {
      setupModal: false,
      game: {},
      users: []
    };
  },
  created() {
    this.$socket.client.emit("game_get_list");
  },
  sockets: {
    game_list(games) {
      this.$store.commit(SET_GAMES_LIST, games);
    },
    game_new(games) {
      this.$store.commit(SET_GAME, games);
    }
  },
  methods: {
    setupGame(game) {
      this.game = game;
      this.setupModal = true;
      this.users = this.$store.state.room.users.map(u => u.user_id);
    },
    createGame() {
      const data = {
        room: this.$store.state.room.id,
        tag: this.game.tag,
        users: this.users
      };
      this.$socket.client.emit("game_create", data);
    }
  }
};
</script>
