<template lang="pug">
.tw-relative(style="z-index: 99")
  .top-navi-bar-minified(v-if="$route.meta.config.showMinifiedNavbar")
    v-btn.text-muted.included(@click="toggleNavi" fab elevation="1" height="38px" width="38px" color="rgba(0, 0, 0, 0.5)" retain-focus-on-click)
      v-icon {{ showSidebar ? icons['mdiArrowLeftThick'] : icons['mdiArrowRightThick'] }}
  v-app-bar.top-navi-bar.pt-safe(v-else height="64px" :class="($route.meta.config.fixedNavbar ? 'top-navi-bar-fixed ' : '') + (extendSidebar ? 'extended-sidebar' : '')" style="border-top: 1px solid rgba(121,121,121,0.1);")
    .navi-wrap.pl-safe.pr-safe
      v-btn.text-default.included(@click="toggleNavi" icon height="38px" width="38px")
        v-icon {{ icons['mdiMenu'] }}
      .text-default {{$t('EOAS - Echtzeit Oasis Abfrge System')}}
      .tw-flex
        v-menu.included.tw-z-30(v-model="showProfileMenu" transition="slide-y-transition" min-width="220px" :close-on-content-click="false" offset-y bottom left nudge-top="-15" z-index="999" content-class="light-shadow")
          template(v-slot:activator="{ on, attrs }")
            v-btn.text-default(icon height="38px" width="38px" v-bind="attrs" v-on="on")
              v-icon {{ icons['mdiAccount'] }}
          v-card.included.light-shadow.card-border.dropdown-content(min-width="220px" max-width="260px")
            v-list-item.tw-px-6.tw-py-3.profile-menu-header.dropdown-title
              v-list-item-action.tw-m-0
                v-avatar(size="40" color="black")
                  v-img(v-on:error="handleErrorImg" :src="avatarSrc" :alt="currentUser.username")
                    template(v-slot:placeholder)
                      .tw-flex.tw-justify-center.tw-items-center.tw-h-full
                        v-progress-circular(indeterminate color="var(--cui-primary)" size="16")
              v-list-item-content.tw-ml-3
                v-list-item-title
                  .text-left.tw-text-sm.tw-font-medium {{ currentUser.username }}
                  .text-left.tw-text-xs.tw-font-light.text-muted {{ currentUser.permissionLevel && currentUser.permissionLevel.includes("admin") ? $t("master") : $t("user") }}
            v-divider
            v-card-text.tw-py-3.tw-px-5.text-center
              v-list.dropdown-content(dense)
                v-list-item-group
                  v-list-item(@click="() => { hideNavi(); $router.push('/settings/appearance') }")
                    v-list-item-icon.tw-mr-4
                      v-icon.touch-button-icon-light-nohover {{ icons['mdiAccountOutline'] }}
                    v-list-item-content.text-left
                      v-list-item-title.tw-text-xs.tw-font-medium.touch-button-icon-light-nohover {{ $t('settings') }}
                 
            v-divider
            v-card-text.tw-py-1.tw-px-5.text-center
              v-list.dropdown-content(dense flat)
                v-list-item-group
                  v-list-item(@click="signout")
                    v-list-item-icon.tw-mr-4
                      v-icon.touch-button-icon-light-nohover {{ icons['mdiLogoutVariant'] }}
                    v-list-item-content.text-left
                      v-list-item-title.tw-text-xs.tw-font-medium.touch-button-icon-light-nohover {{ $t('signout') }}
</template>

<script>
import {
  mdiArrowLeftThick,
  mdiArrowRightThick,
  mdiMenu,
  mdiAccount,
  mdiAccountOutline,
  mdiLogoutVariant,
  mdiBell,
  mdiTune,
} from '@mdi/js';

import { bus } from '@/main';

