<template>
  <v-list-item dense class="mb-2">
    <v-row :justify="isCurrentUser ? 'end' : 'start'">
      <v-col
        class="chat-message"
        cols="10"
        :offset="isCurrentUser ? 2 : 0"
        :class="{
          'text-right': isCurrentUser,
          'success lighten-3': isCurrentUser,
          'info lighten-4': !isCurrentUser
        }"
      >
        <v-list-item-title v-if="!isCurrentUser">
          {{ chatData.username }}
        </v-list-item-title>
        <v-list-item-subtitle class="text--wrap">
          {{ chatData.message }}
        </v-list-item-subtitle>
        <v-list-item-subtitle class="overline">
          {{ humanReadableDate(chatData.timestamp) }}
        </v-list-item-subtitle>
      </v-col>
    </v-row>
  </v-list-item>
</template>

<script>
export default {
  props: {
    currentUser: { type: String, default: "" },
    chatData: { type: Object, default: () => {} }
  },
  computed: {
    isCurrentUser() {
      return this.currentUser === this.chatData.user_id;
    }
  },
  methods: {
    timestampWithOffset(timestamp) {
      return timestamp - new Date().getTimezoneOffset() * 60 * 1000;
    },
    humanReadableDate(timestamp) {
      const date = new Date(this.timestampWithOffset(timestamp));
      return date.toTimeString().substr(0, 5);
    }
  }
};
</script>

<style scoped lang="scss">
.chat-message {
  border-radius: 1rem;
}
</style>
