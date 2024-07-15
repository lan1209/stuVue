<template>
  <div class="container">
    <h3>test</h3>

      <video
        :src="`C:/Users/cha/Desktop/1.mp4`"
        controls
      ></video>

  </div>
</template>
 
<script>
export default {
  name: 'VideoDialog',
  data () {
    return {
      isShow: false,
      // 测试地址
      // videoUrl: 'http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4'
      videoUrl: 'C:/Users/chaiz/Desktop/1.mp4'
    }
  },
 
  created () {
    console.log(this.videoUrl, '视频')
  },
  methods: {
    // 视频播放
    playVideo (row) {
      this.isShow = true
      // 将接受的值赋值给src
      this.videoUrl = row.videoUrl
    },
    closeDialog () {
      // 关闭弹框
      this.isShow = false
      this.videoUrl = '' // 清空数据 关闭视频播放
    }
  }
}
</script>
 
<style scoped lang="scss">

</style>