export default {
  name: 'Navbar',

  data: () => ({
    avatarSrc: '',
    extendSidebar: false,
    icons: {
      mdiArrowLeftThick,
      mdiArrowRightThick,
      mdiBell,
      mdiMenu,
      mdiAccount,
      mdiAccountOutline,
      mdiLogoutVariant,
      mdiTune,
    },
    showSidebar: false,
    showNotificationsMenu: false,
    showProfileMenu: false,
  }),

  computed: {
    notSize() {
      return this.$store.state.notifications.size;
    },
    currentUser() {
      return this.$store.state.auth.user || {};
    },
  },
  watch: {
    currentUser: {
      handler(newValue) {
        if (newValue?.photo) {
          this.avatarSrc = `/files/${newValue.photo}?rnd=${new Date()}`;
        }
      },
      deep: true,
    },
    '$route.path': {
      handler() {
        if (this.showSidebar) {
          this.hideNavi();
        }
      },
    },
  },

  created() {
    bus.$on('extendSidebar', this.triggerSidebar);
    if (this.currentUser.photo && this.currentUser.photo !== 'no_img.png') {
      this.avatarSrc = `/files/${this.currentUser.photo}`;
    } else {
      this.avatarSrc = require('../assets/img/no_user.png');
    }
  },

  beforeDestroy() {
    bus.$off('extendSidebar', this.triggerSidebar);
  },

  methods: {
    triggerSidebar(state) {
      this.showSidebar = state;

      if (this.$route.meta.config.fixedNavbar) {
        this.extendSidebar = state;

        setTimeout(() => {
          this.scrollNavi();
        }, 300);
      } else {
        this.extendSidebar = false;
      }
    },
    toggleNavi() {
      bus.$emit('showSidebar', true);
      bus.$emit('showOverlay', true);

      setTimeout(() => {
        this.scrollNavi();
      }, 300);
    },
    scrollNavi() {
      const activeNav = document.querySelector('.sidebar-nav-item-active');
      const mainNavi = this.$route.meta.config.showMinifiedNavbar
        ? document.querySelector('.minified-navi')
        : document.querySelector('.main-navi');

      if (activeNav && mainNavi) {
        this.$vuetify.goTo(activeNav, {
          container: mainNavi,
          duration: 250,
          offset: 50,
          easing: 'easeInOutCubic',
        });
      }
    },
    handleErrorImg() {
      this.avatarSrc = require('../assets/img/no_user.png');
    },
    hideNavi() {
      this.showSidebar = this.showSidebarContent = this.showProfileMenu = false;
      this.showSidebarMinifiedNav = true;

      bus.$emit('showOverlay', false);
      bus.$emit('extendSidebar', false);
    },
    async signout() {
      this.hideNavi();

      await this.$store.dispatch('auth/logout');
      setTimeout(() => this.$router.push('/'), 200);
    },
  },
};
</script>

<style scoped>
span>>>.v-badge__badge::after {
  border-color: rgba(var(--cui-bg-app-bar-rgb)) !important;
}

.navi-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.top-navi-bar-minified {
  position: absolute !important;
  height: calc(env(safe-area-inset-top, 0px) + 64px) !important;
  padding-top: calc(env(safe-area-inset-top, 0px) + 1rem) !important;
  padding-left: calc(env(safe-area-inset-left, 0px) + 1rem) !important;
}

.top-navi-bar {
  transition: 0.3s all;
  height: calc(env(safe-area-inset-top, 0px) + 64px) !important;
  background: rgba(var(--cui-bg-app-bar-rgb)) !important;
  box-shadow: 0px 3px 3px -2px rgb(0 0 0 / 15%), 0px 3px 4px 0px rgb(0 0 0 / 1%), 0px 1px 8px 0px rgb(0 0 0 / 1%) !important;
  border-bottom: 1px solid rgba(var(--cui-bg-app-bar-border-rgb)) !important;
}

.top-navi-bar-fixed {
  margin-left: 78px;
  position: fixed;
}

.notification-chip {
  color: rgba(var(--cui-text-default-rgb)) !important;
  background: rgba(var(--cui-bg-status-bar-rgb)) !important;
}

.extended-sidebar {
  margin-left: 280px;
}

.text-transparent {
  color: rgba(255, 255, 255, 0.6) !important;
}

.badge-text {
  font-size: 0.5rem;
}

@media (max-width: 960px) {
  .top-navi-bar {
    margin-left: 0 !important;
  }

  .extended-sidebar {
    margin-left: 0 !important;
  }
}
</style>
