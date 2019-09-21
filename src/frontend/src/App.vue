<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer" app>
      <v-list dense>
        <v-list-item @click="viewflag=1" @click.stop="drawer = !drawer">
          <v-list-item-action>
            <v-icon>mdi-domain</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>店舗</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item @click="viewflag=2" @click.stop="drawer = !drawer">
          <v-list-item-action>
            <v-icon>mdi-chart-line-variant</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>リアルタイム統計</v-list-item-title>
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
          <v-row
                 v-for="(store, i) in stores"
                 :key="i">
              <v-card min-width="344" class="mx-auto">
                <v-card-title v-text="store.title"></v-card-title>
                <v-card-text v-text="store.text"></v-card-text>
                <v-card-text v-text="store.level"></v-card-text>
                <v-img :src="store.src"></v-img>
                <v-card-actions>
                  <v-btn text>詳細</v-btn>
                </v-card-actions>
              </v-card>
              <!-- <v-card max-width="344" class="mx-auto"> -->
              <!--   <v-card-title>goWork 新宿</v-card-title> -->
              <!--   <v-card-text></v-card-text> -->
              <!--   <v-card-actions> -->
              <!--     <v-btn text>Click</v-btn> -->
              <!--   </v-card-actions> -->
              <!-- </v-card> -->
              <!-- <v-card max-width="344" class="mx-auto"> -->
              <!--   <v-card-title>coworking 新宿</v-card-title> -->
              <!--   <v-card-text>unknown</v-card-text> -->
              <!--   <v-card-actions> -->
              <!--     <v-btn text>Click</v-btn> -->
              <!--   </v-card-actions> -->
              <!-- </v-card> -->
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
                label="店舗"
                outlined
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

      <v-footer
        absolute
        padless>
        <div class="flex-grow-1"></div>
        <span>&copy; 2019</span>
        <div class="flex-grow-1"></div>
      </v-footer>
    </v-content>
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
import axios from 'axios'
import LineChart from './components/LineChart'

export default {
  components: {
    LineChart
  },
  props: {
    source: String
  },
  data: () => ({
    drawer: false,
    activeBtn: 1,
    viewflag: 1,
    items: null,
    currentItem: null,
    chartData: null,
    stores: [
      {
        src: 'http://163.43.194.84/api/v1/get_image?rasp_id=0',
        title: 'goWork 渋谷',
        text: '静かレベル',
        json: null,
        level: undefined,
        filename: 'data0.json'
      },
      {
        src: 'http://163.43.194.84/api/v1/get_image',
        title: 'goWork 新宿',
        text: '静かレベル',
        json: null,
        level: undefined,
        filename: 'dummymoon.json'
      },
      {
        src: 'http://163.43.194.84/api/v1/get_image',
        title: 'coworking 池袋',
        text: '静かさレベル',
        json: null,
        level: undefined,
        filename: 'dummyvenus.json'
      },
    ],
  }),
  methods: {
    getJsons: async function(stores) {
      cpsp.AdminStaff.login(CPS_PROD_MAIL_ADDRESS, CPS_PROD_PASSWORD, undefined, undefined, true)
        .then(cred => {
          console.log("cred", cred.key)
          const admin = new cpsp.AdminStaff(cred.key)
          for (let s of stores) {
            const file = new cpsp.File(admin, CPS_APP_ID, CPS_GROUP_ID, 'sample_file', s.filename, true)
            file.download().then(d => {
              let reader = new FileReader()
              reader.onload = e => {
                const json = JSON.parse(e.target.result)
                console.log("stat", json)
                s.json = json
                // only use index 0 mic
                const aveValue = this.average(json[0].data.map(d => d.value))
                switch (true) {
                case aveValue < 100:
                  s.level = 0
                case aveValue < 80:
                  s.level = 1
                case aveValue < 60:
                  s.level = 2
                case aveValue < 40:
                  s.level = 3
                case aveValue < 20:
                  s.level = 4
                }
              }
              reader.readAsText(d)
            })
          }
        })
    },
    showChart: function(item) {
      this.currentItem = item
      const storeIndex = this.items.findIndex(i => i === item)
      console.log(storeIndex)
      this.chartData =
        {
          labels: new Array(this.stores[storeIndex].json[0].data.length).fill(1).map((n, i) => n + i),
          datasets: [{
            borderColor: '#0000ff',
            data: this.stores[storeIndex].json[0].data.map(d => d.value),
            pointRadius: 0,
            fill: false
          }]
        }
    },
    sum: function(arr) {
      return arr.reduce(function(prev, current, i, arr) {
        return prev+current;
      })
    },
    average: function(arr, fn) {
      return this.sum(arr, fn)/arr.length;
    },
  },
  created: function () {
    this.items = this.stores.map(s => s.title)
    this.getJsons(this.stores)
    // axios.get('http://163.43.194.84/api/v1/get_image')
    //   .then(response => {
    //     console.log(response.data) // mockData
    //     console.log(response.status) // 200
    //   })
  }
};
</script>
