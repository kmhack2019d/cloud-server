<script>
import { Line, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  name: 'LineChart',
  extends: Line,
  mixins: [reactiveProp],
  props: {
    chartData: {
      type: Object,
      default: null
    }
  },
  data: () =>  ({
    options: {
      title: {
        display: false
      },
      legend: {
        display: false
      },
      responsive: true,
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
              min: 0,
              max: 100
            }
          }
        ]
      }
    }
  }),
  mounted: function() {
    this.renderChart(this.chartData, this.options)
  }
}
</script>
