<template>
  <v-app-bar dark app :clipped-left="breakpoint" :clipped-right="breakpoint" color="primary">
    <v-app-bar-nav-icon @click.stop="$emit('toggleDrawer')" />

    <v-toolbar-title v-if="breakpoint">{{ $t("header.title") }}</v-toolbar-title>

    <v-spacer />

    <v-toolbar-title>
      <span>{{ $store.state.user.room }}</span>
      <span v-if="!!$store.getters.game"> - {{ $store.state.room.game.name }}</span>
    </v-toolbar-title>

    <v-spacer />

    <v-icon @click.stop="$emit('toggleRightDrawer')">
      mdi-forum
    </v-icon>
  </v-app-bar>
</template>

<script>
export default {
  props: {
    breakpoint: { type: Boolean, default: false }
  }
};
</script>
