<template>
    <div class="container page-section compact fade-in-up">
      <h1 class="text-center">Homeowner Register</h1>
      <form @submit.prevent="registerHomeowner">
        <div class="mb-3">
        <label for="customer_name" class="form-label">Customer Name</label>
        <input type="text" class="form-control" id="customer_name" v-model="customer_name" placeholder="Full name" />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" v-model="password" placeholder="Choose a strong password" />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" id="email" v-model="email" placeholder="you@example.com" />
      </div>
      <div class="mb-3">
        <label for="phone" class="form-label">Phone</label>
        <input type="text" class="form-control" id="phone" v-model="phone" placeholder="Contact number" />
      </div>
      <div class="mb-3">
        <label for="address" class="form-label">Address</label>
        <input type="text" class="form-control" id="address" v-model="address" placeholder="Street, city" />
      </div>
      <div class="mb-3">
        <label for="pincode" class="form-label">Pincode</label>
        <input type="text" class="form-control" id="pincode" v-model="pincode" placeholder="Postal code" />
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
        errorMessage: null
      };
    },
    methods: {
      async registerHomeowner() {
        const payload = {
          customer_name: this.customer_name,
          password: this.password,
          email: this.email,
          phone: this.phone,
          address: this.address,
          pincode: this.pincode
        };
  
        try {
          const response = await fetch('http://127.0.0.1:5000/home_owner_register', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
          });
  
          const result = await response.json();
  
          if (!response.ok) {
            this.errorMessage = result.message || 'An error occurred';
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
  
  