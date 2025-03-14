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
      <h1 class="text-center">Create Service Request</h1>
      <form @submit.prevent="createServiceRequest">
        <div class="mb-3">
          <label for="service_name" class="form-label">Service Name</label>
          <input type="text" class="form-control" id="service_name" name="service_name" v-model="service.service_name" readonly>
        </div>
        <div class="mb-3">
          <label for="service_professional" class="form-label">Service Professional</label>
          <select id="service_professional" name="service_professional" class="form-select" v-model="service_professional_id" required>
            <option v-for="sp in service_professionals" :key="sp.id" :value="sp.id">
              {{ sp.customer_name }}
            </option>
          </select>
        </div>
        <div class="mb-3">
          <label for="description" class="form-label">Describe Your Request</label>
          <textarea class="form-control" id="description" name="description" rows="5" v-model="description" placeholder="Share timelines, preferences, and special instructions"></textarea>
        </div>
        <div class="d-flex flex-wrap gap-3">
          <button type="submit" class="btn btn-primary">Create Request</button>
          <button type="button" class="btn btn-info" @click="createOpenRequest">Create Open Request</button>
        </div>
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
      service_id: null,
      service: {},
      service_professionals: []
    };
  },
  mounted() {
    this.service_id = this.$route.params.service_id;
    if (!this.service_id) {
      this.errorMessage = 'Service ID not found';
      return;
    }
    this.getServiceDetails();
  },
  methods: {
    async logout() {
      const response = await fetch('http://127.0.0.1:5000/logout', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('homeownerToken')}` },
      })
      const result = await response.json();
      this.$router.push('/');
    },
    async getServiceDetails() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/home_owner_dashboard/create_request/${this.service_id}`, {
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
        this.service = result;
        console.log(result)
        this.service_professionals = result.service_professionals;
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Unable to connect to the server";
      }
    },
    async createServiceRequest() {
      if (!this.service_id) {
        this.errorMessage = 'Service ID not found';
        return;
      }
      this.errorMessage = null;
      const payload = {
        service_id: this.service_id,
        service_professional_id: this.service_professional_id,
        description: this.description
      };
      console.log(this.service_professional_id)
      console.log("Sending payload:", payload);

      try {
        const response = await fetch(`http://127.0.0.1:5000/home_owner_dashboard/create_request/${this.service_id}`, {
          method: 'POST',
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
          alert("Request created successfully");
          this.$router.push('/home_owner_dashboard');
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Unable to connect to the server";
      }
    },
    async createOpenRequest() {
      if (!this.service_id) {
        this.errorMessage = 'Service ID not found';
        return;
      }
      this.errorMessage = null;
      try {
        const response = await fetch(`http://127.0.0.1:5000/home_owner_dashboard/create_open_request/${this.service_id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('homeownerToken')}`,
          }
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        console.log("Server response:", result);
        if (!response.ok) { 
          this.errorMessage = result.message || 'An error occurred';
        } else {
          alert("Request created successfully");
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
