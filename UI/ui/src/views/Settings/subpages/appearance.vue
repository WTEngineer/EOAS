<template lang="pug">
.tw-flex.tw-justify-center.tw-items-center.page-loading(v-if="loading")
  v-progress-circular(indeterminate color="var(--cui-primary)")
.tw-py-6.tw-px-4(v-else)
  .tw-flex.tw-relative.pl-safe.pr-safe
    v-btn.save-btn(:class="fabAbove ? 'save-btn-top' : ''" v-scroll="onScroll" v-show="fab" color="success" transition="fade-transition" width="80" height="40" fab dark fixed bottom right @click="save" :loading="loadingProgress" style="border-radius: 10px") {{ $t('save') }}
    v-btn.cancel-btn(:class="fabAbove ? 'cancel-btn-top' : ''" v-scroll="onScroll" v-show="fab" color="error" transition="fade-transition" width="80" height="40" fab dark fixed bottom right @click="reset" :loading="loadingProgress" style="border-radius: 10px") {{ $t('default') }}
    .tw-w-full.tw-mx-2
      v-progress-linear.loader(:active="loadingProgress" :indeterminate="loadingProgress" fixed top color="var(--cui-primary)")

      .tw-mb-7.tw-mt-5(v-if="!loading")
        <!-- .page-subtitle {{ $t('theme') }} -->
        .page-subtitle {{ $t('interface_appearance') }}

        .tw-w-full.tw-mx-2.tw-mt-4
          label.form-input-label {{ $t('camera') }}
          v-select(v-model="appearance.cameraView" :items="cameraViews" prepend-inner-icon="mdi-webcam" background-color="var(--cui-bg-card)" required solo)
            template(v-slot:prepend-inner)
              v-icon.text-muted {{ icons['mdiWebcam'] }}
          label.form-input-label {{ $t('location') }}
          v-text-field(v-model="appearance.location" label="" :type="text" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)
            template(v-slot:prepend-inner)
              v-icon.text-muted {{ icons['mdiMapMarker'] }}
          label.form-input-label {{ $t('mode') }}
          v-select(v-model="appearance.mode" :items="modes" prepend-inner-icon="mdi-theme-light-dark" background-color="var(--cui-bg-card)" required solo)
            template(v-slot:prepend-inner)
              v-icon.text-muted {{ icons['mdiThemeLightDark'] }}

          label.form-input-label {{ $t('color') }}
          v-select(v-model="appearance.color" :items="colors" prepend-inner-icon="mdi-palette" background-color="var(--cui-bg-card)" required solo)
            template(v-slot:prepend-inner)
              v-icon.text-muted {{ icons['mdiPalette'] }}

        v-divider.tw-mt-4.tw-mb-8

        .page-subtitle {{ $t('network_setting') }}
        .tw-w-full.tw-mx-2.tw-mt-4.tw-mb-8 
          label.form-input-label {{ $t('address') }}
          v-text-field(v-model="appearance.ipAddress" label="127.0.0.1" prepend-inner-icon="mdi-ip-network" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" required solo)
            template(v-slot:prepend-inner)
              v-icon.text-muted {{ icons['mdiIpNetwork'] }}
          label.form-input-label {{ $t('username') }}
          v-text-field(v-model="appearance.username" label="root" prepend-inner-icon="mdi-account" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" required solo)
            template(v-slot:prepend-inner)
              v-icon.text-muted {{ icons['mdiAccount'] }}
          label.form-input-label {{ $t('password') }}
          v-text-field(v-model="appearance.password" label="******"  :type="showPassword ? 'text' : 'password'" :append-icon="showPassword ? icons['mdiEye'] : icons['mdiEyeOff']" @click:append="showPassword = !showPassword" prepend-inner-icon="mdi-key-variant" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" required solo)
            template(v-slot:prepend-inner)
              v-icon.text-muted {{ icons['mdiKeyVariant'] }}

        v-divider.tw-mt-4.tw-mb-8

        .page-subtitle {{ $t('interface_language') }}

        .tw-w-full.tw-mx-2.tw-mt-4.tw-mb-8
          label.form-input-label {{ $t('language') }}
          v-select(v-model="appearance.lang" :items="langs" prepend-inner-icon="mdi-translate" background-color="var(--cui-bg-card)" required solo)
            template(v-slot:prepend-inner)
              v-icon.text-muted {{ icons['mdiTranslate'] }}

</template>

<script>
import { mdiPalette, mdiThemeLightDark, mdiTranslate, mdiWebcam, mdiMapMarker, mdiAccount, mdiEye, mdiEyeOff, mdiKeyVariant, mdiIpNetwork } from '@mdi/js';
import Sidebar from '@/components/sidebar-settings.vue';

export default {
  name: 'AppearanceSettings',
  components: {
    Sidebar,
  },

  beforeRouteLeave(to, from, next) {
    this.loading = true;
    this.loadingProgress = true;
    next();
  },

  data() {
    return {
      icons: { mdiPalette, mdiThemeLightDark, mdiTranslate, mdiWebcam, mdiMapMarker, mdiAccount, mdiEye, mdiEyeOff, mdiKeyVariant, mdiIpNetwork },
      showPassword: false,
      loading: false,
      fab: true,
      fabAbove: false,
      appearance: {},
      loadingProgress: false,
      defaultAppearance: {
        color: 'pink',
        lang: 'en',
        mode: 'dark',
        cameraView: 'second',
        username: 'root',
        location: 'xxx',
        ipAddress: '127.0.0.1',
        password: '1234'
      },

      modes: [
        {
          text: this.$t('dark'),
          value: 'dark',
        },
        {
          text: this.$t('light'),
          value: 'light',
        },
        {
          text: this.$t('auto'),
          value: 'auto',
        },
      ],
      cameraViews: [
        {
          text: this.$t('1 * 1'),
          value: 'first',
        },
        {
          text: this.$t('2 * 2'),
          value: 'second',
        },
      ],
      colors: [
        {
          text: 'blue',
          value: 'blue',
        },
        {
          text: 'blgray',
          value: 'blgray',
        },
        {
          text: 'brown',
          value: 'brown',
        },
        {
          text: 'green',
          value: 'green',
        },
        {
          text: 'gray',
          value: 'gray',
        },
        {
          text: 'orange',
          value: 'orange',
        },
        {
          text: 'pink',
          value: 'pink',
        },
        {
          text: 'purple',
          value: 'purple',
        },
      ],
      langs: [
        {
          text: 'English',
          value: 'en',
        },
        {
          text: 'German',
          value: 'de',
        },
      ],
    };
  },

  computed: {
    uiConfig() {
      return this.$store.state.config.ui;
    },
  },

  async created() {
    this.reset();

    this.appearance.cameraView = localStorage.getItem('cameraView') || 'second';
    this.appearance.color = localStorage.getItem('theme-color') || 'pink';
    this.appearance.lang = localStorage.getItem('language') || 'pink';
    this.appearance.mode =
      localStorage.getItem('darkmode') === 'auto' ? 'auto' : localStorage.getItem('theme') || 'light';

    // this.$watch('appearance', this.appearanceWatcher, { deep: true });

    this.loading = false;
    this.loadingProgress = false;
  },

  watch: {
    appearance: {
      handler(newValue) {
        console.log(newValue);
        this.appearanceWatcher(newValue);
        this.loading = false;
      this.loadingProgress = false;
      },
      deep: true,
    },
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
    reset() {
      this.appearance = { ...this.defaultAppearance };
    },
    async appearanceWatcher(newValue) {
      this.loadingProgress = true;
      console.log('appearance changed');
      console.log(newValue);

      const autoMode = newValue.mode === 'auto';
      let mode = newValue.mode;
      let color = newValue.color;

      if (autoMode) {
        localStorage.setItem('darkmode', 'auto');

        mode = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', this.matchMediaListener);
      } else {
        localStorage.setItem('darkmode', 'manual');

        window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', this.matchMediaListener);
      }

      const theme = `${mode}-${color}`;
      this.$store.commit('config/setTheme', theme);

      this.$store.commit('config/setCameraView', newValue.cameraView);

      const lang = newValue.lang;
      this.$store.commit('config/setLang', lang);
      this.loading = false;
      this.loadingProgress = false;
    },
    matchMediaListener(event) {
      const autoDarkmode = localStorage.getItem('darkmode') === 'auto';

      if (autoDarkmode) {
        if (event.matches) {
          localStorage.setItem('theme', 'dark');
          document.documentElement.setAttribute('data-theme', 'dark');
        } else {
          localStorage.setItem('theme', 'light');
          document.documentElement.setAttribute('data-theme', 'light');
        }
      }
    },
    save() {
      console.log(this.cameraView);
      
    }
  },
};
</script>

<style scoped>
.tw-container {
  max-width: 1200px;
}

.tw-w-1-2 {
  width: 50%;
}

.tw-w-1-3 {
  width: 33.3%;
}

.tw-w-1-8 {
  width: 12.5%;
}

.tw-w-7-8 {
  width: 87.5%;
}

.rightButtonsGroup {
  background-color: #fff;
  border-radius: 5px;
  border-color: rgba(229, 231, 235, var(--tw-border-opacity));
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
