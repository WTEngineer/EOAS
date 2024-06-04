import { addUser, deleteUser, editUser, getUser, getUsers, addAdmin, deleteAdmin, editAdmin, getAdmin, getAdmins } from '../api/users.api';

export const users = {
  namespaced: true,
  state: {
    users: [],
    user: {},
    admins: [],
    admin: {},
    loading: false,
    error: null
  },
  actions: {
    async fetchUsers({ commit }) {
      commit('setLoading', true);
      try {
        const response = await getUsers();
        commit('setUsers', response.data);
        commit('setLoading', false);
      } catch (error) {
        commit('setError', error);
        commit('setLoading', false);
      }
    },
    async getUser({ commit }, userId) {
      commit('setLoading', true);
      try {
        const response = await getUser(userId);
        commit('setUser', response.data);
      } catch (error) {
        commit('setError', error);
        commit('setLoading', false);
      }
    },
    async addUser({ commit }, user) {
      commit('setLoading', true);
      try {
        const response = await addUser(user);
        commit('addUser', response.data);
      } catch (error) {
        commit('setError', error);
        commit('setLoading', false);
      }
    },
    async editUser({ commit }, userData) {
      commit('setLoading', true);
      try {
        const response = await editUser(userData);
        commit('editUser', response.data);
      } catch (error) {
        commit('setError', error);
        commit('setLoading', false);
      }
    },
    async deleteUser({ commit }, userId) {
      commit('setLoading', true);
      try {
        await deleteUser(userId);
        commit('deleteUser', userId);
      } catch (error) {
        commit('setError', error);
        commit('setLoading', false);
      }
    },
    async fetchAdmins({ commit }) {
      commit('setLoading', true);
      try {
        const response = await getAdmins();
        commit('setAdmins', response.data);
        commit('setLoading', false);
      } catch (error) {
        commit('setError', error);
        commit('setLoading', false);
      }
    },
    async getAdmin({ commit }, adminId) {
      commit('setLoading', true);
      try {
        const response = await getAdmin(adminId);
        commit('setAdmin', response.data);
      } catch (error) {
        commit('setError', error);
        commit('setLoading', false);
      }
    },
    async addAdmin({ commit }, adminData) {
      commit('setLoading', true);
      try {
        const response = await addAdmin(adminData);
        commit('addAdmin', response.data);
      } catch (error) {
        commit('setError', error);
        commit('setLoading', false);
      }
    },
    async editAdmin({ commit }, adminData) {
      commit('setLoading', true);
      try {
        const response = await editAdmin(adminData);
        commit('editAdmin', response.data);
      } catch (error) {
        commit('setError', error);
        commit('setLoading', false);
      }
    },
    async deleteAdmin({ commit }, adminId) {
      commit('setLoading', true);
      try {
        await deleteAdmin(adminId);
        commit('deleteAdmin', adminId);
      } catch (error) {
        commit('setError', error);
        commit('setLoading', false);
      }
    },
  },
  mutations: {
    setUsers: (state, users) => (state.users = users),
    setUser: (state, user) => (state.user = user),
    addUser: (state, user) => state.users.push(user),
    editUser: (state, updatedUser) => {
      const index = state.users.findIndex((user) => user.id === updatedUser.id);
      if (index !== -1) {
        state.users.splice(index, 1, updatedUser);
      }
    },
    deleteUser: (state, id) => {
      state.users = state.users.filter((user) => user.id !== id);
    },
    setAdmins: (state, admins) => (state.admins = admins),
    setAdmin: (state, admin) => (state.admin = admin),
    addAdmin: (state, admin) => state.admins.push(admin),
    editAdmin: (state, updatedAdmin) => {
      const index = state.admins.findIndex((admin) => admin.id === updatedAdmin.id);
      if (index !== -1) {
        state.admins.splice(index, 1, updatedAdmin);
      }
    },
    deleteAdmin: (state, id) => {
      state.admins = state.admins.filter((admin) => admin.id !== id);
    },
    setLoading: (state, loading) => (state.loading = loading),
    setError: (state, error) => (state.error = error),
  },
  getters: {
    allUsers: (state) => state.users,
    singleUser: (state) => state.user,
    allAdmins: (state) => state.admins,
    singleAdmin: (state) => state.admin,
    loading: (state) => state.loading,
    error: (state) => state.error,
  },
};
