<template>
  <v-snackbar v-model="snackbar" bottom :timeout="6000">
    {{ message }}
    <v-btn text @click="snackbar = false">
      Close
    </v-btn>
  </v-snackbar>
</template>

<script>
import i18n from "../../languages";
export default {
  data() {
    return {
      snackbar: false,
      message: ""
    };
  },
  sockets: {
    message(message) {
      if (message) {
        this.message = i18n.t(`snackbar.${message}`);
        this.snackbar = true;
      }
    }
  }
};
</script>
