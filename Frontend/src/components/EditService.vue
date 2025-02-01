<template>
  <div class="container page-section compact fade-in-up">
    <h1 class="text-center">Edit Service</h1>
    <form @submit.prevent="updateService">
      <div class="mb-3">
        <label for="service_name" class="form-label">Service Name</label>
        <input type="text" class="form-control" id="service_name" v-model="service.service_name" placeholder="Service title" required />
      </div>
      <div class="mb-3">
        <label for="service_description" class="form-label">Service Description</label>
        <textarea class="form-control" id="service_description" rows="3" v-model="service.description" placeholder="Describe the service" required></textarea>
      </div>
      <div class="mb-3">
        <label for="service_price" class="form-label">Service Price</label>
        <input type="number" class="form-control" id="service_price" v-model="service.price" placeholder="Estimated price" required min="0" />
      </div>
      <div class="mb-3">
        <label for="service_type" class="form-label">Service Type</label>
        <input type="text" class="form-control" id="service_type" v-model="service.service_type" placeholder="Category" required />
      </div>
      <button type="submit" class="btn btn-primary">Update Service</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      service: {
        id: '',
        service_name: '',
        description: '',
        price: '',
        service_type: ''
      }
    }
  },
  mounted() {
    this.getServiceDetails(this.$route.params.id);
  },
  methods: {
    async getServiceDetails(service_id) {
      try {
        const token = localStorage.getItem('adminToken');
        const headers = {
          'Authorization': `Bearer ${token}`,
        };
        const response = await fetch(`http://127.0.0.1:5000/admin_dashboard/edit_service/${service_id}`, {
          method: 'GET',
          headers,
        });
        const result = await response.json();
        this.service = result.service;
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Unable to connect to the server";
      }
    },
    async updateService() {
      try {
        const token = localStorage.getItem('adminToken');
        const headers = {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        };
        const response = await fetch(`http://127.0.0.1:5000/admin_dashboard/edit_service/${this.service.id}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(this.service)
        });
        const result = await response.json();
        console.log(result);
        this.$router.push('/admin_dashboard');
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Unable to connect to the server";
      }
    },
  }
}
</script>
