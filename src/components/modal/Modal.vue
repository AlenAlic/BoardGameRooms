<template>
  <v-dialog persistent v-model="show" :max-width="maxWidth">
    <v-card>
      <v-card-title>{{ title }}</v-card-title>
      <slot>
        <v-card-text class="text--wrap">
          {{ text }}
        </v-card-text>
      </slot>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn v-if="!!accept" color="primary" text @click="closeModal(true)" :disabled="acceptDisabled">
          {{ accept }}
        </v-btn>
        <v-btn text @click="closeModal(false)">
          {{ close }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import i18n from "../../languages";
export default {
  props: {
    show: { type: Boolean, default: false },
    size: { type: String, default: "" },
    title: { type: String, default: "" },
    text: { type: String, default: i18n.t("modal.text") },
    accept: { type: String, default: "" },
    acceptDisabled: { type: Boolean, default: false },
    close: { type: String, default: i18n.t("modal.close") }
  },
  model: {
    prop: "show",
    event: "close"
  },
  computed: {
    maxWidth() {
      switch (this.size) {
        case "small":
          return "290";
        case "large":
          return "890";
        default: {
          return "450";
        }
      }
    }
  },
  methods: {
    closeModal: function(flag) {
      if (flag) {
        this.$emit("yes");
      }
      this.$emit("close", false);
    }
  }
};
</script>
