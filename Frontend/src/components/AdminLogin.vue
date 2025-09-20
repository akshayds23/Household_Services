<template>
  <div class="container page-section compact fade-in-up">
    <h1 class="text-center">Admin Login</h1>
    <form @submit.prevent="loginAdmin">
      <div class="mb-3">
        <label for="customer_name" class="form-label">Customer Name</label>
        <input type="text" class="form-control" id="customer_name" v-model="customer_name" placeholder="Enter your admin username" />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" v-model="password" placeholder="Secure password" />
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
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
      token: '',
      role: '',
      errorMessage: null
    };
  },
  methods: {
    async loginAdmin() {
      this.error = null;
      const payload = {
        customer_name: this.customer_name,
        password: this.password,
      };

      try {
        const response = await fetch('http://127.0.0.1:5000/hhs_admin_login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`
          },
          body: JSON.stringify(payload),
        });

        const result = await response.json();

        if (!response.ok) {
          this.errorMessage = result.message || 'An error occurred';
        } else {
          if(result.role == "admin"){
            alert("Successfully logged in");
            localStorage.setItem('adminToken', result.token);
            this.$router.push('/admin_dashboard');
          }
          else{
            this.errorMessage = "Unauthorised";
          }
            
      
        }
      } catch (error) {
        this.errorMessage = "Unable to connect to the server";
      }
    },
  },
};
</script>

