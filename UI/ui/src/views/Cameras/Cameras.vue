
<template lang="pug">
.camera-page
  v-btn.clear-btn(:class="fabAbove ? 'clear-btn-top' : ''" v-scroll="onScroll" v-show="fab" color="error" transition="fade-transition" width="60" height="60" fab dark fixed bottom right @click="clear" :loading="loadingProgress")
    v-icon {{ icons['mdiCloseThick'] }}
  v-row.tw-w-full
    v-col(cols="4" style="padding: 5px 0")
      .sidebar
        v-list.sidebar(style=" box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px; padding: 10px; ")
          v-list-item(v-for="(item, index) in analyticsData" :key="index" style=" height: 130px; padding: 5px; background-color: #f0f0f0; border-radius: 10px; margin-bottom: 10px")
            v-list-item-avatar(style="margin-right: 5px; width: 100px; height: 100px")
              img(:src="item.avatar1" alt="Avatar")
            v-list-item-avatar(style="margin-right: 5px; width: 100px; height: 100px")
              img(:src="item.avatar2" alt="Avatar")
            v-list-item-content(style="height: 130px; width: 100%; padding: 0; margin: 0")
              v-list-item-title {{ item.name }}
              v-list-item-subtitle
                .text-xs {{$t('gender')}}: {{ item.gender }}
                .text-xs {{$t('status')}}: {{ item.status }}
                .text-xs {{$t('blocked')}}: {{ item.blocked }}
                .text-xs {{$t('guest')}}: {{ item.guesttype }}
                .text-xs {{$t('safety')}}: {{ item.safetytype }}
                .text-xs {{ item.timestamp }}
            v-icon(:color="item.iconColor" style="position: absolute; right: 5px; top: 5px;") {{ icons[item.action] }}
    v-col(cols="8")
      v-row.tw-w-full(style="padding: 15px 0")
        v-col(:cols="cameraView? 12: 6")
          .tw-w-full
            .camera-box(:style="cameraView ? 'height: 500px' : 'height: 250px'")
              img(
                v-if="streamAvailable1"
                :src="streamSrc1"
                alt="Camera 1 Feed"
                class="camera-stream"
              )
              img(
                v-else
                src="/img/icons/camera.png"   
                alt="Default Image"
                width="100"
                height="100"
              )
        v-col(:cols="cameraView? 12: 6")
          .tw-w-full
            .camera-box(:style="cameraView ? 'height: 500px' : 'height: 250px'")
              img(
                v-if="streamAvailable2"
                :src="streamSrc2"
                alt="Camera 2 Feed"
                class="camera-stream"
              )
              img(
                v-else
                src="/img/icons/camera.png"  
                alt="Default Image"
                width="100"
                height="100"
              )
        v-col(:cols="cameraView? 12: 6")
          .tw-w-full
            .camera-box(:style="cameraView ? 'height: 500px' : 'height: 250px'")
              img(
                v-if="streamAvailable3"
                :src="streamSrc3"
                alt="Camera 3 Feed"
                class="camera-stream"
              )
              img(
                v-else
                src="/img/icons/camera.png"  
                alt="Default Image"
                width="100"
                height="100"
              )
        v-col(:cols="cameraView? 12: 6")
          .tw-w-full
            .camera-box(:style="cameraView ? 'height: 500px' : 'height: 250px'")
              img(
                v-if="streamAvailable4"
                :src="streamSrc4"
                alt="Camera 4 Feed"
                class="camera-stream"
              )
              img(
                v-else
                src="/img/icons/camera.png"  
                alt="Default Image"
                width="100"
                height="100"
              )
              
</template>

<script>
import axios from 'axios';
import { mdiAlert, mdiShare, mdiReply, mdiCloseThick } from '@mdi/js';

