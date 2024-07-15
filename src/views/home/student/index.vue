<template>
  <div id="app">
    <el-card class="detect">
      <!-- 左侧上传视频部分 -->
      <el-upload class="upload-demo" drag action="http://localhost:5000/upload" multiple style="height: 250px;"
        accept="video/*" :on-success="handleUploadSuccess">
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将文件拖拽于此 或 <em>点击上传</em>
        </div>
      </el-upload>
      <div class="vid_info_1" style="border-radius: 0 0 5px 5px">
        <span style="color: white; letter-spacing: 6px">原始视频</span>
      </div>
    </el-card>

    <el-card class="detect-result">
      <!-- 右侧视频检测结果部分 -->
      <div class="videoUrl-wrapper">
        <div class="videoUrl">
          <video controls width="100%" height="100%">
            <source :src="videoUrl" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        </div>
      </div>
      <div class="vid_info_1" style="border-radius: 0 0 5px 5px">
        <span style="color: white; letter-spacing: 4px">检测结果</span>
      </div>
    </el-card>

    <el-card class="plot">
      <!-- 下方折线图部分 -->
      <div class="imageSrc">
        <span>行为结果分析</span>
        <button @click="generateStatistics">生成统计图</button>
        <div v-if="imageSrc">
          <img :src="imageSrc" alt="结果图" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>


export default {
  data() {
    return {
      videoFile: null,
      videoUrl: null,
      imageSrc: null,
    };
  },
  methods: {
    handleUploadSuccess(response, file) {
      console.log("视频处理结果:", response);
      // 假设后端返回的是处理后的视频地址和统计图地址
      if (response.videoUrl) {
        this.videoUrl = response.videoUrl;
      }
      if (response.imageUrl) {
        this.imageSrc = response.imageUrl;
      }
    },
    generateStatistics() {
      fetch("http://localhost:5000/generate-statistics")
        .then((response) => response.blob())
        .then((blob) => {
          this.imageSrc = URL.createObjectURL(blob);
        })
        .catch((error) => console.error("Error:", error));
    },
  },
};
</script>

<style scoped lang="scss">
#app {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.el-card {
  width: 45%;
  margin-bottom: 20px;
}

.detect {
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-demo {
  text-align: center;
}

.el-upload__text {
  margin-top: 10px;
}

.detect-result {
  display: flex;
  align-items: center;
  justify-content: center;
}

.videoUrl-wrapper {
  text-align: center;
  width: 100%;
  margin: 0 auto; /* 居中 */
}

.videoUrl {
  width: calc(100% - 20px); /* 略小于父元素宽度，这里假设 el-card 的 margin 已知为 20px */
  height: auto;
  border: 2px solid #ccc;
  box-sizing: border-box;
}

.plot {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.vid_info_1 {
  height: 30px;
  width: 275px;
  text-align: center;
  background-color: #21b3b9;
  line-height: 30px;
}

.imageSrc {
  margin-top: 20px;
  text-align: center;
}

.imageSrc img {
  max-width: 100%;
  height: auto;
}
</style>