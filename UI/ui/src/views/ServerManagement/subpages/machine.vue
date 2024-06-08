<template>
  <div class="tw-w-full">
    <v-progress-linear class="loader" :active="loading" :indeterminate="loading" fixed top
      color="var(--cui-primary)"></v-progress-linear>

    <div v-if="!loading" class="tw-mb-7 tw-mt-5">
      <div class="tw-flex tw-justify-center">
        <div class="tw-block">
          <div class="page-subtitle">{{ $t('Wählen Sie ihr Gerät') }}</div>
          <!-- <div class="page-subtitle">{{ $t('Geschafft! Nach wählen des Geräts\nerscheint Ihr Freischaltungscode.') }}</div> -->
        </div>
      </div>

      <div class="tw-flex tw-justify-center">
        <div class="tw-block">
          <div class="page-subtitle">{{ $t('Geschafft! Nach wählen des Geräts erscheint Ihr Freischaltungscode.') }}</div>
        </div>
      </div>

      <div class="tw-w-full tw-mt-8" button-container>
        <div class="tw-w-1-3 button-wrapper">
          <v-btn class="tw-mx-2 custom-button" style="height: 200px; width: 250px;">{{ $t('Vorschau') }}</v-btn>
          <v-btn class="tw-mx-2 custom-button" style="height: 200px; width: 250px;">{{ $t('Nächste') }}</v-btn>
        </div>
      </div>

      <div class="tw-flex tw-justify-center">
        <div class="tw-block">
          <div class="page-subtitle">{{ $t('Code zum freischalten des Geräte') }}</div>
        </div>
      </div>

      <div class="tw-w-full tw-mt-4 tw-mb-8" style="padding: 10px 10px">
        <div class="tw-w-full" style="display: flex; justify-content: center; align-items: center;">
          <v-text-field v-model="form.username" :label="$t('')" style="max-width: 600px; height: 60px"
            background-color="var(--cui-bg-card)" color="var(--cui-text-default)" required solo>
          </v-text-field>
        </div>
      </div>

    </div>

    <div class="tw-w-full tw-mt-8" style="display: flex; justify-content: center; align-items: center;">
      <div class="tw-w-1-3" style="display: flex; justify-content: space-evenly;">
        <v-btn class="tw-mx-2 custom-button" @click="triggerOk">{{ $t('HILEF') }}</v-btn>
        <v-btn class="tw-mx-2 custom-button" @click="() => { $router.push('/server-management/main') }">{{
          $t('ABBRUCH') }}</v-btn>
      </div>
    </div>

  </div>
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

      groupSelect: [this.$t('Administrator'), this.$t('Cofounder')],
      blockSelect: [this.$t('Yes'), this.$t('No')],
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
    async triggerOk() {
      // await axios.get
      // const data = {
      //   'url': 'https://oasis.hessen.de/oasisws/spielerstatus',
      //   'kennung': '',
      //   'pass1': '',
      //   'pass2': '',
      //   'certFilePath': '',
      // }
      // await axios.post(url, data)
      this.$router.push('/server-management/main');
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

        // if (this.form.password && this.form.password2) {
        //   delete this.form.password2;
        // } else {
        //   delete this.form.password;
        //   delete this.form.password2;
        // }
        console.log('admin data');
        console.log(this.form);
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

.button-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.button-wrapper {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.button-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  /* Adjust padding as needed */
}

.button-left,
.button-right {
  display: flex;
}

.custom-button {
  width: 200px;
  background-color: green !important;
  color: white;
  /* Optional: if you want to change the text color as well */
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

.tw-w-4-1 {
  width: 25%;
}

.tw-w-4-3 {
  width: 75%;
}

button {
  background: none;
  border: none;
  cursor: pointer;
}

img {
  width: 50px;
  /* Adjust the size as needed */
  height: auto;
}
</style>
