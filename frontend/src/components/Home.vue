<template>
  <div>
    <p>小视频下载</p>
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
    <div v-for="item in items" :key="item.video">
      <b-progress :value="item.progress" variant="success" :striped="item.striped" :animated="item.animate" class="mb-2"></b-progress>
      <p>时长: {{ item.duration }}</p>
      <p>当前时长: {{ item.progress }}</p>

      <b-embed type="video" aspect="4by3" controls>
        <source  :src="item.video" type='video/mp4'/>
      </b-embed>
    </div>
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
      show: true,
      seed: '',
      items: [],
      timer: null
    }
  },
  mounted () {
    this.timer = setInterval(() => {
      const path = 'http://localhost:5000/video/progress'
      for (var i = 0; i < this.items.length; i++) {
        var item = this.items[i]
        axios.get(path, {
          params: {
            filename: item.video
          }
        })
          .then(response => {
            // 进度条
            // 0 还未开始，1 正在下载，2 下载完成
            if (!item.started) {
              var started = (response.data.seconds == 0) ? 0 : 1
            } else {
              var started = (response.data.seconds == 0) ? 2 : 1
            }
            var striped = (started == 1) ? true : false
            var animate = (started == 1) ? true : false
            item = Object.assign({}, item, {
                        progress: Math.round(response.data.seconds * 100.0 / item.duration),
                        striped: striped,
                        animate: animate,
                        started: started
                    })
            Vue.set(this.items, i, item)
            
          })
          .catch(error => {
            console.log(error)
          })
      }
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
          this.items = response.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>
