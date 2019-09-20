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
        display: true,
        text: 'Line chart'
      },
      legend: {
        display: false
      },
    }
  }),
  mounted: function() {
    this.renderChart(this.chartData, this.options)
  }
}
</script>
