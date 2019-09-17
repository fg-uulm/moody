import Vue from "vue";
import App from "./App.vue";
import VueSplitter from "vue-splitter-pane";

Vue.config.productionTip = false;
Vue.use(VueSplitter);

new Vue({
  render: h => h(App)
}).$mount("#app");
