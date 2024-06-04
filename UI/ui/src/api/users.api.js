import api from './index';

const resource = '/users';

export const addUser = async (userData) => await api.post(`${resource}/add-user`, userData);

export const editUser = async (userData) => await api.put(`${resource}/edit-user/${userData.id}`, userData);

export const getUsers = async () => await api.get(`${resource}/get-user`);

export const getUser = async (userId) => await api.get(`${resource}/get-user/${userId}`);

export const deleteUser = async (userId) => await api.delete(`${resource}/delete-user/${userId}`);

export const getAdmins = async () => await api.get(`${resource}/get-admin`);

export const addAdmin = async (userData) => await api.post(`${resource}/add-admin`, userData);

export const editAdmin = async (userData) => await api.put(`${resource}/edit-admin/${userData.id}`, userData);

export const deleteAdmin = async (userId) => await api.delete(`${resource}/delete-admin/${userId}`);

export const getAdmin = async (userId) => await api.get(`${resource}/get-admin/${userId}`);

export const getUserHistory = async (parameters) => await api.get(`${resource}/user-history${parameters ? parameters : ''}`);

export const getAdminHistory = async (parameters) => await api.get(`${resource}/admin-history${parameters ? parameters : ''}`);

export const removeUser = async (userName) => await api.delete(`${resource}/${userName}`);
