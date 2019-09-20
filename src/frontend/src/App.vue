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
                :value="currentItem"
                label="Outlined style"
                @change="showChart"
                ></v-select>
              <line-chart
                :chartData="chartData"
                class=chart
                />
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
import LineChart from './components/LineChart'

export default {
  components: {
    LineChart
  },
  props: {
    source: String
  },
  data: () => ({
    drawer: null,
    activeBtn: 1,
    viewflag: 1,
    items: ['渋谷', '品川', '池袋'],
    currentItem: null,
    chartData: null,
  }),
  methods: {
    showChart: function(item) {
      this.currentItem = item
      cpsp.AdminStaff.login(CPS_PROD_MAIL_ADDRESS, CPS_PROD_PASSWORD, undefined, undefined, true)
        .then(cred => {
          console.log(item)
          console.log("cred", cred.key)
          const admin = new cpsp.AdminStaff(cred.key)
          let filename;
          switch (item) {
          case "渋谷":
            filename = "dummysun.json"
            break
          case "品川":
            filename = "dummymoon.json"
            break
          case "池袋":
            filename = "dummyvenus.json"
            break
          default:
            filename = "dummy.json"
          }
          const file = new cpsp.File(admin, CPS_APP_ID, CPS_GROUP_ID, 'sample_file', filename, true)
          file.download().then(d => {
            let reader = new FileReader()
            reader.onload = e => {
              const stat = JSON.parse(e.target.result)
              console.log("stat", stat)
              this.chartData =
                {
                  labels: new Array(stat[0].data.length).fill(1).map((n, i) => n + i),
                  datasets: [{
                    label: 'chartData',
                    borderColor: '#0000ff',
                    data: stat[0].data.map(d => d.value),
                    fill: false
                  }]
                }
            }
            reader.readAsText(d)
          })
        })
    }
  }
};
</script>
