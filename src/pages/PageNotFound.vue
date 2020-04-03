<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="auto">
        <v-card max-width="400">
          <v-card-title>{{ $t("page_not_found.text") }}</v-card-title>
          <v-card-actions>
            <v-spacer />
            <v-btn text color="primary" :to="{ name: 'home' }">
              {{ $t("page_not_found.go_back") }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
