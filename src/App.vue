<template>
  <div id="app">
    <AppHeader />
    <main>
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>

<script>
import AppHeader from './components/Header.vue';
import AppFooter from './components/Footer.vue';

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter
  }
};
</script>

<style>
/* Global styles */
</style>

