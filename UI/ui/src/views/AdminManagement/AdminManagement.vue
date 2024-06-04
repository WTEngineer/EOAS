<template lang="pug">
.tw-w-full
  v-dialog(v-model="showDeleteConfirmationModal" max-width="600px")
    v-card
      v-card-title(style="display: flex; justify-content: space-between") {{$t('confirmation')}}
        v-icon(@click="deleteCancel" color="error") {{ icons['mdiClose'] }}
      v-card-text.text-default(style="font-size: 16px") {{$t('delete_admin_confirmation_msg')}}
      v-card-actions
        v-spacer
        v-btn.tw-bg-green-500.tw-text-white.tw-m-1(@click="deleteSave")
          v-icon {{ icons['mdiCheck'] }}
  .tw-mx-auto.tw-w-full.tw-py-5.tw-flex.tw-justify-between
    .tw-w-full.tw-flex.tw-flex-wrap.tw-justify-start.tw-flex-start
      v-row.tw-w-full
        v-col.tw-px-2.tw-py-2.tw-px-8(cols="3" v-for="user in users" :key="user.id")
          .tw-bg-white.tw-shadow.tw-rounded-lg.tw-overflow-hidden.tw-mx-2.tw-my-4.tw-max-w-xs
            .tw-w-full.tw-text-center.tw-mb-4
              v-avatar.tw-mt-5(size="120" color="#121212")
                v-img(v-on:error="handleErrorImg" :src="avatarSrc" :alt="user.name" style="border: 1px solid #1a1a1a")
                  template(v-slot:placeholder)
                    .tw-flex.tw-justify-center.tw-items-center.tw-h-full
                      v-progress-circular(indeterminate color="var(--cui-primary)" size="22")
            .tw-w-full.tw-px-10
              .tw-flex.tw-w-full.tw-text-sm.tw-leading-1.tw-text-gray-500
                .tw-w-1-2.tw-text-left {{$t('name')}}:
                .tw-w-1-2.tw-text-left.tw-pl-2 {{ user.name }}
              .tw-flex.tw-w-full.tw-text-sm.tw-leading-1.tw-text-gray-500
                .tw-w-1-2.tw-text-left {{$t('user_group')}}:
                .tw-w-1-2.tw-text-left.tw-pl-2 {{ user.usergroup }}
              .tw-flex.tw-w-full.tw-text-sm.tw-leading-1.tw-text-gray-500
                .tw-w-1-2.tw-text-left {{$t('phone')}}:
                .tw-w-1-2.tw-text-left.tw-pl-2 {{ user.phone }}
              .tw-flex.tw-w-full.tw-text-sm.tw-leading-1.tw-text-gray-500
                .tw-w-1-2.tw-text-left {{$t('creator')}}:
                .tw-w-1-2.tw-text-left.tw-pl-2 {{ user.creator }}
            .tw-flex.tw-justify-around.tw-mt-4.tw-mb-4
              v-btn.tw-bg-green-500.tw-text-white.tw-m-1(@click="editUser(user.id)")
                v-icon {{ icons['mdiAccountEdit'] }}
              v-btn.tw-bg-red-500.tw-text-white.tw-m-1(@click="deleteUser(user.id)")
                v-icon {{ icons['mdiDelete'] }}

  v-btn.add-btn(:class="fabAbove ? 'add-btn-top' : ''" v-scroll="onScroll" v-show="fab" color="success" transition="fade-transition" width="60" height="60" fab dark fixed bottom right @click="() => $router.push('/settings/add-admin')" :loading="loadingProgress")
    v-icon {{ icons['mdiPlus'] }}
</template>

<script>
import { mdiPlus, mdiAccountEdit, mdiDelete, mdiClose, mdiCheck } from '@mdi/js';

export default {

  data() {
    return {
      icons: {
        mdiPlus,
        mdiCheck,
        mdiAccountEdit,
        mdiDelete,
        mdiClose
      },
      avatarSrc: '../../assets/img/no_user.png',
      fab: true,
      fabAbove: false,
      showDeleteConfirmationModal: false,
      userId: null,
    }
  },
  computed: {
    users() {
      return this.$store.state.users.admins;
    },
  },
  async created() {
      this.fetchUsers();
      // const response = await dispatch(this.$store.state.users.users);
      // console.log(response.data);
      // this.users = response.data;
  },
  // async mounted() {
  //   this.users = this.$store.state.users.admins;
  //   console.log(this.$store.state.users.admins);
  // },
  methods: {
    async fetchUsers() {
      await this.$store.dispatch('users/fetchAdmins');
    },
    onScroll(e) {
      if (typeof window === 'undefined') {
        this.fabAbove = true;
        return;
      }

      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fabAbove = top > 20;
    },
    handleErrorImg() {
      // handle image error
      this.avatarSrc = require('../../assets/img/no_user.png');
    },
    editUser(id) {
      // edit user logic
      this.$router.push(`/settings/add-admin/${id}`)
      console.log(id);
    },
    deleteUser(id) {
      // delete user logic
      this.showDeleteConfirmationModal = true;
      this.userId = id;
      console.log(id);
    },
    deleteSave() {
      this.$store.dispatch('users/deleteAdmin', this.userId);
      this.showDeleteConfirmationModal = false;
    },
    deleteCancel() {
      this.showDeleteConfirmationModal = false;
    },
    addUser() {
      // add user logic
    },
  }
}
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

.add-btn {
  right: 30px !important;
  bottom: 75px !important;
  z-index: 11 !important;
  transition: 0.3s all;
}

.add-btn {
  z-index: 11 !important;
  transition: 0.3s all;
}

.add-btn-top {
  bottom: 125px !important;
}
</style>
