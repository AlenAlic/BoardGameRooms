<template>
  <v-container>
    <v-row align="start" justify="center" class="my-5">
      <v-col cols="auto" v-for="t in board_tiles" :key="t.value">
        <tile
          :tile="t"
          @click.native="
            (t.value === player_dice_score || t.value === next_highest_tile) &&
            player_take_tile_allowed &&
            t.active &&
            isMyTurn
              ? takeTile('board', t.value)
              : null
          "
          :selectable="
            (t.value === player_dice_score || t.value === next_highest_tile) && player_take_tile_allowed && t.active
          "
          :clickable="
            (t.value === player_dice_score || t.value === next_highest_tile) &&
              player_take_tile_allowed &&
              t.active &&
              isMyTurn
          "
          :active="t.active"
        />
      </v-col>
    </v-row>
    <template v-if="game_active">
      <v-row align="center" class="my-5">
        <!--        <v-col cols="3">-->
        <!--          <v-card flat class="fill-height">-->
        <!--            <v-card-text>-->
        <!--              <v-row align="start" justify="start" no-gutters>-->
        <!--                <template v-if="player_tiles.length > 0">-->
        <!--                  <v-col cols="auto" v-for="t in player_tiles" :key="t.value">-->
        <!--                    <tile :tile="t" class="mx-2 my-2" />-->
        <!--                  </v-col>-->
        <!--                </template>-->
        <!--                <v-col cols="auto" v-else>-->
        <!--                  <tile class="mx-2 my-2" placeholder />-->
        <!--                </v-col>-->
        <!--              </v-row>-->
        <!--            </v-card-text>-->
        <!--          </v-card>-->
        <!--        </v-col>-->
        <v-col cols="8">
          <v-card flat>
            <v-card-text>
              <v-row align="center" justify="center" v-if="game.dice_thrown">
                <v-col cols="auto" v-for="(d, idx) in board.dice" :key="idx">
                  <dice
                    :dice="d"
                    @click.native="canDiceBeSelected(d.value) ? setDice(d.value) : null"
                    :highlight="dice === d.value"
                    :disabled="!canDiceBeSelected(d.value)"
                    :clickable="canDiceBeSelected(d.value)"
                  />
                </v-col>
              </v-row>
              <v-row align="center" justify="center" v-else>
                <v-col cols="auto" v-for="(d, idx) in board.dice" :key="idx">
                  <dice placeholder />
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions v-if="isMyTurn && game_active">
              <v-spacer />
              <v-btn v-if="!game.dice_thrown && board.dice.length > 0" text color="primary" @click="throwDice">
                {{ $t("RWM.throw_dice") }}
              </v-btn>
              <v-btn
                v-else-if="game.dice_thrown && !game.turn_over"
                text
                color="primary"
                @click="chooseDice"
                :disabled="dice === 0"
              >
                {{ $t("RWM.grab_dice") }}
              </v-btn>
              <v-btn v-else-if="game.turn_over" text color="primary" @click="endTurn">
                {{ $t("RWM.end_turn") }}
              </v-btn>
              <v-spacer />
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="4">
          <v-card class="fill-height" flat>
            <v-card-text>
              <v-row class="fill-height" align="center" justify="center">
                <v-col cols="auto" v-for="(d, idx) in player_dice" :key="idx">
                  <dice :dice="d" />
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-text class="text-center" v-if="player_dice.length">
              <span>{{ $t("RWM.total_score") }} {{ player_dice_score }}</span>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row v-if="game.started" justify="center" class="mt-5">
        <v-col v-for="player_id in game.order" :key="player_id">
          <v-card flat>
            <v-card-title class="flex_text--center" :class="{ 'primary--text': player_id === game.current_player }">
              {{ game.players[player_id].name }}
            </v-card-title>
            <v-card-text>
              <v-row no-gutters justify="center">
                <v-col cols="auto" v-if="game.players[player_id].tiles.length > 0">
                  <tile v-if="player_id === current_player.player_id" :tile="player_last_tile(player_id)" />
                  <tile
                    v-else
                    :tile="player_last_tile(player_id)"
                    @click.native="
                      player_last_tile(player_id).value === player_dice_score && player_take_tile_allowed && isMyTurn
                        ? takeTile(player_id, player_last_tile(player_id).value)
                        : null
                    "
                    :selectable="player_last_tile(player_id).value === player_dice_score && player_take_tile_allowed"
                    :clickable="
                      player_last_tile(player_id).value === player_dice_score && player_take_tile_allowed && isMyTurn
                    "
                  />
                </v-col>
                <v-col cols="auto" v-else>
                  <tile placeholder />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row justify="center" v-else-if="current_user.user_id === room.admin">
        <v-btn color="primary" large @click="startGame">
          {{ $t("RWM.start_game") }}
        </v-btn>
      </v-row>
    </template>
    <template v-else-if="!game_active">
      <v-row justify="center">
        <v-col class="text-center">
          <div class="display-1 mt-5">
            {{ $t("RWM.winner") }}
          </div>
          <div class="title">
            {{ `${game.players[game.winner].name} (${game.scores[game.winner]})` }}
          </div>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col v-for="player_id in Object.keys(game.scores)" :key="player_id">
          <v-card flat>
            <v-card-title class="flex_text--center">
              {{ `${game.players[player_id].name} (${game.scores[player_id]})` }}
            </v-card-title>
            <v-card-text>
              <v-row no-gutters justify="center">
                <template v-if="game.players[player_id].tiles.length > 0">
                  <v-col cols="auto" v-for="t in game.players[player_id].tiles" :key="t.value">
                    <tile :tile="t" class="mx-2 my-2" />
                  </v-col>
                </template>
                <v-col cols="auto" v-else>
                  <tile placeholder />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script>
