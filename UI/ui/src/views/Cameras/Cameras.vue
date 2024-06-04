<!-- <template lang="pug">
.tw-flex.tw-justify-center.tw-items-center.page-loading(v-if="loading")
  v-progress-circular(indeterminate color="var(--cui-primary)")
.tw-py-6.tw-px-4(v-else)
  .pl-safe.pr-safe
    
    .tw-flex.tw-justify-between
      .header-title.tw-flex.tw-items-center
        .page-title {{ $t($route.name.toLowerCase()) }}
      .header-utils.tw-flex.tw-justify-center.tw-items-center
        v-btn.tw-mr-1(v-if="showListOptions" icon height="35px" width="35px" :color="listMode ? 'var(--cui-primary)' : 'grey'" @click="changeListView(1)")
          v-icon(size="25") {{ icons['mdiFormatListBulleted'] }}
        v-btn(v-if="showListOptions" icon height="35px" width="35px" :color="!listMode ? 'var(--cui-primary)' : 'grey'" @click="changeListView(2)")
          v-icon(size="25") {{ icons['mdiViewModule'] }}

    .tw-mt-5
      v-data-table.tw-w-full(v-if="listMode && cameras.length" @click:row="clickRow" :items-per-page="-1" calculate-widths disable-pagination hide-default-footer :loading="loading" :headers="headers" :items="cameras" :no-data-text="$t('no_data_available')" item-key="name" class="elevation-1" mobile-breakpoint="0")
        template(v-slot:item.status="{ item }")
          .tw-w-full.tw-text-center  
            v-icon(size="10" :color="camStates.some((cam) => cam.name === item.name && cam.status === 'ONLINE') ? 'success' : 'error'") {{ icons['mdiCircle'] }}
        template(v-slot:item.preview="{ item }")
          vue-aspect-ratio.tw-m-3(ar="16:9" width="100px")
            VideoCard(:camera="item" snapshot @cameraStatus="cameraStatus")
        template(v-slot:item.name="{ item }")
          b {{ item.name }}
        template(v-slot:item.model="{ item }")
          .text-font-disabled {{ item.model || 'IP Camera' }}
        template(v-slot:item.address="{ item }")
          .text-font-disabled {{ item.url }}
        template(v-slot:item.lastNotification="{ item }")
          .text-font-disabled {{ item.lastNotification ? item.lastNotification.time : $t('no_data') }}
        template(v-slot:item.liveFeed="{ item }")
          v-chip(color="var(--cui-primary)" dark small style="cursor: pointer" @click="$router.push(`/cameras/${item.name}`)") {{ camStates.some((cam) => cam.name === item.name && cam.status === 'ONLINE') ? $t('live') : $t('offline') }}

      div(v-for="room in rooms" :key="room" v-if="!listMode && ((room === 'Standard' && cameras.find((cam) => cam.settings.room === room)) || room !== 'Standard')")
        .tw-mt-7(v-if="room !== 'Standard'")
        
        h4(style="font-weight: 700;") {{ room === 'Standard' ? $t('standard') : room }}
        v-divider.tw-mt-3

        v-layout.tw-mt-5(row wrap)
          v-flex.tw-mb-3.tw-px-2(v-if="!listMode && camera.settings.room === room" xs12 sm6 md4 lg3 v-for="camera in cameras" :key="camera.name")
            vue-aspect-ratio(ar="4:3")
              VideoCard(:camera="camera" title titlePosition="bottom" snapshot)

    infinite-loading(:identifier="infiniteId", @infinite="infiniteHandler")
      div(slot="spinner")
        v-progress-circular(indeterminate color="var(--cui-primary)")
      .tw-mt-10.tw-text-sm.text-muted(slot="no-more") {{ $t("no_more_cameras") }}
      .tw-mt-10.tw-text-sm.text-muted(slot="no-results") {{ $t("no_cameras") }} :(

  LightBox(
    ref="lightboxBanner"
    :media="notImages"
    :showLightBox="false"
    :showThumbs="false"
    showCaption
    disableScroll
  )
  
</template>

<script>
import LightBox from 'vue-it-bigger';
import 'vue-it-bigger/dist/vue-it-bigger.min.css';
import InfiniteLoading from 'vue-infinite-loading';
import { mdiCircle, mdiPlus, mdiFormatListBulleted, mdiViewModule } from '@mdi/js';
import VueAspectRatio from 'vue-aspect-ratio';

import { getSetting } from '@/api/settings.api';
import { getCameras, getCameraSettings } from '@/api/cameras.api';
import { getNotifications } from '@/api/notifications.api';

import FilterCard from '@/components/filter.vue';
import VideoCard from '@/components/camera-card.vue';

import socket from '@/mixins/socket';

export default {
  name: 'Cameras',

  components: {
    LightBox,
    FilterCard,
    InfiniteLoading,
    VideoCard,
    'vue-aspect-ratio': VueAspectRatio,
  },

  mixins: [socket],

  beforeRouteLeave(to, from, next) {
    this.loading = true;
    next();
  },

  data: () => ({
    icons: {
      mdiCircle,
      mdiPlus,
      mdiFormatListBulleted,
      mdiViewModule,
    },

    cameras: [],
    loading: false,
    infiniteId: Date.now(),
    page: 1,
    query: '',

    rooms: [],
    camStates: [],

    backupHeaders: [],
    headers: [
      {
        text: 'Status',
        value: 'status',
        align: 'start',
        sortable: false,
        class: 'tw-py-3',
        cellClass: 'tw-py-3',
        width: '30px',
      },
      {
        text: '',
        value: 'preview',
        align: 'start',
        sortable: false,
        width: '100px',
        class: 'tw-px-1',
        cellClass: 'tw-px-0',
      },
      {
        text: 'Name',
        value: 'name',
        align: 'start',
        sortable: true,
        class: 'tw-pl-3 tw-pr-1',
        cellClass: 'tw-pl-3 tw-pr-1',
      },
      {
        text: 'Model',
        value: 'model',
        align: 'start',
        sortable: true,
        class: 'tw-pl-3 tw-pr-1',
        cellClass: 'tw-pl-3 tw-pr-1',
      },
      {
        text: 'Address',
        value: 'address',
        align: 'start',
        sortable: false,
        class: 'tw-pl-3 tw-pr-1',
        cellClass: 'tw-pl-3 tw-pr-1',
      },
      {
        text: 'Last Motion',
        value: 'lastNotification',
        align: 'start',
        sortable: true,
        class: 'tw-pl-3 tw-pr-1',
        cellClass: 'tw-pl-3 tw-pr-1',
      },
      {
        text: '',
        value: 'liveFeed',
        align: 'start',
        sortable: false,
        class: 'tw-pl-3 tw-pr-1',
        cellClass: 'tw-pl-3 tw-pr-1',
      },
    ],

    oldSelected: false,
    listMode: false,
    showListOptions: true,
  }),

  beforeDestroy() {
    ['resize', 'orientationchange'].forEach((event) => {
      window.removeEventListener(event, this.onResize);
    });
  },

  async mounted() {
    const response = await getSetting('general');
    this.rooms = response.data.rooms;
    this.listMode = this.oldSelected = localStorage.getItem('listModeCameras') === '1';
    this.backupHeaders = [...this.headers];

    this.loading = false;

    ['resize', 'orientationchange'].forEach((event) => {
      window.addEventListener(event, this.onResize);
    });

    this.onResize();
  },

  methods: {
    cameraStatus(data) {
      if (!this.camStates.some((cam) => cam.name === data.name)) {
        this.camStates.push(data);
      }
    },
    clickRow(item) {
      this.$router.push(`/cameras/${item.name}`);
    },
    changeListView(view) {
      localStorage.setItem('listModeCameras', view);
      this.listMode = this.oldSelected = view === 1;
    },
    filter(filterQuery) {
      this.loading = true;
      this.cameras = [];
      this.page = 1;
      this.query = filterQuery;
      this.infiniteId = Date.now();
      this.loading = false;
    },
    async infiniteHandler($state) {
      try {
        const response = await getCameras(`?pageSize=5&page=${this.page || 1}` + this.query);

        for (const camera of response.data.result) {
          const settings = await getCameraSettings(camera.name);
          camera.settings = settings.data;

          const lastNotification = await getNotifications(`?cameras=${camera.name}&pageSize=5`);
          camera.lastNotification = lastNotification.data.result.length > 0 ? lastNotification.data.result[0] : false;

          camera.url = camera.videoConfig.source.replace(/\u00A0/g, ' ').split('-i ')[1];

          if (!camera.url.startsWith('/')) {
            const protocol = camera.url.split('://')[0];
            const url = new URL(camera.url.replace(protocol, 'http'));
            camera.url = `${protocol}://${url.hostname}:${url.port || 80}${url.pathname}`;
          }
        }

        if (response.data.result.length > 0) {
          this.page += 1;
          this.cameras.push(...response.data.result);

          $state.loaded();
        } else {
          $state.complete();
        }
      } catch (err) {
        console.log(err);
        this.$toast.error(err.message);
      }
    },
    onResize() {
      const removeHeaders = [];

      if (this.windowWidth() < 415) {
        removeHeaders.push('model', 'address', 'lastNotification', 'liveFeed');
      } else if (this.windowWidth() < 650) {
        removeHeaders.push('model', 'address', 'lastNotification');
      } else if (this.windowWidth() <= 800) {
        removeHeaders.push('model', 'lastNotification');
      } else if (this.windowWidth() < 900) {
        removeHeaders.push('model');

        /*if (!this.toggleView) {
          this.toggleView = true;
          this.oldSelected = this.listMode;
        }

        this.showListOptions = false;
        this.listMode = false;*/
      } else {
        /*this.showListOptions = true;

        if (this.toggleView) {
          this.listMode = this.oldSelected;
          this.toggleView = false;
        }*/
      }

      let headers = [...this.backupHeaders];

      if (removeHeaders.length) {
        headers = headers.filter((header) => !removeHeaders.some((val) => header.value === val));
      }

      this.headers = headers;
    },
    windowWidth() {
      return window.innerWidth && document.documentElement.clientWidth
        ? Math.min(window.innerWidth, document.documentElement.clientWidth)
        : window.innerWidth ||
            document.documentElement.clientWidth ||
            document.getElementsByTagName('body')[0].clientWidth;
    },
  },
};
</script>

<style scoped>
.page-title {
  font-size: 1.3rem !important;
  letter-spacing: -0.025em !important;
  font-weight: 700 !important;
  line-height: 1.5 !important;
}

.header {
  display: flex;
}

div >>> .v-data-table-header__icon {
  display: none;
}
</style> -->


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
      streamSrc1: 'http://localhost:8000/stream1',
      streamSrc2: 'http://localhost:8000/stream2',
      streamSrc3: 'http://localhost:8000/stream3',
      streamSrc4: 'http://localhost:8000/stream4',
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
    // await this.checkStreamAvailability(`${this.streamSrc2}/available`, 'streamAvailable2');
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
      fetch('http://localhost:8000/camera-analytics')
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
