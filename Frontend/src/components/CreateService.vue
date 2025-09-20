<template>
  <div class="container page-section compact fade-in-up">
    <h1 class="text-center">Create Service</h1>
    <form @submit.prevent="createService">
      <div class="mb-3">
        <label for="service_name" class="form-label">Service Name</label>
        <input type="text" class="form-control" id="service_name" v-model="service_name" placeholder="e.g. Home Deep Cleaning" required />
      </div>
      <div class="mb-3">
        <label for="service_description" class="form-label">Service Description</label>
        <textarea class="form-control" id="service_description" rows="3" v-model="description" placeholder="Describe what is included" required></textarea>
      </div>
      <div class="mb-3">
        <label for="service_price" class="form-label">Service Price</label>
        <input type="number" class="form-control" id="service_price" v-model="price" placeholder="Estimated price" required min="0" />
      </div>
      <div class="mb-3">
        <label for="service_type" class="form-label">Service Type</label>
        <input type="text" class="form-control" id="service_type" v-model="service_type" placeholder="Category name" required />
      </div>
      <button type="submit" class="btn btn-primary">Create Service</button>
    </form>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      service_name: '',
      description: '',
      price: null,
      service_type: '',
      errorMessage: null
    };
  },
  methods: {
    async createService() {
      this.errorMessage = null;
      const payload = {
        service_name: this.service_name,
        description: this.description,
        price: this.price,
        service_type: this.service_type,
      };

      console.log("Sending payload:", payload);
      console.log("Token:", localStorage.getItem('adminToken'));

      try {
        const response = await fetch('http://127.0.0.1:5000/admin_dashboard/create_service', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('adminToken')}`,
          },
          body: JSON.stringify(payload),
        });

        const result = await response.json();
        console.log("Server response:", result);

        if (!response.ok) {
          this.errorMessage = result.message || 'An error occurred';
        } else {
          alert("Service created successfully");
          this.resetForm();
          this.$router.push('/admin_dashboard');
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Unable to connect to the server";
      }
    },
    resetForm() {
      this.service_name = '';
      this.description = '';
      this.price = null;
      this.service_type = '';
    }
  }
};
</script>