import Tile from "./Tile";
import Dice from "./Dice";
export default {
  components: { Dice, Tile },
  data() {
    return {
      dice: 0,
      tile: 0,
      tile_source: "board"
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
    board() {
      return this.game.board;
    },
    board_tiles() {
      return this.board.tiles;
    },
    current_player() {
      return this.game.current_player ? this.game.players[this.game.current_player] : {};
    },
    isMyTurn() {
      return this.current_user.user_id === this.current_player.player_id;
    },
    player_tiles() {
      return this.game.players[this.current_user.user_id] ? this.game.players[this.current_user.user_id].tiles : [];
    },
    player_dice() {
      return this.game.players[this.current_player.player_id]
        ? this.game.players[this.current_player.player_id].dice
        : [];
    },
    player_dice_score() {
      return this.player_dice.reduce((total, dice) => {
        return total + dice.points;
      }, 0);
    },
    next_highest_tile() {
      let board_tiles = this.board.tiles.filter(t => t.value <= this.player_dice_score && t.active).map(t => t.value);
      let player_tiles = this.game.order
        .filter(player_id => player_id !== this.current_player.player_id)
        .map(player_id => this.player_last_tile(player_id))
        .filter(tile => !!tile)
        .map(tile => tile.value)
        .filter(value => value === this.player_dice_score);
      return board_tiles.includes(this.player_dice_score)
        ? this.player_dice_score
        : Math.max(...board_tiles, ...player_tiles);
    },
    player_take_tile_allowed() {
      return this.player_dice.filter(dice => dice.value === 6).length > 0 && this.dice === 0 && !this.game.turn_over;
    },
    game_active() {
      return this.board.tiles.filter(tile => tile.active).length > 0;
    }
  },
  methods: {
    canDiceBeSelected(value) {
      return this.player_dice.filter(dice => dice.value === value).length === 0;
    },
    setDice(value) {
      if (this.isMyTurn && this.canDiceBeSelected(value)) {
        this.dice = value;
      }
    },
    player_last_tile(player_id) {
      return this.game.players[player_id].tiles[this.game.players[player_id].tiles.length - 1];
    },
    startGame() {
      const data = {
        room: this.room.id,
        action: "START",
        data: {
          players: this.room.users
        }
      };
      this.$socket.client.emit("game_action", data);
    },
    throwDice() {
      const data = {
        room: this.room.id,
        action: "THROW_DICE"
      };
      this.$socket.client.emit("game_action", data);
    },
    chooseDice() {
      const data = {
        room: this.room.id,
        action: "CHOOSE_DICE",
        data: {
          user_id: this.current_user.user_id,
          value: this.dice
        }
      };
      this.$socket.client.emit("game_action", data);
      this.dice = 0;
    },
    takeTile(player_id, value) {
      if (this.isMyTurn && !this.game.turn_over) {
        const data = {
          room: this.room.id,
          action: "TAKE_TILE",
          data: {
            user_id: this.current_player.player_id,
            player_id: player_id,
            value: value
          }
        };
        this.$socket.client.emit("game_action", data);
      }
    },
    endTurn() {
      const data = {
        room: this.room.id,
        action: "END_TURN"
      };
      this.$socket.client.emit("game_action", data);
      this.dice = 0;
    }
  }
};
</script>
