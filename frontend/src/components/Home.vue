<template>
  <div>
    <p>小视频下载</p>
    <p>Random number from backend: {{ randomNumber }}</p>
    <b-container fluid>
      <b-row>
        <b-col sm="9"><b-form-input placeholder="输入知乎回答URL地址" v-model="seed"></b-form-input></b-col>
        <b-col sm="9"><button @click="getVideo">下载</button></b-col>
      </b-row>
    </b-container>
  </div>
  <div role="group">
    <b-row>
      <b-col sm="9">
        <b-form-input id="inputLive"
                      v-model.trim="seed"
                      type="text"
                      :state="nameState"
                      aria-describedby="inputLiveHelp inputLiveFeedback"
                      placeholder=""></b-form-input>
        <b-form-invalid-feedback id="inputLiveFeedback">
          <!-- This will only be shown if the preceeding input has an invalid state -->
          地址不能为空
        </b-form-invalid-feedback>
        <b-form-text id="inputLiveHelp">
          <!-- this is a form text block (formerly known as help block) -->
          包含视频的知乎回答完整URL地址
        </b-form-text>
      </b-col>
      <b-col sm="9"><button @click="getVideo">下载</button></b-col>
    </b-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      randomNumber: 0,
      seed: null
    }
  },
  methods: {
    getVideo () {
      // this.randomNumber = this.getRandomInt(1, 100)
      this.randomNumber = this.getRandomFromBackend()
    },
    getRandomFromBackend () {
      const path = 'http://localhost:5000/video/zhihu'
      axios.post(path, {
        url: this.seed
      })
        .then(response => {
          this.randomNumber = response.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>

