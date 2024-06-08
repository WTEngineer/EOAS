<template lang="pug">
.tw-px-auto.tw-py-5.tw-flex.tw-flex-wrap
  v-btn.save-btn(:class="fabAbove ? 'save-btn-top' : ''" v-scroll="onScroll" v-show="fab" color="success" transition="fade-transition" width="40" height="40" fab dark fixed bottom right @click="save" :loading="loadingProgress")
    v-icon {{ icons['mdiCheckBold'] }}
  v-btn.cancel-btn(:class="fabAbove ? 'cancel-btn-top' : ''" v-scroll="onScroll" v-show="fab" color="error" transition="fade-transition" width="40" height="40" fab dark fixed bottom right @click="() => {$router.push('/user-management') }" :loading="loadingProgress")
    v-icon {{ icons['mdiCloseThick'] }}
  v-dialog(v-model="showCam" max-width="800px")
    v-card
      v-card-title(v-if="!IDcardStatus" style="display: flex; justify-content: space-between") {{$t('camera_capture')}}
        v-icon(@click="captureCancel" color="error") {{ icons['mdiClose'] }}
      v-card-title(v-else="IDcardStatus" style="display: flex; justify-content: space-between") {{$t('id_card_detect')}}
        v-icon(@click="captureCancel" color="error") {{ icons['mdiClose'] }}
      v-card-text(v-if="!IDcardStatus")
        video(ref="video" width="640" height="480" autoplay style="border: 1px solid #000;")
        canvas(ref="canvas" width="640" height="480" style="display: none;")
      v-card-text(v-else="IDcardStatus")
        .tw-w-full
          .camera-box
            img(
              :src="idStream"
              alt="Camera Feed"
              class="camera-stream"
            )
      v-card-actions
        v-spacer
        v-btn(v-if="!IDcardStatus" color="success" @click="capture") {{$t('capture')}}
        v-btn(v-if="!IDcardStatus" color="success" @click="captureSave") {{$t('save')}}
  v-dialog(v-model="signatureModal" max-width="550px")
    v-card(height="350px")
      v-card-title(style="display: flex; justify-content: space-between") {{$t('signature')}}
        v-icon(@click="signatureModal=false" color="error") {{ icons['mdiClose'] }}
      v-card-text
        canvas(ref="signaturePadCanvas", width="500", height="200", style="border:1px solid #000;")
      v-card-actions(style="justify-content: flex-end")
        v-btn.tw-bg-green-500.tw-text-white(@click="saveSignature") {{$t('ok')}}
        v-btn.tw-bg-green-500.tw-text-white(@click="clearSignature" style="margin-left: 20px; margin-right: 8px") {{$t('clear')}}
  .tw-w-1-2
    .tw-flex.tw-flex.tw-items-center
      v-avatar(size="240" background-color="var(--cui-bg-card)" color="var(--cui-text-default)")
        v-img(v-on:error="handleErrorImg" :src="user.avatar" :alt="user.name" style="border: 1px solid #1a1a1a")
          template(v-slot:placeholder)
            .tw-flex.tw-justify-center.tw-items-center.tw-h-full
              v-progress-circular(indeterminate color="var(--cui-primary)" size="22")
      .tw-w-1-2.tw-mr-10.tw-px-2
        v-btn.tw-w-full.text-default.tw-my-2(@click="showCamModal" style="background: rgba(var(--cui-bg-default-rgb))") {{$t('camera')}}
        input(type="file" ref="fileInput" @change="uploadPicture" style="display: none;")
        v-btn.tw-w-full.text-default.tw-my-2(@click="triggerFileInput" style="background: rgba(var(--cui-bg-default-rgb))") {{$t('picture')}}
        v-btn.tw-w-full.text-default.tw-my-2(@click="showIDCamModal" style="background: rgba(var(--cui-bg-default-rgb))") {{$t('id')}}
        v-btn.tw-w-full.text-default.tw-my-2(@click="showSignatureModal" style="background: rgba(var(--cui-bg-default-rgb))") {{$t('signature')}}
        v-btn.tw-w-full.text-default.tw-my-2(style="background: rgba(var(--cui-bg-default-rgb))") {{$t('edit')}}

    .tw-w-full.tw-mt-8.tw-pr-20

      label.form-input-label {{$t('full_name')}}:
      v-text-field(v-model="user.name" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)

      .tw-flex
        .tw-w-1-3.tw-mr-2
          label.form-input-label {{$t('birthday')}}:
          v-text-field(v-model="user.birth" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)
        .tw-w-1-3.tw-mr-2
          label.form-input-label {{$t('age')}}:
          v-text-field(v-model="user.age" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)
        .tw-w-1-3
          label.form-input-label {{$t('status')}}:
          v-text-field(v-model="user.status" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo disabled)

      label.form-input-label {{$t('oasis_query')}}:
      v-textarea(v-model="oasisQuery" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo disabled)
      v-btn.tw-bg-gray-300.tw-text-black.tw-mt-2(disabled) {{$t('oasis_query')}}
  .tw-w-1-2
    v-tabs(v-model="tab"  background-color="var(--cui-bg-card)" color="var(--cui-text-default)" show-arrows)
      v-tab {{ $t('characteristics') }}
      v-tab {{ $t('agreement') }}

    v-tabs-items(v-model="tab")
      v-tab-item(:value="0")
        .tw-px-4
          .tw-flex.tw-flex-col.tw-mt-5
            label.form-input-label {{$t('gender')}}:
            v-select(v-model="user.gender" :items="genderOptions" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)

            label.form-input-label {{$t('guest_type')}}:
            v-select(v-model="user.guesttype" :items="guestTypeOptions" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)

            label.form-input-label {{$t('security_type')}}:
            v-select(v-model="user.safetytype" :items="securityTypeOptions" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)

            label.form-input-label {{$t('information')}}:
            v-textarea(v-model="user.info" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)

            label.form-input-label {{$t('blocked')}}:
            v-select(v-model="user.blocked" :items="blockedOptions" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)

            .tw-flex.tw-ml-10
              .tw-w-1-2.tw-mr-2
                label.form-input-label {{$t('from')}}:
                v-text-field(v-model="user.whenfrom" :label="$t('from')" type="date" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo :disabled="isBlockedDisabled")
              .tw-w-1-2
                label.form-input-label {{$t('to')}}:
                v-text-field(v-model="user.whento" :label="$t('to')" type="date" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo :disabled="isBlockedDisabled")

            .tw-mt-4
              label.form-input-label {{$t('location')}}:
              v-text-field.tw-w-full(v-model="user.location" :label="$t('location')" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)
            .tw-mt-4
              label.form-input-label {{$t('reason')}}:
              v-text-field(v-model="user.reason" :label="$t('reason')" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)
            .tw-mt-4
              label.form-input-label {{$t('type')}}:
              v-select(v-model="user.type" :items="typeOptions" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)

      v-tab-item(:value="1")
        .tw-px-4
          v-img(:src="sign", alt="Sample Image", width="100%", height="auto", style="border: 1px solid #000;")
          .tw-flex.tw-justify-end
            v-btn.text-default.tw-mt-2(style="margin-bottom: 20px; margin-right: 280px; background: rgba(var(--cui-bg-default-rgb))" ) {{$t('print')}}

