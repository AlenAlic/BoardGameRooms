<template>
  <v-container>
    <v-row align="start">
      <v-col cols="12">
        <v-card class="text-center">
          <v-card-text>
            <v-row align="start" justify="center" no-gutters>
              <v-col cols="auto" v-for="user in game.users" :key="user.user_id">
                <v-card class="mx-3">
                  <v-card-text>
                    <div class="title text-center">{{ user.username }}</div>
                    <span v-if="!!game.guesses[user.user_id]">
                      {{ game.guesses[user.user_id] }}
                    </span>
                    <span v-else>No guess yet</span>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
          <template v-if="!game.throw">
            <template v-if="game.active_users.includes(current_user.user_id)">
              <v-card-text>
                <div class="title text-center">My guess</div>
              </v-card-text>
              <v-card-text>
                <v-btn
                  v-for="n in 6"
                  :key="n"
                  class="mx-3 my-3"
                  color="primary"
                  large
                  @click="sendGuess(n)"
                  :disabled="!!game.throw"
                >
                  {{ n }}
                </v-btn>
              </v-card-text>
            </template>
          </template>
          <template v-else>
            <v-card-text>
              <div class="title">Dice throw</div>
              <div>{{ game.throw }}</div>
            </v-card-text>
            <v-card-text>
              <div class="title">Winner(s)</div>
              <template v-if="winners.length">
                <div v-for="user in winners" :key="user.user_id">
                  {{ user.username }}
                </div>
              </template>
              <div v-else>
                No winners
              </div>
            </v-card-text>
          </template>
          <v-card-actions v-if="current_user.user_id === room.admin">
            <v-spacer />
            <v-btn v-if="!game.throw" color="primary" large :disabled="!canThrowDice" @click="throwDice">
              Throw Dice
            </v-btn>
            <v-btn v-else color="primary" large @click="newGame">
              New game
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      guess: this.$store.getters.game.guesses[this.$store.state.user.user_id] || null
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
    winners() {
      const winning_ids = Object.keys(this.game.guesses).filter(id => this.game.guesses[id] === this.game.throw);
      return this.game.users.filter(user => winning_ids.includes(user.user_id));
    },
    canThrowDice() {
      const activeUserIds = [...this.game.active_users].sort();
      const guessesIds = Object.keys(this.game.guesses)
        .filter(id => activeUserIds.includes(id))
        .sort();
      return JSON.stringify(guessesIds) === JSON.stringify(activeUserIds);
    }
  },
  methods: {
    sendGuess(guess) {
      const data = {
        room: this.room.id,
        action: "GUESS",
        data: {
          user_id: this.current_user.user_id,
          guess: guess
        }
      };
      this.$socket.client.emit("game_action", data);
    },
    throwDice() {
      const data = {
        room: this.room.id,
        action: "THROW_DICE",
        data: null
      };
      this.$socket.client.emit("game_action", data);
    },
    newGame() {
      const data = {
        room: this.room.id,
        action: "NEW_GAME",
        data: null
      };
      this.$socket.client.emit("game_action", data);
    }
  }
};
</script>
