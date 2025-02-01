<template>
  <div class="container page-section compact fade-in-up">
    <h1 class="text-center">Service Professional Register</h1>
    <form @submit.prevent="registerServiceProfessional">
      <div class="mb-3">
        <label for="customer_name" class="form-label">Customer Name</label>
        <input type="text" class="form-control" id="customer_name" v-model="customer_name" placeholder="Full name" required />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" v-model="password" placeholder="Choose a strong password" required />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" id="email" v-model="email" placeholder="you@example.com" required />
      </div>
      <div class="mb-3">
        <label for="phone" class="form-label">Phone</label>
        <input type="text" class="form-control" id="phone" v-model="phone" placeholder="Contact number" required />
      </div>
      <div class="mb-3">
        <label for="address" class="form-label">Address</label>
        <input type="text" class="form-control" id="address" v-model="address" placeholder="Street, city" required />
      </div>
      <div class="mb-3">
        <label for="pincode" class="form-label">Pincode</label>
        <input type="text" class="form-control" id="pincode" v-model="pincode" placeholder="Postal code" required />
      </div>
      <div class="mb-3">
        <label for="service_professional_file" class="form-label">Service Professional File</label>
        <input type="file" class="form-control" id="service_professional_file" @change="handleFileChange" required />
      </div>
      <div class="mb-3">
        <label for="service" class="form-label">Select Service</label>
        <select id="service" name="service" class="form-select" v-model="selectedService" required>
          <option v-for="service in services" :key="service.id" :value="service.id">
            {{ service.service_name }}
          </option>
        </select>
      </div>
      <div class="mb-3">
        <label for="service_professional_experience" class="form-label">Service Professional Experience</label>
        <input type="text" class="form-control" id="service_professional_experience" v-model="service_professional_experience" placeholder="Years of experience" />
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      customer_name: '',
      password: '',
      email: '',
      phone: '',
      address: '',
      pincode: '',
      service_professional_file: null,
      services: [],
      selectedService: '',
      service_professional_experience: '',
      errorMessage: null
    };
  },
  async mounted() {
    await this.fetchServices();
  },
  methods: {
    handleFileChange(event) {
      this.service_professional_file = event.target.files[0];
    },
    async fetchServices() {
      try {
        const response = await fetch('http://127.0.0.1:5000/get_services');
        const result = await response.json();
        this.services = result.services;
      } catch (error) {
        console.error("Error fetching services:", error);
        this.errorMessage = "Unable to fetch services";
      }
    },
    async registerServiceProfessional() {
      const formData = new FormData();
      formData.append('customer_name', this.customer_name);
      formData.append('password', this.password);
      formData.append('email', this.email);
      formData.append('phone', this.phone);
      formData.append('address', this.address);
      formData.append('pincode', this.pincode);
      formData.append('service_professional_file', this.service_professional_file);
      formData.append('service', this.selectedService);
      formData.append('service_professional_experience', this.service_professional_experience);
      
      try {
        const response = await fetch('http://127.0.0.1:5000/service_professional_register', {
          method: 'POST',
          body: formData
        });
        
        const result = await response.json();
        
        if (!response.ok) {
          this.errorMessage = result.error || 'An error occurred';
        } else {
          alert("Registration successful");
          this.$router.push('/login');
        }
      } catch (error) {
        this.errorMessage = "Unable to connect to the server";
      }
    }
  }
};
</script>

