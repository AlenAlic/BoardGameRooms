<template>
  <v-card
    class="text-center fill-height px-8 py-4 card"
    :elevation="elevation"
    :flat="placeholder"
    :class="{ clickable: clickable, not_allowed: disabled, shake: shake }"
  >
    <v-row no-gutters class="fill-height" align="center" justify="center">
      <v-col v-if="!placeholder && !stack">
        <div v-for="n in card.number" :key="n">
          <v-icon :style="{ opacity: opacity }" :color="color" large class="my-1" v-if="card.fill !== 0.5">
            {{ shape }}
          </v-icon>
          <stacked-icon v-else :opacity="opacity" :shape="shape" :color="color" />
        </div>
      </v-col>
      <!--      <div v-else class="title">{{ remainingCards }}</div>-->
    </v-row>
  </v-card>
</template>

<script>
import StackedIcon from "./StackedIcon";
const COLORS = {
  red: "error",
  blue: "info",
  green: "success"
};
const FILLED_SHAPES = {
  circle: "mdi-checkbox-blank-circle",
  diamond: "mdi-cards-diamond",
  square: "mdi-square"
};
const EMPTY_SHAPES = {
  circle: "mdi-checkbox-blank-circle-outline",
  diamond: "mdi-cards-diamond-outline",
  square: "mdi-square-outline"
};
export default {
  components: { StackedIcon },
  props: {
    card: { type: Object, default: () => {} },
    selected: { type: Boolean, default: false },
    clickable: { type: Boolean, default: false },
    disabled: { type: Boolean, default: false },
    stack: { type: Boolean, default: false },
    remainingCards: { type: Number, default: 0 },
    shake: { type: Boolean, default: false }
  },
  computed: {
    color() {
      return COLORS[this.card.color];
    },
    shape() {
      if (this.card.fill) return FILLED_SHAPES[this.card.shape];
      else return EMPTY_SHAPES[this.card.shape];
    },
    opacity() {
      return this.card.fill === 0 || this.card.fill === 1 ? 1 : 0.25;
    },
    placeholder() {
      return this.card && this.card.placeholder;
    },
    elevation() {
      if (this.stack) {
        return this.remainingCards / 3;
      } else {
        return this.selected ? 10 : null;
      }
    }
  }
};
</script>

<style scoped lang="scss">
.card {
  width: 100px;
  height: 164px;
}
.shake {
  animation: shake 0.5s;
  animation-iteration-count: infinite;
}
@keyframes shake {
  0% {
    transform: translate(1px, 1px) rotate(0deg);
  }
  10% {
    transform: translate(-1px, -2px) rotate(-1deg);
  }
  20% {
    transform: translate(-3px, 0px) rotate(1deg);
  }
  30% {
    transform: translate(3px, 2px) rotate(0deg);
  }
  40% {
    transform: translate(1px, -1px) rotate(1deg);
  }
  50% {
    transform: translate(-1px, 2px) rotate(-1deg);
  }
  60% {
    transform: translate(-3px, 1px) rotate(0deg);
  }
  70% {
    transform: translate(3px, 1px) rotate(-1deg);
  }
  80% {
    transform: translate(-1px, -1px) rotate(1deg);
  }
  90% {
    transform: translate(1px, 2px) rotate(0deg);
  }
  100% {
    transform: translate(1px, -2px) rotate(-1deg);
  }
}
</style>