export default {
  name: 'CameraPage',
  data() {
    return {
      ws: null,
      fab: true,
      fabAbove: false,
      streamAvailable1: false,
      streamAvailable2: false,
      streamAvailable3: false,
      streamAvailable4: false,
      streamSrc1: `http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/stream1`,
      streamSrc2: `http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/stream2`,
      streamSrc3: `http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/stream3`,
      streamSrc4: `http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/stream4`,
      icons: {
        'Unknown': mdiAlert,
        'ComeOut': mdiShare,
        'ComeIn': mdiReply,
        mdiCloseThick,
      },
      cameraView: false,
      analyticsData: [],
      intervalId: null,
    };
  },
  async created() {
    if (localStorage.getItem('cameraView')) {
      this.cameraView = localStorage.getItem('cameraView') === 'first'? true: false;
    }
    await this.checkStreamAvailability(`${this.streamSrc1}/available`, 'streamAvailable1');
    await this.checkStreamAvailability(`${this.streamSrc2}/available`, 'streamAvailable2');
    this.intervalId = setInterval(this.fetchAnalyticsData, 5000);
    // await this.checkStreamAvailability(`${this.streamSrc3}/available`, 'streamAvailable3');
    // await this.checkStreamAvailability(`${this.streamSrc4}/available`, 'streamAvailable4');
  },
  beforeDestroy() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  },
  async mounted() {
    // Check if streams are available
    // await this.initWebSocket();
    console.log(this.streamAvailable3)
  },
  methods: {
    async checkStreamAvailability(src, streamAvailable) {
      const response = await axios.get(src);
      console.log(response.status)
      console.log(streamAvailable)
      if (response.status === 200) {
        this[streamAvailable] = true;
      }
    },
    // initWebSocket() {
    //   this.ws = new WebSocket('ws://localhost:8000/ws/camera-analytics');
    //   this.ws.onopen = () => {
    //     console.log('WebSocket connection opened');
    //   };
    //   console.log('init web socket');
    //   console.log(this.ws);
    //   this.ws.onmessage = this.handleWebSocketMessage;
    //   this.ws.onerror = (error) => {
    //     console.error('WebSocket error:', error);
    //   };
    //   this.ws.onclose = () => {
    //     console.log('WebSocket connection closed, retrying...');
    //     setTimeout(this.initWebSocket, 5000);
    //   };
    // },
    // handleWebSocketMessage(event) {
    //   const data = JSON.parse(event.data);
    //   console.log('socket data');
    //   console.log(data);
    // },
    fetchAnalyticsData() {
      fetch(`http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/camera-analytics`)
        .then(response => response.json())
        .then(data => {
          console.log(data.action);
          if (data && data.action) {
            if (this.analyticsData.length === 0 || (this.analyticsData.length > 0 && this.analyticsData[this.analyticsData.length - 1].action !== data.action))
              if (data.action === 'ComeOut') {
                this.analyticsData.unshift({...this.analyticsData[this.analyticsData.length - 1], action: 'ComeOut', iconColor: 'red'})
              }
              this.analyticsData.unshift({
                ...data,
                iconColor: data.action === 'Unknown'? '#dddd00': data.action === 'ComeIn'? 'green': 'red',
                avatar1: `data:image/jpeg;base64,${data.firstPhoto}`,
                avatar2: `data:image/jpeg;base64,${data.secondPhoto}`,
              });
              console.log(this.analyticsData);
          }
        })
        .catch(error => console.error('Error fetching analytics data:', error));
    },
    onScroll(e) {
      if (typeof window === 'undefined') {
        this.fabAbove = true;
        return;
      }

      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fabAbove = top > 20;
    },
    clear() {
      this.analyticsData = [];
    },
  },
};
</script>

<style scoped>
.camera-page {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.camera-analytics-page {
  width: 30%;
}

.camera-box {
  width: 100%;
  height: 250px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  position: relative;
}

.camera-stream {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.sidebar {
  padding: 10px 0px;
  height: 100%;
}
.clear-btn {
  right: 30px !important;
  bottom: 75px !important;
  z-index: 11 !important;
  transition: 0.3s all;
}

.clear-btn-top {
  bottom: 125px !important;
}
</style>
