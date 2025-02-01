<template>
  <div class="app-shell">
    <transition name="route-fade" mode="out-in">
      <router-view />
    </transition>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  padding: 2.5rem 1.5rem 3.5rem;
}

@media (max-width: 768px) {
  .app-shell {
    padding: 1.75rem 1rem 2.75rem;
  }
}
</style>
