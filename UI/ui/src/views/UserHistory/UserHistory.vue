<template lang="pug">
.tw-flex.tw-justify-center.tw-items-center.page-loading(v-if="loading")
  v-progress-circular(indeterminate color="var(--cui-primary)")
.tw-py-6.tw-px-4(v-else)
  .tw-flex.tw-relative.pl-safe.pr-safe

    Sidebar(camerasSelect datePicker labelSelect roomSelect typeSelect @filter="filter")
    .filter-content.filter-included.tw-w-full.tw-relative
      .tw-w-full.tw-flex.tw-flex-wrap.tw-justify-start.tw-flex-start
        v-row.tw-w-full
          v-col.tw-px-2.tw-py-2(cols="4" v-for="user in users" :key="user.id")
            .tw-bg-white.tw-shadow.tw-rounded-lg.tw-overflow-hidden.tw-mx-2.tw-my-4.tw-max-w-xs(style="padding: 0 20px")
              .tw-w-full.tw-text-center.tw-mb-4
                v-avatar.tw-mt-5(size="120" color="#121212")
                  v-img(v-on:error="handleErrorImg" :src="user.avatar? user.avatar: 'http://localhost:8000/images/camera.png'" :alt="user.name" style="border: 1px solid #1a1a1a")
                    template(v-slot:placeholder)
                      .tw-flex.tw-justify-center.tw-items-center.tw-h-full
                        v-progress-circular(indeterminate color="var(--cui-primary)" size="22")
              .tw-w-full.tw-px-10
              .tw-flex.tw-w-full.tw-text-sm.tw-leading-1.tw-text-gray-500
                .tw-w-1-2.tw-text-left {{ $t('name') }}:
                .tw-w-1-2.tw-text-left.tw-pl-2 {{ user.name }}
              .tw-flex.tw-w-full.tw-text-sm.tw-leading-1.tw-text-gray-500
                .tw-w-1-2.tw-text-left {{ $t('time') }}:
                .tw-w-1-2.tw-text-left.tw-pl-2 {{ user.time }}
              .tw-flex.tw-w-full.tw-text-sm.tw-leading-1.tw-text-gray-500
                .tw-w-1-2.tw-text-left {{ $t('place') }}:
                .tw-w-1-2.tw-text-left.tw-pl-2 {{ user.place }}
              .tw-flex.tw-w-full.tw-text-sm.tw-leading-1.tw-text-gray-500
                .tw-w-1-2.tw-text-left {{ $t('view') }}:
                .tw-w-1-2.tw-text-left.tw-pl-2 {{ user.view }}
              .tw-flex.tw-w-full.tw-text-sm.tw-leading-1.tw-text-gray-500
                .tw-w-1-2.tw-text-left {{ $t('action') }}:
                .tw-w-1-2.tw-text-left.tw-pl-2 {{ user.action }}
        infinite-loading(:identifier="infiniteId" @infinite="infiniteHandler")
  LightBox(
    ref="lightbox"
    :media="images"
    :showLightBox="false"
    :showThumbs="false"
    showCaption
    disableScroll
  )

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
import { mdiDelete, mdiDownload, mdiFilter, mdiFormatListBulleted, mdiViewModule } from '@mdi/js';
import { saveAs } from 'file-saver';
import VueAspectRatio from 'vue-aspect-ratio';

import { removeRecording, removeRecordings } from '@/api/recordings.api';

import { bus } from '@/main';

import FilterCard from '@/components/filter.vue';
import RecordingCard from '@/components/recording-card.vue';
import Sidebar from '@/components/sidebar-filter.vue';

import socket from '@/mixins/socket';
import { getUserHistory } from '../../api/users.api';

