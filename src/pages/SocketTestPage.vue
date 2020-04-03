<template>
  <v-container>
    <v-form @submit.prevent="sendMessage" :value="!!message">
      <v-row align="start" justify="center">
        <v-col cols="12" class="text-center">
          <h2>{{ $t("test_page.title") }}</h2>
        </v-col>
        <v-col cols="12" class="text-center">
          <h3>
            {{ $t("test_page.connected") }}
            <v-icon v-if="$socket.connected" small color="success">
              mdi-check-circle
            </v-icon>
            <v-icon v-else small color="error">mdi-close-circle</v-icon>
          </h3>
        </v-col>
        <v-col cols="12" sm="6" md="4" xl="3" class="text-center">
          <v-text-field
            v-model="message"
            :label="$t('test_page.echo')"
            outlined
            prepend-inner-icon="mdi-cloud-upload"
            hide-details
          />
          <v-row align="center" justify="space-around">
            <v-btn color="info" class="my-3" :disabled="!message" type="submit">
              {{ $t("test_page.send") }}
            </v-btn>
            <v-btn text @click="reset" class="my-3">
              {{ $t("test_page.reset") }}
            </v-btn>
          </v-row>
          <div class="mb-2">
            <h4>
              {{ $t("test_page.sent") }}
              <v-icon v-if="echoSent" small color="success">mdi-check-circle</v-icon>
              <v-icon v-else small color="error">mdi-close-circle</v-icon>
            </h4>
            <h4>
              {{ $t("test_page.received") }}
              <v-icon v-if="echoReceived" small color="success">mdi-check-circle</v-icon>
              <v-icon v-else small color="error">mdi-close-circle</v-icon>
            </h4>
          </div>
          <h3>{{ $t("test_page.messages") }}</h3>
          <div v-for="(message, index) in echoMessages" :key="index">
            {{ message }}
          </div>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      message: "",
      echoSent: false,
      echoReceived: false,
      echoMessages: []
    };
  },
  sockets: {
    echo(message) {
      this.echoMessages.push(message);
      this.echoReceived = true;
    }
  },
  methods: {
    sendMessage() {
      this.echoSent = true;
      this.echoReceived = false;
      this.$socket.client.emit("echo", this.message);
      this.message = "";
    },
    reset() {
      this.message = "";
      this.echoReceived = false;
      this.echoSent = false;
      this.echoMessages = [];
    }
  }
};
</script>
