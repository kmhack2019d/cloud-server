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
      <v-toolbar-title>noisee</v-toolbar-title>
    </v-app-bar>

    <v-content>
      <div v-if="viewflag==1">
        <v-container fluid>
          <v-row>
            <v-col class="text-center">
              <v-card max-width="344" class="mx-auto">
                <v-card-title>渋谷店</v-card-title>
                <v-card-text></v-card-text>
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
              <v-select
                :items="items"
                label="Outlined style"
                @change="showChart"
                ></v-select>
            </v-col>
          </v-row>
        </v-container>
      </div>
    </v-content>

    <v-bottom-navigation :value="activeBtn" grow color="indigo">
      <v-btn @click="viewflag=1">
        <span>noise map</span>
        <v-icon>mdi-map</v-icon>
      </v-btn>

      <v-btn @click="viewflag=2">
        <span>stat</span>
        <v-icon>mdi-chart-line-variant</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
</template>

<script>
import * as cpsp from "./cpsp.js"
import {
  CPS_PROD_MAIL_ADDRESS,
  CPS_PROD_PASSWORD,
  CPS_APP_ID,
  CPS_GROUP_ID
} from "./config.js"

export default {
  props: {
    source: String
  },
  data: () => ({
    drawer: null,
    activeBtn: 1,
    viewflag: 1,
    items: ['渋谷', '品川', '池袋']
  }),
  methods: {
    showChart: (item) => {
      cpsp.AdminStaff.login(CPS_PROD_MAIL_ADDRESS, CPS_PROD_PASSWORD, undefined, undefined, true)
        .then(cred => {
          console.log(item)
          console.log("cred", cred.key)
          const admin = new cpsp.AdminStaff(cred.key)
          const file = new cpsp.File(admin, CPS_APP_ID, CPS_GROUP_ID, 'sample_file', 'dummy.json', true)
          file.download().then(d => {
            let reader = new FileReader()
            reader.onload = e => {
              const str = e.target.result
              // console.log(str)
              console.log(JSON.parse(str))
              // chartConfig.data.labels = Array.from({length: newdata.length}, (v, k) => k)
              // chartConfig.data.datasets[0].data = newdata
              // chart.update()
            }
            reader.readAsText(d)
          })
        })
    }
  }
};
</script>
