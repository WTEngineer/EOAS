<template lang="pug">
.loader.tw-flex.tw-justify-center.tw-items-center(v-if="showLoader")
  img(:src="logoSrc" alt="Loading" @load="onLoad" width="200px" style="background-color: rgb(17, 17, 17)")
</template>

<script>
export default {
  name: 'Loader',
  props: {
    reload: Boolean,
    minDisplayTime: {
      type: Number,
      default: 3000 // Minimum display time in milliseconds
    }
  },
  data() {
    return {
      showLoader: true,
      isLoaded: false,
      startTime: null,
      mode: 'light',
    };
  },
  computed: {
    logoSrc() {
      // Conditionally require the image based on the mode
      if (this.mode === 'light') {
        return require('../assets/img/light_logo.gif');
      } else {
        return require('../assets/img/dark_logo.gif');
      }
    }
  },
  methods: {
    onLoad() {
      this.isLoaded = true;
      this.checkLoaderTime();
    },
    checkLoaderTime() {
      const currentTime = new Date().getTime();
      const elapsedTime = currentTime - this.startTime;
      const remainingTime = this.minDisplayTime - elapsedTime;
      
      if (remainingTime > 0) {
        setTimeout(() => {
          this.showLoader = false;
        }, remainingTime);
      } else {
        this.showLoader = false;
      }
    }
  },
  mounted() {
    this.startTime = new Date().getTime();
    this.mode = localStorage.getItem('theme') || 'light';
  },
};
</script>

<style scoped>
.loader {
  background: rgba(var(--cui-bg-default-rgb));
  width: 100vw;
  min-width: 100vw;
  max-width: 100vw;
  height: 100vh;
  min-height: 100vh;
  max-height: 100vh;
}
</style>
