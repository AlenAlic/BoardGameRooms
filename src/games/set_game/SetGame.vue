<template>
  <v-container v-if="!game.started" class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="auto">
        <v-btn x-large text color="primary" @click="startGame">
          {{ $t("SET.start") }}
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
  <v-container v-else>
    <v-row align="start" justify="space-between">
      <v-col cols="9">
        <template>
          <v-row justify="center" v-for="r in 3" :key="r">
            <v-col cols="auto" v-for="c in cols" :key="`${r - 1}-${c - 1}`">
              <card
                :card="game.cards[getCardIndex(r, c)]"
                @click.native="current_player ? selectCard(game.cards[getCardIndex(r, c)].tag) : null"
                :selected="game.selected_cards.includes(game.cards[getCardIndex(r, c)].tag)"
                :clickable="current_player === current_user.user_id"
                :disabled="current_player !== current_user.user_id"
                :shake="shakeCards.includes(game.cards[getCardIndex(r, c)].tag)"
              />
            </v-col>
          </v-row>
        </template>
      </v-col>
      <v-col cols="3" class="text-center">
        <template v-if="!game.game_over">
          <v-row no-gutters justify="center" class="mb-5">
            <card :remaining-cards="game.remaining_cards" stack>
              <v-row no-gutters class="fill-height" align="center" justify="center">
                <v-col cols="auto">{{ game.remaining_cards }}</v-col>
              </v-row>
            </card>
          </v-row>
          <v-simple-table class="text-start my-5">
            <thead>
              <tr>
                <th>{{ $t("SET.score") }}</th>
                <th />
              </tr>
            </thead>
            <tbody>
              <tr v-for="user_id in Object.keys(game.scores)" :key="user_id">
                <td>{{ playerName(user_id) }}</td>
                <td>{{ game.scores[user_id] }}</td>
              </tr>
            </tbody>
          </v-simple-table>
          <v-btn
            color="primary"
            class="mt-5"
            large
            @click="checkBoard"
            :disabled="!!current_player"
            v-if="current_user.user_id === room.admin"
          >
            {{ $t("SET.no_set") }}
          </v-btn>
        </template>
        <template v-else>
          <v-row justify="center" class="mb-5">
            <v-col class="text-center">
              <div class="display-1 mt-5">
                {{ $t("SET.winners") }}
              </div>
              <div class="title">
                <div class="my-2" v-for="user_id in game.winners" :key="user_id">
                  {{ playerName(user_id) }}
                </div>
              </div>
            </v-col>
          </v-row>
          <v-simple-table class="text-start">
            <thead>
              <tr>
                <th />
                <th>{{ $t("SET.start") }}</th>
                <th>{{ $t("SET.sets") }}</th>
                <th>{{ $t("SET.penalties") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user_id in Object.keys(game.scores)" :key="user_id">
                <td>{{ playerName(user_id) }}</td>
                <td>{{ game.scores[user_id] }}</td>
                <td>{{ game.sets[user_id] }}</td>
                <td>{{ game.scores[user_id] - game.sets[user_id] }}</td>
              </tr>
            </tbody>
          </v-simple-table>
        </template>
      </v-col>
    </v-row>
    <v-row align="center" v-if="!game.game_over">
      <v-col cols="9" class="text-center">
        <template v-if="!current_player">
          <v-btn x-large color="primary" :disabled="!!current_player" @click="callSet">
            SET
          </v-btn>
          <Keypress :key-code="32" event="keyup" @pressed="callSet" />
        </template>
        <div v-else-if="selected_cards.length < 3" class="display-1">
          <div class="mb-2">{{ playerName(current_player) }}</div>
          <div>{{ timer.toFixed(1) }}</div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Card from "./Card";
export default {
  components: {
    Card,
    Keypress: () => import("vue-keypress")
  },
  data() {
    return {
      timer: 0.0,
      shakeCards: []
    };
  },
  computed: {
    game() {
      return this.$store.getters.game;
    },
    current_user() {
      return this.$store.state.user;
    },
    room() {
      return this.$store.state.room;
    },
    cols() {
      return this.game.cards.length / 3;
    },
    current_player() {
      return this.game && this.game.current_player;
    },
    selected_cards() {
      return this.game ? this.game.selected_cards : [];
    }
  },
  sockets: {
    game_message(message) {
      if (message.message_id === "set_shake") {
        this.shakeCards = message.data;
        setTimeout(() => (this.shakeCards = []), 500);
      }
    }
  },
  methods: {
    playerName(user_id) {
      const users = this.game.users.filter(u => u.user_id === user_id);
      return users.length === 1 ? users[0].username : null;
    },
    getCardIndex(row, col) {
      return 3 * (col - 1) + row - 1;
    },
    startGame() {
      const data = {
        room: this.room.id,
        action: "START_GAME"
      };
      this.$socket.client.emit("game_action", data);
    },
    callSet() {
      const data = {
        room: this.room.id,
        action: "CALL_SET",
        data: {
          user_id: this.current_user.user_id
        }
      };
      this.$socket.client.emit("game_action", data);
      this.timer = 6.9;
    },
    selectCard(tag) {
      const data = {
        room: this.room.id,
        action: "SELECT_CARD",
        data: {
          tag: tag
        }
      };
      this.$socket.client.emit("game_action", data);
      if (this.game.selected_cards.length === 2 && !this.game.selected_cards.includes(tag)) {
        this.timer = 2.0;
        setTimeout(() => {
          this.checkSet();
        }, 1000);
      }
    },
    checkBoard() {
      const data = {
        room: this.room.id,
        action: "CHECK_BOARD"
      };
      this.$socket.client.emit("game_action", data);
    },
    noChoiceMade() {
      if (this.selected_cards.length < 3) {
        const data = {
          room: this.room.id,
          action: "NO_CHOICE",
          data: {
            user_id: this.current_user.user_id
          }
        };
        this.$socket.client.emit("game_action", data);
      }
    },
    checkSet() {
      const data = {
        room: this.room.id,
        action: "CHECK_SET"
      };
      this.$socket.client.emit("game_action", data);
    }
  },
  watch: {
    timer: {
      handler(value) {
        if (value > 0) {
          setTimeout(() => {
            this.timer -= 0.1;
          }, 100);
        } else {
          this.noChoiceMade();
        }
      }
    },
    current_player: {
      handler(value) {
        if (!value) this.timer = 0;
      }
    }
  }
};
</script>
