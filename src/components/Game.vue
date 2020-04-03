<template>
  <guess-dice-throw v-if="tag === 'GDT'" />
</template>

<script>
import GuessDiceThrow from "../games/guess_dice_throw/GuessDiceThrow";
export default {
  components: { GuessDiceThrow },
  computed: {
    tag() {
      return this.$store.getters.game.tag;
    }
  }
};
</script>
