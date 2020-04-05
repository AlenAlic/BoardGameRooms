<template>
  <div class="stacked_icon my-1">
    <v-icon :style="{ opacity: opacity }" :color="color" large>
      {{ shape }}
    </v-icon>
    <v-icon class="stacked_icon__outline" :color="color" large>{{ shape }}-outline</v-icon>
  </div>
</template>

<script>
export default {
  props: {
    opacity: { type: Number, default: 0.2 },
    color: { type: String, default: "secondary" },
    shape: { type: String, default: "mdi-star" }
  }
};
</script>

<style scoped lang="scss">
.stacked_icon {
  .stacked_icon__outline {
    position: absolute;
    left: 32px;
  }
}
</style>
