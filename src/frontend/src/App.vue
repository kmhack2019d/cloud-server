<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer" app>
      <v-list dense>
        <v-list-item @click>
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click>
          <v-list-item-action>
            <v-icon>mdi-contact-mail</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Contact</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="indigo" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Application</v-toolbar-title>
    </v-app-bar>

    <v-content>
      <div v-if="viewflag==1">
        <v-container fluid>
          <v-row>
            <v-col class="text-center">
              <v-card max-width="344" class="mx-auto">
                <v-card-title>I'm a title</v-card-title>
                <v-card-text>I'm card text</v-card-text>
                <v-card-actions>
                  <v-btn text>Click</v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </div>

      
      <div v-if="viewflag==2">
        <v-container fluid>
          <v-row>
            <v-col class="text-center">
              <v-card max-width="344" class="mx-auto">
                <v-card-title>I'm a title22222222222</v-card-title>
                <v-card-text>I'm card text</v-card-text>
                <v-card-actions>
                  <v-btn text>Click</v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </div>
    </v-content>

    <v-bottom-navigation :value="activeBtn" color="deep-purple accent-4">
      <v-btn @click="viewflag=1">
        <span>Recents</span>
        <v-icon>mdi-history</v-icon>
      </v-btn>

      <v-btn @click="viewflag=2">
        <span>Favorites</span>
        <v-icon>mdi-heart</v-icon>
      </v-btn>

      <v-btn>
        <span>Nearby</span>
        <v-icon>mdi-map-marker</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
</template>

<script>
export default {
  props: {
    source: String
  },
  data: () => ({
    drawer: null,
    viewflag: 2
  })
};
</script>