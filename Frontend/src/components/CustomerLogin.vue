<template>
  <div class="container page-section compact fade-in-up">
    <h1 class="text-center">Login</h1>
    <form @submit.prevent="logincustomer">
      <div class="mb-3">
        <label for="customer_name" class="form-label">Customer Name</label>
        <input
          type="text"
          class="form-control"
          id="customer_name"
          v-model="customer_name"
          placeholder="Who should we welcome today?"
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
          type="password"
          class="form-control"
          id="password"
          v-model="password"
          placeholder="Enter your password"
        />
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
    <p>Don't have an account? </p>
    <p><button class="btn btn-danger" @click="$router.push('/service_professional_register')">Register as Service Professional</button></p>
    <p><button class="btn btn-danger" @click="$router.push('/home_owner_register')">Register as Homeowner</button></p>
  
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
      async logincustomer() {
        this.error = null;
        const payload = {
          customer_name: this.customer_name,
          password: this.password,
        };
  
        try {
          const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
          });
  
          const result = await response.json();
          if (!response.ok) {
            this.errorMessage = result.error || 'No data found';
          } else {
            if(result.role == "home_owner"){
              alert("Successfully logged in");
              localStorage.setItem('homeownerToken', result.token);
              this.$router.push('/home_owner_dashboard');
            }
            else if(result.role == "service_professional"){
              alert("Successfully logged in");
              localStorage.setItem('serviceProfessionalToken', result.token);
              this.$router.push('/service_professional_dashboard');
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
  
  