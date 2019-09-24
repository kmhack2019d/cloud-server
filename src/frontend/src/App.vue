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
          <v-layout column>
              <v-card class="mb-2" v-for="(store, i) in stores" :key="i">
                <v-img
                  class="white--text"
                  height="200px"
                  :src="store.image_url"
                  >
                  <v-card-title class="align-end fill-height" v-text="store.title"></v-card-title>
                </v-img>
                <v-card-text>
                  <v-chip class="">リアルタイム静かレベル:
                    <v-avatar right color="blue" dark v-if="store.level != -1">{{ store.level }}</v-avatar>
                    <v-avatar right color="black" class="white--text" dark v-else>?</v-avatar>
                  </v-chip><br/>
                  <div class="black--text">
                    {{ store.text }}
                  </div>
                  <div class="black--text">
                    <v-chip v-if="store.active" color="primary" dark>
                      現在営業中!!
                    </v-chip>
                    <div v-else>
                      現在営業外
                    </div>
                  </div>
                </v-card-text>
                <v-rating v-model="store.star" readonly></v-rating>
                <v-card-actions>
                  <v-btn text @click="detail(i)">詳細</v-btn>
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
          </v-layout>
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
        padless>
        <div class="flex-grow-1"></div>
        <span>&copy; 2019</span>
        <div class="flex-grow-1"></div>
      </v-footer>
    </v-content>
    <v-dialog v-model="dialog.show" fullscreen hide-overlay>
        <v-card class="mb-2">
          <v-img
            class="white--text"
            height="200px"
            :src="dialog.store.image_url"
            >
            <div>
              <v-btn icon outlined color="white" class="mt-2 ml-2" @click="dialog.show = false">×</v-btn>
            </div>
          </v-img>
          <v-card-title>{{dialog.store.title}}</v-card-title>
          <v-card-text>
            <v-chip>リアルタイム静かレベル:
                <v-avatar right color="blue" dark v-if="dialog.store.level != -1">{{ dialog.store.level }}</v-avatar>
                <v-avatar right color="black" class="white--text" dark v-else>?</v-avatar>
            </v-chip><br/>
            <div class="black--text">
              {{ dialog.store.text }}
            </div>
            <div class="black--text">
              <v-chip v-if="dialog.store.active" color="primary" dark>
                現在営業中!!
              </v-chip>
              <div v-else>
                現在営業外
              </div>
            </div>
            <div class="mt-6" v-if="dialog.store.level != -1">
              リアルタイムな机ごとのうるささ
              <img :src="dialog.store.src" style="width: 100%" ref="store-heatmap">
            </div>
          </v-card-text>
          <v-rating v-model="dialog.store.star" readonly></v-rating>
        </v-card>
    </v-dialog>
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
    dialog: {
      id: 0,
      show: false,
      store: {}
    },
    stores: [
      {
        src: 'http://163.43.194.84/api/v1/get_image',
        title: 'goWork 渋谷',
        text: '過ごしやすく、とても広い部屋が特徴です。部屋が綺麗で冷暖房完備なので、女性の方もおすすめ！',
        json: null,
        level: undefined,
        star: 4,
        filename: 'data0.json',
        active: true,
        image_url: 'https://www.smbc-card.com/hojin/magazine/bizi-dora/general-affairs/img/coworking-space.jpg'
      },
      {
        src: 'http://163.43.194.84/api/v1/get_image',
        title: 'goWork 新宿',
        text: '新宿で駅近でアクセス良好！本棚が充実しており、プログラミングやデザインを仕事にしている方にぴったり。',
        json: null,
        level: undefined,
        star: 3,
        filename: 'dummymoon.json',
        active: false,
        image_url: 'http://workmill.jp/assets/uploads/2016/04/ph01_report3-.jpg'
      },
      {
        src: 'http://163.43.194.84/api/v1/get_image',
        title: 'coworking 池袋',
        text: '静かで大変作業がしやすいことが特徴。雑音がなくて、集中したい人にとっておすすめのコアワーキングスペースです。',
        json: null,
        level: -1,
        star: 5,
        filename: 'dummyvenus.json',
        active: true,
        image_url: 'https://time-space.kddi.com/digicul-column/digicul-joho/20170127/images/img008.jpg'
      },
    ],
  }),
  methods: {
    detail: function (id) {
      location.href="/"+id
    },
    getJsons: async function(stores) {
      cpsp.AdminStaff.login(CPS_PROD_MAIL_ADDRESS, CPS_PROD_PASSWORD, undefined, undefined, true)
        .then(cred => {
          console.log("cred", cred.key)
          const admin = new cpsp.AdminStaff(cred.key)
          for (let s of stores) {
            if (s.level != -1) {
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
    if (location.pathname == "/0") {
      this.dialog.show = true
      this.dialog.id = 0
      this.dialog.store = this.stores[this.dialog.id]

    } else if (location.pathname == "/1") {
      this.dialog.show = true
      this.dialog.id = 1
      this.dialog.store = this.stores[this.dialog.id]

    } else if (location.pathname == "/2") {
      this.dialog.show = true
      this.dialog.id = 2
      this.dialog.store = this.stores[this.dialog.id]

    }
  }
};
</script>

