<template>
  <guess-dice-throw v-if="tag === 'GDT'" />
  <regenwormen v-else-if="tag === 'RWM'" />
  <set-game v-else-if="tag === 'SET'" />
</template>

<script>
import GuessDiceThrow from "../games/guess_dice_throw/GuessDiceThrow";
import Regenwormen from "../games/regenwormen/Regenwormen";
import SetGame from "../games/set_game/SetGame";
export default {
  components: { SetGame, GuessDiceThrow, Regenwormen },
  computed: {
    tag() {
      return this.$store.getters.game.tag;
    }
  }
};
</script>
