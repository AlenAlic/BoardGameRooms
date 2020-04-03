import Vue from "vue";
import VueRouter from "vue-router";

// Pages
const Home = () => import("./../pages/Home");
const PageNotFound = () => import("./../pages/PageNotFound");
const SocketTestPage = () => import("./../pages/SocketTestPage");

Vue.use(VueRouter);

const routes = [
  {
    path: "/index.html",
    alias: "/",
    component: Home
  },
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/test",
    name: "test",
    component: SocketTestPage,
    meta: {
      auth: false,
      debugRoute: true
    }
  },
  {
    path: "**",
    name: "PageNotFound",
    component: PageNotFound
  }
];

const router = new VueRouter({
  mode: "history",
  linkActiveClass: "is-active",
  linkExactActiveClass: "primary",
  routes
});

/**
 * Disable debug routes on production
 */
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.debugRoute)) {
    if (process.env.NODE_ENV !== "development") {
      next({
        name: "home",
        query: {
          redirect: to.path
        }
      });
      return;
    }
  }
  next();
});

export default router;
