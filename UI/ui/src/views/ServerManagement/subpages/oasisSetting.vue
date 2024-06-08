<template>
  <div class="tw-w-full">
    <v-progress-linear class="loader" :active="loading" :indeterminate="loading" fixed top
      color="var(--cui-primary)"></v-progress-linear>

    <div v-if="!loading" class="tw-mb-7 tw-mt-5">
      <div class="tw-flex tw-justify-center">
        <div class="tw-block">
          <div class="page-subtitle" >{{ $t('Oasis Certification Setting') }}</div>
        </div>
      </div>

      <div class="tw-w-full tw-mt-4 tw-mb-8" style="padding: 10px 10px">
        <div class="tw-w-full" style="display: flex; justify-content: center; align-items: center;">
          <div class="tw-w-4-1" style="text-align: right">
            <label class="form-input-label">{{ $t('URL') }}</label>
          </div>
          <div class="tw-w-4-3" style="text-align: left; padding-left: 30px">
            <v-text-field v-model="url" :label="$t('https://oasis-tst-crt.hessen.de/oasisws/spielerstatus')"
              style="max-width: 600px; height: 60px" background-color="var(--cui-bg-card)"
              color="var(--cui-text-default)" required solo>

            </v-text-field>
          </div>
        </div>

        <div class="tw-w-full" style="display: flex; justify-content: center; align-items: center;">
          <div class="tw-w-4-1" style="text-align: right">
            <label class="form-input-label">{{ $t('kennung') }}</label>
          </div>
          <div class="tw-w-4-3" style="text-align: left; padding-left: 30px">
            <v-text-field v-model="kennung" :label="$t('')" 
              style="max-width: 600px; height: 60px" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" required
              solo>
            </v-text-field>
          </div>
        </div>

        <div class="tw-w-full" style="display: flex; justify-content: center; align-items: center;">
          <div class="tw-w-4-1" style="text-align: right">
            <label class="form-input-label">{{ $t('passwort') }}</label>
          </div>
          <div class="tw-w-4-3"
            style="text-align: left; padding-left: 30px; display: flex; justify-content: space-between; align-items: center">
            <div class="tw-w-4-3">
              <v-text-field v-model="pass1" :label="$t('')" 
                style="max-width: 600px; height: 60px" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" required
                solo>
              </v-text-field>
            </div>
            <div class="tw-w-4-1">
              <v-btn @click="triggerGetPath">...</v-btn>      
            </div>
            <input type="file" ref="getPath" @change="handleGetPath" style="display: none" />
          </div>
        </div>

        <div class="tw-w-full" style="display: flex; justify-content: center; align-items: center;">
          <div class="tw-w-4-1" style="text-align: right">
            <label class="form-input-label">{{ $t('Cert-File') }}</label>
          </div>
          <div class="tw-w-4-3" style="text-align: left; padding-left: 30px">
            <v-text-field v-model="certFilePath" :label="$t('')" 
              style="max-width: 600px; height: 60px" background-color="var(--cui-bg-card)" color="var(--cui-text-default)" required
              solo>
            </v-text-field>
          </div>
        </div>

        <div class="tw-w-full" style="display: flex; justify-content: center; align-items: center;">
          <div class="tw-w-4-1" style="text-align: right">
            <label class="form-input-label">{{ $t('passwort') }}</label>
          </div>
          <div class="tw-w-4-3" style="text-align: left; padding-left: 30px">
            <v-text-field v-model="pass2" :label="$t('')"
               style="max-width: 600px; height: 60px" background-color="var(--cui-bg-card)"
              color="var(--cui-text-default)" required solo>
            </v-text-field>
          </div>
        </div>
      </div>
    </div>

    <div class="tw-w-full tw-mt-8" style="display: flex; justify-content: center; align-items: center;">
      <div class="tw-w-1-3" style="display: flex; justify-content: space-evenly;">
        <v-btn class="tw-mx-2 custom-button" @click="triggerImport">{{ $t('Import') }}</v-btn>
        <v-btn class="tw-mx-2 custom-button" @click="triggerOk">{{ $t('Ok') }}</v-btn>
        <v-btn class="tw-mx-2 custom-button" @click="() => {$router.push('/server-management/main') }">{{ $t('Cancel') }}</v-btn>
      </div>

      <input type="file" ref="fileImport" @change="handleFileImport" style="display: none" />
    </div>

  </div>
</template>

<script>
import { mdiAccount, mdiCheckBold, mdiCloseThick, mdiEye, mdiEyeOff, mdiBlockHelper, mdiCreation, mdiKeyVariant, mdiTimelapse, mdiAccountGroup, mdiCellphoneBasic } from '@mdi/js';
import axios from 'axios';

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

      url: 'https://oasis.hessen.de/oasisws/spielerstatus',
      kennung: '',
      pass1: '',
      pass2: '',
      certFilePath: '',

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

    ////////////////////////////////////////////////////////////
    triggerImport() {
      this.$refs.fileImport.click();
    },
    async triggerGetPath() {
      // this.$refs.getPath.click();
      const res = await axios.get(`http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/api/get-full-path`);
      this.certFilePath = res.data;
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
    handleFileImport(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const text = e.target.result;
          console.log('text');
          console.log(text);
          this.parseFileContent(text);
        };
        reader.readAsText(file);
      }
    },
    handleGetPath(event) {
      const file = event.target.files[0];
      console.log(event.target.files);
      if (file) {
        this.certFilePath = file.name;
      }
    },
    parseFileContent(content) {
      const kennungMatch = content.match(/Kennung\s*:\s*(\S+)/);
      const pass1Match = content.match(/Pass1\s*:\s*(\S+)/);
      const pass2Match = content.match(/Pass2\s*:\s*(\S+)/);

      this.kennung = kennungMatch ? kennungMatch[1] : '';
      this.pass1 = pass1Match ? pass1Match[1] : '';
      this.pass2 = pass2Match ? pass2Match[1] : '';
    },

    ///////////////////////////////////////////////////////////////

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