export default {
  name: 'User history',

  components: {
    FilterCard,
    InfiniteLoading,
    LightBox,
    RecordingCard,
    Sidebar,
    'vue-aspect-ratio': VueAspectRatio,
  },

  mixins: [socket],

  beforeRouteLeave(to, from, next) {
    this.loading = true;
    next();
  },

  data() {
    return {
      users: [],
      originalData: [],
      icons: {
        mdiDelete,
        mdiDownload,
        mdiFilter,
        mdiFormatListBulleted,
        mdiViewModule,
      },
      images: [],
      infiniteId: Date.now(),
      loading: false,
      page: 1,
      query: '',
      selectedFilter: [],
      recordings: [],
      totalRecordings: 0,
      showOverlay: false,

      listMode: false,
      showListOptions: true,
      toggleView: false,
      oldSelected: false,

      selected: [],

      backupHeaders: [],
      headers: [
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
          text: this.$t('camera'),
          value: 'camera',
          align: 'start',
          sortable: true,
          class: 'tw-pl-3 tw-pr-1',
          cellClass: 'tw-pl-3 tw-pr-1',
        },
        {
          text: this.$t('type'),
          value: 'recordType',
          align: 'start',
          sortable: true,
          class: 'tw-py-3',
          cellClass: 'tw-py-3',
        },
        {
          text: this.$t('time'),
          value: 'time',
          align: 'start',
          sortable: true,
          class: 'tw-px-1',
          cellClass: 'tw-px-1',
        },
        {
          text: this.$t('label'),
          value: 'label',
          align: 'start',
          sortable: true,
          class: 'tw-px-1',
          cellClass: 'tw-px-1',
        },
        {
          text: '',
          value: 'download',
          align: 'start',
          sortable: false,
          width: '80px',
          class: 'tw-py-1',
          cellClass: 'tw-py-1',
        },
      ],

      diskload: {},
    };
  },

  watch: {
    query: {
      handler() {
        this.selectedFilter = this.query.split('&').filter((query) => query);
        if (this.selectedFilter.length >= 2) {
          const from = this.selectedFilter[0].split('=')[1];
          const to = this.selectedFilter[1].split('=')[1];
          const updatedHistory = this.originalData.filter(row => row.time >= from && row.time < to + 1);
          this.users = updatedHistory;
        }
        else {
          this.users = this.originalData;
        }
      },
    },
  },

  async created() {
    this.fetchHistory();
    bus.$on('showFilterOverlay', this.triggerFilterOverlay);
  },

  beforeDestroy() {
    bus.$off('showFilterOverlay', this.triggerFilterOverlay);

    ['resize', 'orientationchange'].forEach((event) => {
      window.removeEventListener(event, this.onResize);
    });
  },

  async mounted() {
    this.backupHeaders = [...this.headers];
    this.listMode = this.oldSelected = localStorage.getItem('listModeRecordings') === '1';

    this.loading = false;

    ['resize', 'orientationchange'].forEach((event) => {
      window.addEventListener(event, this.onResize);
    });

    this.onResize();
  },

  methods: {
    clickRow(data) {
      if (this.downloading) {
        return;
      }

      if (this.selected.find((item) => item.id === data.id)) {
        this.selected = this.selected.filter((item) => item.id !== data.id);
      } else {
        this.selected.push(data);
      }
    },
    handleErrorImg() {
      this.user.avatar = 'http://localhost:8000/images/camera.png'
      // Handle image error
    },
    changeListView(view) {
      localStorage.setItem('listModeRecordings', view);
      this.listMode = this.oldSelected = view === 1;
    },
    download({ url, fileName }) {
      this.downloading = true;

      const isSafari = navigator.appVersion.indexOf('Safari/') !== -1 && navigator.appVersion.indexOf('Chrome') === -1;

      const downloadFinished = () => {
        setTimeout(() => (this.downloading = false), 1000);
      };

      if (isSafari) {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.responseType = 'blob';

        xhr.onload = function () {
          saveAs(xhr.response, fileName);
          downloadFinished();
        };

        xhr.onerror = function () {
          console.error('download failed', url);
          this.$toast.error(`${this.$t('download_failed')}`);
          downloadFinished();
        };

        xhr.send();
        return;
      }

      // Create download link.
      const link = document.createElement('a');

      if (fileName) {
        link.download = fileName;
      }

      link.href = url;
      link.style.display = 'none';

      document.body.appendChild(link);

      // Start download.
      link.click();

      // Remove download link.
      document.body.removeChild(link);

      downloadFinished();
    },
    filter(filterQuery) {
      if (this.query !== filterQuery) {
        this.loading = true;
        this.recordings = [];
        this.page = 1;
        this.query = filterQuery;
        this.infiniteId = Date.now();
        this.loading = false;
      }
    },
    async fetchHistory() {
      try {
        const response = await getUserHistory(`?pageSize=8&page=${this.page}` + this.query);
        const newData = response.data.result;
        this.users = [...this.users, ...newData];
        this.originalData = [...this.originalData, ...newData];
      } catch (error) {
        console.error(error);
        this.$toast.error(error.message);
      }
    },
    async infiniteHandler($state) {
      try {
        if (this.selectedFilter.length) {
          const from = this.selectedFilter[0].split('=')[1];
          const to = this.selectedFilter[1].split('=')[1];
          const response = await getUserHistory(`?pageSize=8&page=${this.page}&from=${from}&to=${to + 1}`);
          if (response.data.result.length) {
            this.page += 1;
            this.users = [...this.users, ...response.data.result];
            this.originalData = [...this.originalData, ...response.data.result];
            $state.loaded();
          } else {
            $state.complete();
          }
        } else {
          const response = await getUserHistory(`?pageSize=8&page=${this.page}` + this.query);
          if (response.data.result.length) {
            this.page += 1;
            this.users = [...this.users, ...response.data.result];
            this.originalData = [...this.originalData, ...response.data.result];
            $state.loaded();
          } else {
            $state.complete();
          }
        }

      } catch (error) {
        console.error(error);
        this.$toast.error(error.message);
        $state.complete();
      }
    },
    openGallery(item) {
      const index = this.recordings.findIndex((recording) => recording.id === item.id);
      this.$refs.lightbox.showImage(index);
    },
    onResize() {
      const removeHeaders = [];

      if (this.windowWidth() < 350) {
        removeHeaders.push('time', 'label', 'recordType', 'download');
      } else if (this.windowWidth() < 415) {
        removeHeaders.push('time', 'label', 'recordType');
      } else if (this.windowWidth() <= 550) {
        removeHeaders.push('time', 'label');
      } else if (this.windowWidth() < 605) {
        removeHeaders.push('time');

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
    selectAllRecordings() {
      if (this.recordings.length && this.selected.length === this.recordings.length) {
        this.selected = [];
      } else {
        this.selected = this.recordings.map((recording) => recording);
      }
    },
    async remove() {
      if (!this.selected.length) {
        return;
      }

      if (this.selected.length === this.recordings.length) {
        this.removeAll();
      }

      for (const recording of this.selected) {
        try {
          await removeRecording(recording.id, '?refresh=true');

          const index = this.recordings.findIndex((rec) => rec.id === recording.id);

          this.selected = this.selected.filter((rec) => rec.id !== recording.id);
          this.recordings = this.recordings.filter((rec) => rec.id !== recording.id);

          this.images = this.images.filter((image, i) => i !== index);
          this.$toast.success(`${this.$t('recording')} ${this.$t('removed')}!`);

          this.totalRecordings--;
        } catch (err) {
          console.log(err);
          this.$toast.error(err.message);

          return;
        }
      }
    },
    async removeAll() {
      try {
        await removeRecordings();

        this.selected = [];
        this.recordings = [];
        this.images = [];
        this.$toast.success(this.$t('all_recordings_removed'));

        this.totalRecordings = 0;
      } catch (err) {
        console.log(err);
        this.$toast.error(err.message);
      }
    },
    triggerFilterOverlay(state) {
      this.showOverlay = state;
    },
    toggleFilterNavi() {
      this.showOverlay = true;
      bus.$emit('showFilterNavi', true);
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
  margin-left: 5px;
}

div>>>.theme--light.v-expansion-panels .v-expansion-panel-header .v-expansion-panel-header__icon .v-icon {
  color: rgba(var(--cui-text-default-rgb)) !important;
}

.theme--light.v-btn.v-btn--disabled,
.theme--light.v-btn.v-btn--disabled .v-icon,
.theme--light.v-btn.v-btn--disabled .v-btn__loading {
  color: var(--cui-text-disabled) !important;
}

div>>>.v-btn--fab.v-btn--absolute,
div>>>.v-btn--fab.v-btn--fixed {
  z-index: 0 !important;
}

.header {
  display: flex;
}

.subtitle {
  color: rgba(var(--cui-text-third-rgb)) !important;
}

.overlay {
  background-color: #000 !important;
  border-color: #000 !important;
  opacity: 0.6;
  z-index: 1;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  /*left: -1rem;
    right: -1.5rem;
    top: -1.5rem;
    bottom: -1.5rem;*/
}

@media (min-width: 1280px) {
  .overlay {
    display: none;
  }

  .filter-nav-toggle {
    display: none !important;
  }

  .filter-content {
    margin-left: 320px;
  }
}

div>>>.v-data-table-header__icon {
  display: none;
}

@media (max-width: 600px) {
  div>>>.v-data-table__mobile-row__header {
    display: none !important;
  }

  div>>>.v-data-table__mobile-row__cell,
  div>>>.v-data-table__mobile-row__cell .vue-aspect-ratio {
    width: 100% !important;
    margin: 0 !important;
    position: relative;
    top: -30px;
    margin-bottom: -10px !important;
  }
}

.vue-aspect-ratio>>>.v-input--selection-controls__input .v-icon__svg {
  fill: #626262 !important;
}

.header-utils>>>.v-badge__badge,
.header-title>>>.v-badge__badge {
  font-size: 8px !important;
  line-height: 1.2 !important;
  border: 2px solid var(--cui-bg-default) !important;
  color: #fff !important;
}

.v-alert {
  padding: 10px !important;
}

div>>>.v-simple-checkbox .v-input--selection-controls__input {
  margin: 0 !important;
}

div>>>.v-data-table .v-input:not(.v-input--is-focused):not(.v-input--switch):not(.v-input--checkbox)>.v-input__control>.v-input__slot,
div>>>.v-data-table .v-input:not(.v-input--has-state):not(.v-input--switch):not(.v-input--checkbox)>.v-input__control>.v-input__slot {
  border: none !important;
}

div>>>.v-input--selection-controls__input svg {
  fill: var(--cui-text-hint) !important;
}

.tw-w-1-2 {
  width: 50%;
}

@media (min-width: 400px) {
  .tw-w-1-4 {
    width: 100%;
  }
}

@media (min-width: 600px) {
  .tw-w-1-4 {
    width: 50%;
  }
}

@media (min-width: 1400px) {
  .tw-w-1-4 {
    width: 25%;
  }
}
</style>