</template>

<script>
import SignaturePad from 'signature_pad';
import api from '../../../api';
import { mdiCheckBold, mdiCloseThick, mdiClose } from '@mdi/js';
import axios from 'axios';

export default {
  data() {
    return {
      icons: {
        mdiCheckBold,
        mdiCloseThick,
        mdiClose
      },
      idStream: '',
      intervalId: '',
      sign: `http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/images/sample.jpg`,
      user: {},
      userId: '',
      oasisQuery: '',
      tab: 0,
      capturedImage: null,
      stream: null,
      genderOptions: [{
        text: this.$t('male'),
        value: 'Male'
      },
      {
        text: this.$t('female'),
        value: 'Female'
      }],
      guestTypeOptions: [
        {
          text: this.$t('not_assigned'),
          value: 'Not Assigned'
        },
        {
          text: this.$t('very_good_player'),
          value: 'Very Good Player'
        }, 
        {
          text: this.$t('good_player'),
          value: 'Good Player'
        }, 
        {
          text: this.$t('coffee_drinker'),
          value: 'Coffee Drinker'
        }
      ],
      securityTypeOptions: [
        {
          text: this.$t('not_assigned'),
          value: 'Not Assigned'
        },
        {
          text: this.$t('inconspicuous'),
          value: 'Inconspicuous'
        },
        {
          text: this.$t('suspicion_of_manipulation'),
          value: 'Suspicion Of Manipulation'
        },
        {
          text: this.$t('manipulator'),
          value: 'Manipulator'
        }
      ],
      blockedOptions: [{
        text: this.$t('yes'),
        value: 'Yes'
      },
      {
        text: this.$t('no'),
        value: 'No'
      }],
      typeOptions: [{
        text: this.$t('global'),
        value: 'Global'
      },
      {
        text: this.$t('local'),
        value: 'Local'
      }],
      agreementText: '',
      signatureModal: false,
      showCam: false,
      signaturePad: null,
      signaturePadOptions: {
        dotSize: 1.5,
        minWidth: 0.5,
        maxWidth: 2.5,
        penColor: 'black',
        backgroundColor: 'white'
      },
      fab: true,
      fabAbove: false,
    }
  },
  created() {
    const userId = this.$route.params.id;
    this.userId = userId;
    
    if (this.$route.params.id) {
      this.fetchUserData(userId);
    }
  },
  computed: {
    currentUser() {
      return this.$store.state.users.user || {};
    },
    isBlockedDisabled() {
      return this.user.blocked === 'No';
    }
  },

  watch: {
    currentUser: {
      handler(newValue) {
        console.log('crrr');
        console.log(newValue);
        this.user = { ...newValue };
      },
      deep: true,
    },
    IDcardStatus: {
      handler(newValue) {
        console.log('ID card status');
        console.log(newValue);
      }
    },
    // showCam(val) {
    //   if (val) {
    //     this.startCamera();
    //   } else {
    //     this.stopCamera();
    //   }
    // }
  },
  async beforeDestroy() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
    await axios.get(`http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/api/camera/camera_1/off`);
    await axios.get(`http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/api/camera/camera_2/off`);
    // await axios.get(`http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/api/camera/camera_3/off`);
    // await axios.get(`http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/api/camera/camera_4/off`);
  },
  methods: {
    onScroll(e) {
      if (typeof window === 'undefined') {
        this.fabAbove = true;
        return;
      }

      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fabAbove = top > 20;
    },
    async startCamera() {
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({ video: true });
        this.$refs.video.srcObject = this.stream;
      } catch (err) {
        console.error('Error accessing camera: ', err);
      }
    },
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    capture() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      this.capturedImage = canvas.toDataURL('image/png');
    },
    captureSave() {
      this.stopCamera();
      this.user = {...this.user, avatar: this.capturedImage};
      this.showCam = false;
    },
    async captureCancel() {
      if (this.IDcardStatus) {
        if (this.intervalId) {
         clearInterval(this.intervalId);
        }
        await axios.get(`http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/api/camera/camera_1/off`);
        await axios.get(`http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/api/camera/camera_2/off`);
        // await axios.get(`http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/api/camera/camera_3/off`);
        // await axios.get(`http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/api/camera/camera_4/off`);
      }
      this.stopCamera();
      this.showCam = false;
    },
    stopCamera() {
      if (this.stream) {
        const tracks = this.stream.getTracks();
        tracks.forEach(track => track.stop());
      }
    },
    showCamModal() {
      this.startCamera();
      this.IDcardStatus = false;
      this.showCam = true;
    },
    showIDCamModal() {
      this.IDcardStatus = true;
      this.showCam = true;
      this.idStream = `http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/id-analytics/stream`;
      this.intervalId = setInterval(this.fetchAnalyticsData, 1000);
      // fetch(`http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/id-analytics`)
      //   .then(response => response.json())
      //   .then(data => {
      //     console.log('ID data');
      //     console.log(data);
      //     this.user = {...this.user, ...data};
      //     this.showCam = false;
      //   })
      //   .catch(error => console.error('Error fetching id analytics data:', error));
    },
    fetchAnalyticsData() {
      fetch(`http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/id-analytics`)
        .then(response => response.json())
        .then(data => {
          console.log(data.name);
          if (data && data.name) {
            this.user = {...this.user, ...data};
          }
        })
        .catch(error => console.error('Error fetching analytics data:', error));
    },
    save() {
      console.log(this.user);
      if (this.userId) {
        this.user['id'] = this.userId;
        this.$store.dispatch('users/editUser', this.user);
      } else {
        this.$store.dispatch('users/addUser', this.user);
      }
      this.$router.push('/user-management');
    },
    cancel() {
      this.$router.push(-1);
    },
    uploadPicture(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const res = e.target.result;
          this.user = {...this.user, avatar: res};
        };
        reader.readAsDataURL(file);
      }
    },
    showSignatureModal() {
      this.signatureModal = true;
      this.$nextTick(() => {
        if (!this.signaturePad) {
          const canvas = this.$refs.signaturePadCanvas;
          this.signaturePad = new SignaturePad(canvas, {
            penColor: 'black'
          });
        }
      });
    },
    clearSignature() {
      if (this.signaturePad) {
        this.signaturePad.clear();
      }
    },
    async saveSignature() {
      if (this.signaturePad) {
        const signatureData = this.signaturePad.toDataURL();
        // Handle the saved signature data (e.g., save to user profile)
        console.log(signatureData);
        const response = await api.post('/signature', { data: signatureData });
        console.log(response.data);
        this.sign = response.data.data;
        this.signatureModal = false;
      }
    },
    async fetchUserData(id) {
      console.log(id);
      await this.$store.dispatch('users/getUser', id);
      this.sign = `http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/images/${this.user.name}.jpg`;
    },
    handleErrorImg() {
      // Handle image error
    }
  }
}
</script>

<style scoped>
.camera-box {
  width: 560px;
  height: 400px;
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

.tw-w-1-2 {
  width: 50%;
}

.tw-w-1-3 {
  width: 33.3%;
}

.save-btn {
  right: 30px !important;
  bottom: 95px !important;
  z-index: 11 !important;
  transition: 0.3s all;
}

.save-btn-top {
  bottom: 145px !important;
}

.cancel-btn {
  right: 30px !important;
  bottom: 45px !important;
  z-index: 11 !important;
  transition: 0.3s all;
}

.cancel-btn-top {
  bottom: 95px !important;
}
</style>
