import Vue from 'vue';
import VueRouter from 'vue-router';

// import { app } from '@/main';
import store from '@/store';

// import { checkLogin } from '@/api/auth.api';

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch((err) => err);
};

Vue.use(VueRouter);
export const routes = [
  {
    path: '*',
    name: '404',
    meta: {
      auth: {
        requiresAuth: false,
        requiredLevel: [],
      },
      config: {
        showFooter: false,
        showNavbar: false,
        showSidebar: false,
      },
    },
    component: () => import(/* webpackChunkName: "404" */ '@/views/404/404.vue'),
  },
  {
    path: '/',
    name: 'Login',
    meta: {
      auth: {
        requiresAuth: false,
        requiredLevel: [],
      },
      config: {
        showFooter: false,
        showNavbar: false,
        showSidebar: false,
      },
    },
    component: () => import(/* webpackChunkName: "login" */ '@/views/Login/Login.vue'),
  },
  {
    path: '/start',
    name: 'Start',
    meta: {
      auth: {
        requiresAuth: true,
        requiredLevel: ['admin'],
      },
      config: {
        showFooter: false,
        showNavbar: false,
        showSidebar: false,
      },
    },
    component: () => import(/* webpackChunkName: "start" */ '@/views/Start/Start.vue'),
  },
  // {
  //   path: '/dashboard',
  //   name: 'dashboard',
  //   meta: {
  //     auth: {
  //       requiresAuth: true,
  //       requiredLevel: [/*"cameras:access", */ 'dashboard:access'],
  //     },
  //     config: {
  //       fixedNavbar: true,
  //       showFooter: true,
  //       showNavbar: true,
  //       showSidebar: true,
  //     },
  //     navigation: {
  //       main: true,
  //       icon: 'mdi-view-dashboard',
  //     },
  //   },
  //   component: () => import(/* webpackChunkName: "dashboard" */ '@/views/Dashboard/Dashboard.vue'),
  // },
  {
    path: '/cameras',
    name: 'monitor',
    meta: {
      auth: {
        requiresAuth: true,
        requiredLevel: ['cameras:access'],
      },
      config: {
        fixedNavbar: true,
        showFooter: true,
        showNavbar: true,
        showSidebar: true,
      },
      navigation: {
        main: true,
        icon: 'mdi-cctv',
      },
    },
    component: () => import(/* webpackChunkName: "cameras" */ '@/views/Cameras/Cameras.vue'),
  },
  {
    path: '/cameras/:name',
    name: 'camera',
    meta: {
      auth: {
        requiresAuth: true,
        requiredLevel: ['cameras:access'],
      },
      config: {
        fixedNavbar: true,
        showFooter: true,
        showNavbar: true,
        showSidebar: true,
      },
    },
    component: () => import(/* webpackChunkName: "camera" */ '@/views/Camera/Camera.vue'),
  },
  {
    path: '/cameras/:name/feed',
    name: 'CameraFeed',
    meta: {
      auth: {
        requiresAuth: true,
        requiredLevel: ['cameras:access'],
      },
      config: {
        fixedNavbar: false,
        showFooter: false,
        showNavbar: false,
        showSidebar: false,
      },
    },
    component: () => import(/* webpackChunkName: "cameraFeed" */ '@/views/Camera/CameraFeed.vue'),
  },
  {
    path: '/user-management',
    name: 'user_management',
    meta: {
      auth: {
        requiresAuth: true,
        requiredLevel: ['userManagement:access'],
      },
      config: {
        fixedNavbar: true,
        showFooter: true,
        showNavbar: true,
        showSidebar: true,
      },
      navigation: {
        main: true,
        icon: 'mdi-account-details',
      },
    },
    component: () => import('@/views/UserManagement/UserManagement.vue'),
  },
  {
    path: '/user-history',
    name: 'user_history',
    meta: {
      auth: {
        requiresAuth: true,
        requiredLevel: ['recordings:access'],
      },
      config: {
        fixedNavbar: true,
        showFooter: true,
        showNavbar: true,
        showSidebar: true,
      },
      navigation: {
        main: true,
        icon: 'mdi-image-multiple',
      },
    },
    component: () => import('@/views/UserHistory/UserHistory.vue'),
  },
  {
    path: '/admin-management',
    name: 'admin_management',
    meta: {
      auth: {
        requiresAuth: true,
        requiredLevel: ['adminManagement:access'],
      },
      config: {
        fixedNavbar: true,
        showFooter: true,
        showNavbar: true,
        showSidebar: true,
      },
      navigation: {
        main: true,
        icon: 'mdi-account-group',
      },
    },
    component: () => import('@/views/AdminManagement/AdminManagement.vue'),
  },
  {
    path: '/admin-history',
    name: 'admin_history',
    meta: {
      auth: {
        requiresAuth: true,
        requiredLevel: ['recordings:access'],
      },
      config: {
        fixedNavbar: true,
        showFooter: true,
        showNavbar: true,
        showSidebar: true,
      },
      navigation: {
        main: true,
        icon: 'mdi-file-account',
      },
    },
    component: () => import(/* webpackChunkName: "recordings" */ '@/views/AdminHistory/AdminHistory.vue'),
  },
  {
    path: '/settings/appearance',
    name: 'settings',
    meta: {
      auth: {
        requiresAuth: true,
        requiredLevel: ['recordings:access'],
      },
      config: {
        fixedNavbar: true,
        showFooter: true,
        showNavbar: true,
        showSidebar: true,
      },
      navigation: {
        main: true,
        icon: 'mdiCogs',
      },
    },
    component: () => import('@/views/Settings/subpages/appearance.vue'),
  },
  {
    path: '/server-management',
    name: 'Server management',
    meta: {
      redirectTo: '/server-management/main',
      auth: {
        requiresAuth: true,
        requiredLevel: [],
      },
      config: {
        fixedNavbar: true,
        showFooter: true,
        showNavbar: true,
        showSidebar: true,
      },
      navigation: {
        main: true,
        icon: 'mdiCogs',
      },
    },
    component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/Settings.vue'),
    children: [
      {
        path: 'main',
        meta: {
          name: '',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: [],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-account-circle-outline',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/ServerManagement/subpages/Main.vue'),
      },
      {
        path: 'oasisSetting',
        meta: {
          name: '',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['settings:general:access', 'settings:general:edit'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-application-cog',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/ServerManagement/subpages/oasisSetting.vue'),
      },
      {
        path: 'freischaltung',
        meta: {
          name: '',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['settings:general:access', 'settings:general:edit'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-application-cog',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/ServerManagement/subpages/freischaltung.vue'),
      },
      {
        path: 'abfrage',
        meta: {
          name: '',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['settings:general:access', 'settings:general:edit'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-application-cog',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/ServerManagement/subpages/abfrage.vue'),
      },
      {
        path: 'about',
        meta: {
          name: '',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['settings:general:access', 'settings:general:edit'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-application-cog',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/ServerManagement/subpages/about.vue'),
      },
    ],
  },
  // {
  //   path: '/notifications',
  //   name: 'Notifications',
  //   meta: {
  //     auth: {
  //       requiresAuth: true,
  //       requiredLevel: ['notifications:access'],
  //     },
  //     config: {
  //       fixedNavbar: true,
  //       showFooter: true,
  //       showNavbar: true,
  //       showSidebar: true,
  //     },
  //     navigation: {
  //       main: true,
  //       icon: 'mdi-bell',
  //     },
  //   },
  //   component: () => import(/* webpackChunkName: "notifications" */ '@/views/Notifications/Notifications.vue'),
  // },
  // {
  //   path: '/camview',
  //   name: 'Camview',
  //   meta: {
  //     auth: {
  //       requiresAuth: true,
  //       requiredLevel: [/*"cameras:access", */ 'camview:access'],
  //     },
  //     config: {
  //       showFooter: false,
  //       showMinifiedNavbar: true,
  //       showNavbar: true,
  //       showSidebar: true,
  //     },
  //     navigation: {
  //       main: true,
  //       icon: 'mdi-grid-large',
  //     },
  //   },
  //   component: () => import(/* webpackChunkName: "camview" */ '@/views/Camview/Camview.vue'),
  // },
  // {
  //   path: '/console',
  //   name: 'Console',
  //   meta: {
  //     auth: {
  //       requiresAuth: true,
  //       requiredLevel: ['admin'],
  //     },
  //     config: {
  //       fixedNavbar: true,
  //       showFooter: true,
  //       showNavbar: true,
  //       showSidebar: true,
  //     },
  //     navigation: {
  //       extras: true,
  //       icon: 'mdi-console',
  //     },
  //   },
  //   component: () => import(/* webpackChunkName: "console" */ '@/views/Console/Console.vue'),
  // },
  {
    path: '/config',
    name: 'Config',
    meta: {
      auth: {
        requiresAuth: true,
        requiredLevel: ['admin'],
      },
      config: {
        fixedNavbar: true,
        showFooter: true,
        showNavbar: true,
        showSidebar: true,
      },
      navigation: {
        extras: true,
        icon: 'mdi-text-box-outline',
      },
    },
    component: () => import(/* webpackChunkName: "config" */ '@/views/Config/Config.vue'),
  },
  {
    path: '/utilization',
    name: 'Utilization',
    meta: {
      auth: {
        requiresAuth: true,
        requiredLevel: ['admin'],
      },
      config: {
        fixedNavbar: true,
        showFooter: true,
        showNavbar: true,
        showSidebar: true,
      },
      navigation: {
        extras: true,
        icon: 'mdi-chart-arc',
      },
    },
    component: () => import(/* webpackChunkName: "utilization" */ '@/views/Utilization/Utilization.vue'),
  },
  {
    path: '/plugins',
    name: 'Plugins',
    meta: {
      auth: {
        requiresAuth: true,
        requiredLevel: ['admin'],
      },
      config: {
        fixedNavbar: true,
        showFooter: true,
        showNavbar: true,
        showSidebar: true,
      },
      navigation: {
        extras: true,
        icon: 'mdi-puzzle',
      },
    },
    component: () => import(/* webpackChunkName: "plugins" */ '@/views/Plugins/Plugins.vue'),
  },
  {
    path: '/settings',
    name: 'Settings',
    meta: {
      redirectTo: '/settings/account',
      auth: {
        requiresAuth: true,
        requiredLevel: [],
      },
      config: {
        fixedNavbar: true,
        showFooter: true,
        showNavbar: true,
        showSidebar: true,
      },
      navigation: {
        bottom: true,
        icon: 'mdi-cog',
      },
    },
    component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/Settings.vue'),
    children: [
      {
        path: 'edit-user/:id',
        meta: {
          name: 'Edit User',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: [],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-account-circle-outline',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/editUser.vue'),
      },
      {
        path: 'add-admin',
        meta: {
          name: 'add_admin',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: [],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-account-circle-outline',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/addAdmin.vue'),
      },
      {
        path: 'add-admin/:id',
        meta: {
          name: 'edit_admin',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: [],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-account-circle-outline',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/addAdmin.vue'),
      },
      {
        path: 'appearance',
        meta: {
          name: 'Appearance',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: [],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-pencil-ruler',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/appearance.vue'),
      },
      {
        path: 'interface',
        meta: {
          name: 'Interface',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['settings:general:access', 'settings:general:edit'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-application-cog',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/interface.vue'),
      },
      {
        path: 'add-user',
        meta: {
          name: 'add_user',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['admin'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-account-plus',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/addUser.vue'),
      },
      {
        path: 'add-user/:id',
        meta: {
          name: 'edit_user',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['admin'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-account-plus',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/addUser.vue'),
      },
      {
        path: 'cameras',
        meta: {
          name: 'Cameras',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['settings:cameras:access', 'settings:cameras:edit'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-cctv',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/cameras.vue'),
      },
      {
        path: 'recordings',
        meta: {
          name: 'Recordings',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['settings:recordings:access', 'settings:recordings:edit'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-image-multiple-outline',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/recordings.vue'),
      },
      {
        path: 'notifications',
        meta: {
          name: 'Notifications',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['settings:notifications:access', 'settings:notifications:edit'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-bell-outline',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/notifications.vue'),
      },
      {
        path: 'rekognition',
        meta: {
          name: 'Rekognition',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['admin'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-face-recognition',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/rekognition.vue'),
      },
      {
        path: 'backup',
        meta: {
          name: 'Backup',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['backup:download', 'backup:restore'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-backup-restore',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/backup.vue'),
      },
      {
        path: 'system',
        meta: {
          name: 'System',
          child: true,
          auth: {
            requiresAuth: true,
            requiredLevel: ['admin'],
          },
          config: {
            fixedNavbar: true,
            showFooter: true,
            showNavbar: true,
            showSidebar: true,
          },
          navigation: {
            icon: 'mdi-tune',
          },
        },
        component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings/subpages/system.vue'),
      },
    ],
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  scrollBehavior() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ x: 0, y: 0, behavior: 'smooth' });
      }, 250);
    });
  },
});

router.beforeEach(async (to, from, next) => {
  const user = store.getters['auth/user'];
  const pageName = (to.name || to.meta.name).toLowerCase();
  console.log(user);
  console.log(pageName);
  if (user) {
    try {
      next();
      // await checkLogin();

      // if (to.meta.auth.requiredLevel.length > 0) {
      //   const granted = user.permissionLevel.some(
      //     (level) => to.meta.auth.requiredLevel.includes(level) || level === 'admin'
      //   );

      //   if (!granted) {
      //     app.$toast.error(`${app.$t(pageName)}: ${app.$t('permission_required')}`);
      //     return next('/settings/account');
      //     //return next(false);
      //   }
      // }

      // const lastRouteName = localStorage.getItem('lastPage');
      // const shouldRedirect = Boolean(pageName === 'login' && lastRouteName);

      // if (shouldRedirect) {
      //   next({ path: lastRouteName });
      // } else {
      //   next();
      // }
    } catch (err) {
      console.log(err);

      await store.dispatch('auth/logout');
      setTimeout(() => next('/'), 200);
    }
  } else {
    if (pageName !== 'login') {
      next('/');
    } else {
      next();
    }
  }
});

router.afterEach((to) => {
  const pageName = (to.name || to.meta.name).toLowerCase();

  if (pageName !== 'login') {
    localStorage.setItem('lastPage', to.path);
  }
});

export default router;
