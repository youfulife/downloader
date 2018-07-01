<template>
  <div id="app">
    
    <b-container class="p-4">
      <b-row>
        <b-col>
          <b-img  left fluid :src="require('./assets/logo.png')" />
        </b-col>
        <b-col>
          <b-img  right fluid width="200" height="200" :src="require('./assets/qrcode.png')" />
        </b-col>
      </b-row>
    </b-container>

    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
