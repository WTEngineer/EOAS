<template lang="pug">
.tw-w-full
  v-progress-linear.loader(:active="loading" :indeterminate="loading" fixed top color="var(--cui-primary)")

  v-btn.save-btn(:class="fabAbove ? 'save-btn-top' : ''" v-scroll="onScroll" v-show="fab" color="success" transition="fade-transition" width="40" height="40" fab dark fixed bottom right @click="save" :loading="loadingProgress")
    v-icon {{ icons['mdiCheckBold'] }}
  v-btn.cancel-btn(:class="fabAbove ? 'cancel-btn-top' : ''" v-scroll="onScroll" v-show="fab" color="error" transition="fade-transition" width="40" height="40" fab dark fixed bottom right @click="() => {$router.push('/admin-management') }" :loading="loadingProgress")
    v-icon {{ icons['mdiCloseThick'] }}

  .tw-mb-7.tw-mt-5(v-if="!loading")
    .tw-flex.tw-justify-between
      .tw-block
        <!-- .page-subtitle {{ $t('profile') }} -->
        .page-subtitle {{ $t('general_information') }}

    v-form.tw-w-full.tw-mt-4.tw-mb-8(ref="form" v-model="valid" lazy-validation)
      label.form-input-label {{ $t('username') }}
      v-text-field(v-model="form.username" :label="$t('username')" prepend-inner-icon="mdi-account" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" :rules="rules.username" required solo)
        template(v-slot:prepend-inner)
          v-icon.text-muted {{ icons['mdiAccount'] }}

      label.form-input-label {{ $t('Group') }}
      v-select(ref="adminGroup" :value="selectedGroup" :items="groupSelect" background-color="var(--cui-bg-card)" required solo)
        template(v-slot:prepend-inner)
          v-icon.text-muted {{ icons['mdiAccountGroup'] }}

      label.form-input-label {{ $t('permissions') }}: 
      v-chip.tw-text-white.tw-ml-1(small :key="perm" color="var(--cui-primary)") admin

      v-divider.tw-my-8

      .page-subtitle.tw-mt-8 {{ $t('password') }}

      label.form-input-label {{ $t('new_password') }}
      v-text-field(v-model="form.password" label="******" autocomplete="new-password" :type="showNewPassword ? 'text' : 'password'" :append-icon="showNewPassword ? icons['mdiEye'] : icons['mdiEyeOff']" @click:append="showNewPassword = !showNewPassword" prepend-inner-icon="mdi-key-variant" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" required solo)
        template(v-slot:prepend-inner)
          v-icon.text-muted {{ icons['mdiKeyVariant'] }}

      label.form-input-label {{ $t('new_password_verify') }}
      v-text-field(v-model="form.password2" label="******" autocomplete="new-password-confirm" :type="showNewPasswordConfirm ? 'text' : 'password'" :append-icon="showNewPasswordConfirm ? icons['mdiEye'] : icons['mdiEyeOff']" @click:append="showNewPasswordConfirm = !showNewPasswordConfirm" prepend-inner-icon="mdi-key-variant" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" :rules="rules.newpassword2" required solo)
        template(v-slot:prepend-inner)
          v-icon.text-muted {{ icons['mdiKeyVariant'] }}
      
      v-divider.tw-my-8

      .page-subtitle.tw-mt-8 {{ $t('Other information') }}

      label.form-input-label {{ $t('Telephone') }}
      v-text-field(v-model="form.phone" label="" :type="text" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)
        template(v-slot:prepend-inner)
          v-icon.text-muted {{ icons['mdiCellphoneBasic'] }}

      label.form-input-label {{ $t('Creator') }}
      v-text-field(v-model="form.creator" label="" :type="text" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" solo)
        template(v-slot:prepend-inner)
          v-icon.text-muted {{ icons['mdiCreation'] }}

      label.form-input-label {{ $t('Blocked') }}
      v-select(ref="blocked" :value="selectedBlock" :items="blockSelect" background-color="var(--cui-bg-card)" solo)
        template(v-slot:prepend-inner)
          v-icon.text-muted {{ icons['mdiBlockHelper'] }}
</template>

<script>
import { mdiAccount, mdiCheckBold, mdiCloseThick, mdiEye, mdiEyeOff, mdiBlockHelper, mdiCreation, mdiKeyVariant, mdiTimelapse, mdiAccountGroup, mdiCellphoneBasic } from '@mdi/js';


export default {
  name: 'AccountSettings',

  beforeRouteLeave(to, from, next) {
    this.loading = true;
    next();
  },

  data() {
    return {
      icons: {
        mdiAccountGroup,
        mdiBlockHelper,
        mdiAccount,
        mdiCreation,
        mdiCheckBold,
        mdiEye,
        mdiEyeOff,
        mdiKeyVariant,
        mdiTimelapse,
        mdiCellphoneBasic,
        mdiCloseThick,
      },
      userId: '',

      fab: true,
      fabAbove: false,

      loading: false,
      loadingProgress: false,

      form: {},

      rules: {
        username: [],
        newpassword: [],
        newpassword2: [],
      },

      groupSelect: [{
        text: this.$t('administrator'),
        value: 'Administrator'
      }, 
      {
        text: this.$t('cofounder'),
        value: 'Cofounder'
      }],
      blockSelect: [
        {
          text: this.$t('yes'),
          value: 'Yes'
        }, 
        {
          text: this.$t('no'),
          value: 'No'
        }
      ],
      selectedGroup: '',
      selectedBlock: '',

      showNewPassword: false,
      showNewPasswordConfirm: false,

      valid: true,
    };
  },

  computed: {
    currentUser() {
      return this.$store.state.users.admin || {};
    },
  },

  watch: {
    currentUser: {
      handler(newValue) {
        console.log(newValue);
        this.form.username = newValue.name;
        this.form.password = newValue.password;
        this.form.password2 = newValue.password;
        this.form.creator = newValue.creator;
        this.form.phone = newValue.phone;
        this.selectedGroup = newValue.usergroup;
        this.selectedBlock = newValue.blocked;
      },
      deep: true,
    },
  },

  created() {
    console.log('aa');
    console.log(this.$route.params);
    this.userId = this.$route.params.id;
    if (this.$route.params.id) {
      this.getUserById(this.$route.params.id);
    }
    this.rules = {
      username: [(v) => (!!v && !!v.trim()) || this.$t('username_is_required')],
      newpassword2: [
        (v) =>
          v
            ? v === this.form.password || this.$t('password_not_match')
            : !this.form.password || this.$t('enter_new_password'),
      ],
    };
  },

  methods: {
    async getUserById(id) {
      await this.$store.dispatch('users/getAdmin', id);
    },
    onScroll(e) {
      if (typeof window === 'undefined') {
        this.fabAbove = true;
        return;
      }

      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fabAbove = top > 20;
    },
    reset() {
      this.form = { ...this.currentUser };
    },
    async save() {
      this.loadingProgress = true;

      const valid = this.$refs.form.validate();

      if (valid) {
        this.form.adminGroup = this.$refs.adminGroup.internalValue;
        this.form.blocked = this.$refs.blocked.internalValue;
        const userData = {
          name: this.form.username,
          password: this.form.password,
          phone: this.form.phone,
          creator: this.form.creator,
          blocked: this.form.blocked,
          usergroup: this.form.adminGroup,
        }

        try {
          if (this.userId) {
            userData['id'] = this.userId;
            await this.$store.dispatch('users/editAdmin', userData);
            this.$toast.success(this.$t('This admin was updated successfully'));
            this.$router.push('/admin-management');
          }
          else {
            await this.$store.dispatch('users/addAdmin', userData);
            this.$toast.success(this.$t('New admin was added successfully'));
            this.$router.push('/admin-management');
          }
        } catch (err) {
          console.log(err);
          this.$toast.error(err.message);
        }
      } else {
        this.$toast.warning(this.$t('fill_all_required_fields'));
      }

      this.loadingProgress = false;
    },
  },
};
</script>

<style scoped>
.image-upload label {
  cursor: pointer;
}

.image-upload>input {
  display: none;
}

.profile-avatar {
  width: 8rem;
  height: 8rem;
  border-radius: 4rem;
  overflow: hidden;
  object-fit: cover;
}

.profile-avatar-bg {
  border-radius: 5rem;
  border: 5px solid var(--trans-border-color);
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
