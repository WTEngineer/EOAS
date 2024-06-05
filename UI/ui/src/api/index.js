import axios from 'axios';

const api = axios.create({
  baseURL: `http://${process.env.VUE_APP_SERVER_ADDRESS}:8000/api`,
  // process.env.NODE_ENV === 'development' || process.env.NODE_ENV === 'test'
  //   ? `${location.protocol}//${location.hostname}:${process.env.VUE_APP_SERVER_PORT}/api`
  //   : `http://localhost:8000/api`,
});

api.interceptors.request.use(
  (config) => {
    const user = JSON.parse(localStorage.getItem('user'));

    if (user && user.access_token) {
      config.headers['Authorization'] = `Bearer ${user.access_token}`;
    }

    return Promise.resolve(config);
  },

  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    return Promise.resolve(response);
  },

  (error) => {
    return Promise.reject(error);
  }
);

export default api;
