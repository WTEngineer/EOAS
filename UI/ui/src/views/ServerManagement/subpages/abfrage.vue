<template>
  <div class="tw-w-full tw-mt-8 tw-pr-20">
    <div class="tw-flex tw-justify-center">
        <div class="tw-block">
          <div class="page-subtitle" >{{ $t('Ausweis/Reisepass durch') }}</div>
          <div class="page-subtitle" >{{ $t('hineindruecken einscannen.') }}</div>
        </div>
    </div>


    <div>
      <label class="form-input-label">Full name:</label>
      <v-text-field v-model="user.name" solo></v-text-field>
    </div>

    <div class="tw-flex">
      <div class="tw-w-1-3 tw-mr-2">
        <label class="form-input-label">Birthday:</label>
        <v-text-field v-model="user.birth" solo>
        </v-text-field>
      </div>

      <div class="tw-w-1-3 tw-mr-2">
        <label class="form-input-label">Age:</label>
        <v-text-field v-model="user.age" solo disabled>
        </v-text-field>
      </div>

      <div class="tw-w-1-3">
        <label class="form-input-label">Status:</label>
        <v-text-field v-model="user.status" solo disabled>
        </v-text-field>
      </div>
    </div>

    <div class="tw-w-full tw-mt-8" style="display: flex; justify-content: center; align-items: center;">
      <div class="tw-w-1-3" style="display: flex; justify-content: space-evenly;">
        <v-btn class="tw-mx-2 custom-button" @click="triggerOk">{{ $t('Ok') }}</v-btn>
        <v-btn class="tw-mx-2 custom-button" @click="() => {$router.push('/server-management/main') }">{{ $t('Cancel') }}</v-btn>
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
      user: {
        name: '',
        birth: '',
        age: '',
        status: ''
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

.tw-w-full {
  width: 100%;
}

.tw-mt-8 {
  margin-top: 2rem;
}

.tw-pr-20 {
  padding-right: 5rem;
}

.tw-flex {
  display: flex;
}

.tw-w-1-3 {
  width: 33.3333%;
}

.tw-mr-2 {
  margin-right: .5rem;
}

.form-input-label {
  display: block;
  margin-bottom: 0.5rem;
}

.v-text-field {
  width: 100%;
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
</style>
