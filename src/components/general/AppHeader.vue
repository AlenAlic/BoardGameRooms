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

    <template v-if="showLoadingDice">
      <v-icon @click="diceModal = true" class="mr-5">
        mdi-star
      </v-icon>
      <modal v-model="diceModal">
        <loading-dice />
      </modal>
    </template>

    <v-icon @click.stop="$emit('toggleRightDrawer')">
      mdi-forum
    </v-icon>
  </v-app-bar>
</template>

<script>
import Modal from "../modal/Modal";
import LoadingDice from "../easter_eggs/LoadingDice";
export default {
  components: { Modal, LoadingDice },
  props: {
    breakpoint: { type: Boolean, default: false }
  },
  data() {
    return {
      diceModal: false
    };
  },
  computed: {
    showLoadingDice() {
      const names = ["Alen", "Fi", "Fii", "Fiii", "Fiiii", "Fiiiii", "Fiiiiii", "Fiiiiiii", "Fiiiiiiii"];
      return names.includes(this.$store.state.user.username);
    }
  }
};
</script>
