<template>
  <v-card
    class="text-center"
    :class="{ placeholder: placeholder || !active, clickable: clickable, not_allowed: !active }"
    :elevation="selectable ? 10 : null"
  >
    <v-card-text class="title" :class="{ placeholder_text: placeholder }">
      {{ placeholder ? "xx" : tile.value }}
    </v-card-text>
    <v-divider />
    <v-card-text class="title error--text" :class="{ placeholder_text: placeholder }">
      {{ placeholder ? "x" : tile.worms }}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    tile: { type: Object, default: () => {} },
    placeholder: { type: Boolean, default: false },
    selectable: { type: Boolean, default: false },
    clickable: { type: Boolean, default: false },
    active: { type: Boolean, default: true }
  }
};
</script>

<style scoped lang="scss">
.placeholder {
  background: lightgray;
}
.v-application {
  .v-card__text {
    .placeholder_text {
      color: lightgrey !important;
    }
  }
}
</style>
