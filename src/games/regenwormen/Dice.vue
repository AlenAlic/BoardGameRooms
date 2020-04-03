<template>
  <v-card
    class="text-center"
    min-width="3.75rem"
    :class="{ 'disabled not_allowed': disabled, clickable: clickable }"
    :elevation="highlight ? 10 : null"
  >
    <v-card-text class="title">
      <span v-if="placeholder">?</span>
      <span v-else-if="dice.value <= 5">{{ dice.value }}</span>
      <v-icon small color="error" v-else>
        mdi-checkbox-blank-circle
      </v-icon>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    dice: { type: Object, default: () => {} },
    placeholder: { type: Boolean, default: false },
    highlight: { type: Boolean, default: false },
    disabled: { type: Boolean, default: false },
    clickable: { type: Boolean, default: false }
  }
};
</script>

<style scoped lang="scss">
.disabled {
  background: lightgray;
}
</style>
