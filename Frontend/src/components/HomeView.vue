<template>
  <section class="container page-section compact hero-section fade-in-up">
    <div class="row align-items-center justify-content-center w-100 g-5">
      <div class="col-12 col-lg-6 d-flex flex-column align-items-center align-items-lg-start text-center text-lg-start gap-3 stagger-child">
        <h1 class="display-1 hero-title">Household Services</h1>
        <p class="tagline">Your trusted marketplace for reliable household professionals.</p>
        <router-link to="/login" class="btn btn-primary btn-lg">Get Started</router-link>
        <p class="text-muted mb-0">
          Are you an admin?
          <router-link to="/hhs_admin_login" class="admin-link">Access the admin portal</router-link>
        </p>
      </div>
      <div class="col-12 col-lg-6 d-flex justify-content-center hero-media">
        <img src="@/assets/home-hero.svg" alt="Illustration of household services" class="img-fluid hero-image" />
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.hero-section {
  min-height: calc(100vh - 180px);
  display: flex;
  align-items: center;
}

.hero-image {
  max-width: 420px;
  width: 100%;
}

.hero-media {
  padding: 1rem;
}

.admin-link {
  font-weight: 600;
}
</style>
