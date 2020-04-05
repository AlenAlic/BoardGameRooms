<template>
  <v-form @submit.prevent="sendMessage" :value="!!message">
    <v-list class="bottom-padding">
      <chat-message
        v-for="(data, idx) in $store.state.room.messages"
        :key="idx"
        :chat-data="data"
        :current-user="$store.state.user.user_id"
      />
    </v-list>
    <v-footer absolute height="60px">
      <v-text-field
        v-model="message"
        outlined
        hide-details
        dense
        append-outer-icon="mdi-send"
        @click:append-outer="sendMessage"
      />
    </v-footer>
  </v-form>
</template>

<script>
import { UPDATE_CHAT } from "../../store/modules/room";
import ChatMessage from "../../components/general/ChatMessage";
export default {
  components: { ChatMessage },
  props: {
    initialDrawer: null
  },
  data() {
    return {
      message: ""
    };
  },
  computed: {
    validInput() {
      return this.username && this.room;
    }
  },
  sockets: {
    room_chat_update(data) {
      this.$store.commit(UPDATE_CHAT, data);
    }
  },
  methods: {
    sendMessage() {
      if (this.message) {
        let data = {
          username: this.$store.state.user.username,
          user_id: this.$store.state.user.user_id,
          room: this.$store.state.user.room,
          message: this.message,
          timestamp: this.$util.timestampUTC
        };
        this.$socket.client.emit("chat_game_room", data);
        this.message = "";
        this.$emit("updated");
      }
    }
  }
};
</script>

<style scoped lang="scss">
.bottom-padding {
  padding-bottom: 72px;
}
</style>
