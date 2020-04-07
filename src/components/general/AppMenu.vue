<template>
  <v-sheet>
    <v-tabs v-model="tab">
      <v-tab>
        <v-icon>mdi-account-multiple</v-icon>
      </v-tab>
      <v-tab>
        <v-icon>mdi-settings</v-icon>
      </v-tab>
      <v-tab>
        <v-icon>mdi-gamepad</v-icon>
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-list>
          <v-list-item v-for="user in $store.state.room.users" :key="user.user_id" active-class="accent" dense>
            <v-list-item-icon>
              <v-icon v-if="user.user_id === $store.state.room.admin">mdi-star</v-icon>
              <v-icon v-else>mdi-account</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ user.username }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-tab-item>
      <v-tab-item>
        <v-list>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                {{ $t("settings.room_capacity") }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ $store.state.room.users.length }} / {{ $store.state.room.settings.max_size }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                {{ $t("settings.password") }}
              </v-list-item-title>
              <v-list-item-subtitle v-if="!!$store.state.room.password">
                {{ $store.state.room.password }}
              </v-list-item-subtitle>
              <v-list-item-subtitle v-else>
                {{ $t("settings.no_password") }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-btn color="primary" @click="leaveRoomModal = true">
                {{ $t("settings.leave_room.btn") }}
              </v-btn>
              <modal
                v-model="leaveRoomModal"
                @yes="leaveRoom"
                :text="$t('settings.leave_room.modal.text')"
                :accept="$t('settings.leave_room.modal.leave')"
                :close="$t('settings.leave_room.modal.stay')"
              />
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-tab-item>
      <v-tab-item>
        <v-list v-if="$store.getters.game">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>
                {{ $t("game_menu.players") }}
              </v-list-item-title>
              <template v-for="user in $store.getters.game.users">
                <v-list-item-subtitle
                  v-if="$store.getters.game && $store.getters.game.active_users.includes(user.user_id)"
                  :key="user.user_id"
                >
                  {{ user.username }}
                </v-list-item-subtitle>
              </template>
            </v-list-item-content>
          </v-list-item>
          <v-list-item v-if="$store.state.user.user_id === $store.state.room.admin">
            <v-list-item-content>
              <v-btn color="primary" @click="stopGameModal = true">
                {{ $t("game_menu.stop_game.btn") }}
              </v-btn>
              <modal
                v-model="stopGameModal"
                @yes="stop_game"
                :text="$t('game_menu.stop_game.modal.text')"
                :accept="$t('game_menu.stop_game.modal.stop')"
                :close="$t('game_menu.stop_game.modal.continue')"
              />
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content v-if="$store.getters.game.active_users.includes($store.state.user.user_id)">
              <v-btn color="primary" @click="leaveGameModal = true">
                {{ $t("game_menu.leave_game.btn") }}
              </v-btn>
              <modal
                v-model="leaveGameModal"
                @yes="leave_game"
                :text="$t('game_menu.leave_game.modal.text')"
                :accept="$t('game_menu.leave_game.modal.leave')"
                :close="$t('game_menu.leave_game.modal.stay')"
              />
            </v-list-item-content>
            <v-list-item-content
              v-else-if="$store.getters.game.users.map(u => u.user_id).includes($store.state.user.user_id)"
            >
              <v-btn color="primary" @click="rejoin_game">
                {{ $t("game_menu.rejoin_game.btn") }}
              </v-btn>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-list v-else>
          <v-list-item>
            <v-list-item-content>
              {{ $t("game_menu.not_available") }}
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-tab-item>
    </v-tabs-items>
  </v-sheet>
</template>

<script>
import Modal from "../../components/modal/Modal";
import { CLEAR_SESSION } from "../../store/modules/user";
export default {
  components: { Modal },
  props: { initialDrawer: null },
  data() {
    return {
      drawer: this.initialDrawer,
      tab: null,
      leaveRoomModal: false,
      stopGameModal: false,
      leaveGameModal: false,
      rejoinGameModal: false
    };
  },
  methods: {
    leaveRoom() {
      this.leave_game_room();
    },
    leave_game_room() {
      let data = {
        user_id: this.$store.state.user.user_id,
        room: this.$store.state.user.room
      };
      this.$socket.client.emit("leave_game_room", data);
      this.$store.commit(CLEAR_SESSION, data);
    },
    stop_game() {
      this.$socket.client.emit("game_stop", this.$store.state.user.room);
    },
    leave_game() {
      let data = {
        user_id: this.$store.state.user.user_id,
        room: this.$store.state.user.room
      };
      this.$socket.client.emit("game_leave", data);
    },
    rejoin_game() {
      let data = {
        user_id: this.$store.state.user.user_id,
        room: this.$store.state.user.room
      };
      this.$socket.client.emit("game_rejoin", data);
    }
  }
};
</script>
