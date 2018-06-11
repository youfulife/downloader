<template>
  <div>
    <p>小视频下载</p>
    <p>Random number from backend: {{ randomNumber }}</p>
    <b-form @submit="onSubmit" v-if="show">
      <b-form-group id="fieldset1"
                    description="示例：https://www.zhihu.com/question/xxx/answer/xxx"
                    label=""
                    label-for="input1"
                    :invalid-feedback="invalidFeedback"
                    :valid-feedback="validFeedback"
                    :state="state">
        <b-form-input id="input1"
                      :state="state"
                      v-model.trim="seed"
                      required>
        </b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">下载</b-button>
    </b-form>

    <b-progress :value="progress" variant="success" :striped="striped" :animated="animate" show-progress class="mb-2"></b-progress>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  computed: {
    state () {
      return this.seed.length >= 4
    },
    invalidFeedback () {
      if (this.seed.length > 4) {
        return ''
      } else {
        return '请输入包含视频的知乎回答链接'
      }
    },
    validFeedback () {
      return this.state === true ? 'Thank you' : ''
    }
  },
  data () {
    return {
      // 进度条
      progress: 10,
      striped: true,
      animate: true,

      show: true,
      seed: '',
      video: '',
      timer: null
    }
  },
  mounted () {
    this.timer = setInterval(() => {
      this.progress = 25 + (Math.random() * 75)
    }, 2000)
  },
  beforeDestroy () {
    clearInterval(this.timer)
    this.timer = null
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      this.download()
      // alert(JSON.stringify(this.form));
    },
    download () {
      const path = 'http://localhost:5000/video/zhihu'
      axios.post(path, {
        url: this.seed
      })
        .then(response => {
          this.video = response.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>
