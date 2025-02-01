<template>
    <div>
        <nav class="navbar navbar-expand-lg fade-in-up">
            <div class="container">
                <router-link class="navbar-brand" to="/home_owner_dashboard">Homeowner Dashboard</router-link>
                <button class="navbar-toggler" type="button" data-mdb-toggle="collapse" data-mdb-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                        <router-link class="nav-link" to="/admin_dashboard">Home</router-link>
                        </li>
                        <li class="nav-item">
                        <router-link class="nav-link" to="/admin_dashboard/search">Search</router-link>
                        </li>
                        <li class="nav-item">
                        <router-link class="nav-link" to="/logout" @click="logout">Logout</router-link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        <div class="container page-section compact fade-in-up">
            <h1 class="text-center">Edit Service Request</h1>
            <form @submit.prevent="editServiceRequest">
                <div class="mb-3">
                    <label for="service_name" class="form-label">Service Name</label>
                    <input type="text" class="form-control" id="service_name" v-model="service_name" disabled />
                </div>
                <div class="mb-3">
                    <label for="service_professionals" class="form-label">Service Professional</label>
                    <input type="text" class="form-control" id="service_professional" v-model="service_professional" disabled />
                </div>
                <div class="mb-3">
                    <label for="service_description" class="form-label">Update Description</label>
                    <textarea class="form-control" id="service_description" rows="4" v-model="description" required placeholder="Clarify schedule, special requests, or other changes"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Update Service Request</button>
            </form>
            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        </div>
    </div>
</template>
  
  <script>
  export default {
  data() {
    return {
      service_professional_id: '',
      description: '',
      errorMessage: null,
      service_request_id: null,
      service_request: {},
      service_professional: ''
    };
  },
  mounted() {
    this.service_request_id = this.$route.params.service_request_id;
    if (!this.service_request_id) {
      this.errorMessage = 'Service Request ID not found';
      return;
    }
    this.getServiceRequestDetails();
  },
  methods: {
    async getServiceRequestDetails() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/home_owner_dashboard/edit_request/${this.service_request_id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('homeownerToken')}`,
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        this.service_request = result;
        this.service_name = result.service_name;
        this.service_professional = result.service_professional;
        this.description = result.description;
        this.service_professional_id = result.service_professional_id;
        console.log(this.service_professionals)
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Unable to connect to the server";
      }
    },
    async editServiceRequest() {
      if (!this.service_request_id) {
        this.errorMessage = 'Service Request ID not found';
        return;
      }
      this.errorMessage = null;
      const payload = {
        description: this.description,
        service_professional_id: this.service_professional_id
      };
      console.log("Sending payload:", payload);

      try {
        const response = await fetch(`http://127.0.0.1:5000/home_owner_dashboard/edit_request/${this.service_request_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('homeownerToken')}`,
          },
          body: JSON.stringify(payload),
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        console.log("Server response:", result);
        if (!response.ok) {
          this.errorMessage = result.message || 'An error occurred';
        } else {
          alert("Service request updated successfully");
          this.$router.push('/home_owner_dashboard');
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Unable to connect to the server";
      }
    }
  }
};
  </script>
  
  