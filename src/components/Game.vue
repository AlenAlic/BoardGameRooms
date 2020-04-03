<template>
  <guess-dice-throw v-if="tag === 'GDT'" />
  <regenwormen v-else-if="tag === 'RWM'" />
</template>

<script>
import GuessDiceThrow from "../games/guess_dice_throw/GuessDiceThrow";
import Regenwormen from "../games/regenwormen/Regenwormen";
export default {
  components: { GuessDiceThrow, Regenwormen },
  computed: {
    tag() {
      return this.$store.getters.game.tag;
    }
  }
};
</script>
