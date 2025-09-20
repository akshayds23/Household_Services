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
                <router-link class="nav-link" to="/home_owner_dashboard">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/home_owner_dashboard/search">Search</router-link>
              </li>
              <li>
                <router-link class="nav-link" to="/home_owner_dashboard/bidding_requests">Bidding Requests</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/logout" @click="logout">Logout</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <div class="container page-section compact fade-in-up">
        <h1 class="text-center">Homeowner Search</h1>
        <form @submit.prevent="searchHomeOwner">
          <div class="mb-3">
            <label for="search_by" class="form-label">Search By:</label>
            <select class="form-select" id="search_by" v-model="searchBy">
              <option value="pincode">Pincode</option>
              <option value="address">Address</option>
              <option value="service_name">Service Name</option>
            </select>
          </div>
          <div class="mb-3">
            <label for="search_term" class="form-label">Search Term:</label>
            <input type="text" class="form-control" id="search_term" v-model="searchTerm" placeholder="Enter search term">
          </div>
          <button type="submit" class="btn btn-primary">Search</button>
        </form>
        <div v-if="services && services.length > 0" class="mt-5 table-responsive">
            <h2>Services:</h2>
            <table class="table table-striped table-hover">
              <thead>
                <tr>
                  <th>Service Name</th>
                  <th>Description</th>
                  <th>Price</th>
                  <th>Category</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="service in services" :key="service.id">
                  <td>{{ service.service_name }}</td>
                  <td>{{ service.description }}</td>
                  <td>{{ service.price }}</td>
                  <td>{{ service.service_type }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="mt-5 text-center text-muted">
            <h2 class="h4">No services match your filters yet.</h2>
          </div>
      </div>
    </div>
  </template>
  
  <script>
    export default {
      data() {
        return {
          searchBy: '',
          searchTerm: '',
          services: null,
          errorMessage: null,
        };
      },
      methods: {
        async logout() {
          const response = await fetch('http://127.0.0.1:5000/logout', {
            method: 'POST',
            headers: { 
                'Authorization': `Bearer ${localStorage.getItem('homeownerToken')}`
            },
          });
          this.$router.push('/');
        },
        async searchHomeOwner() {
            console.log('searchBy:', this.searchBy);
            console.log('searchTerm:', this.searchTerm);
  try {
    const response = await fetch(`http://127.0.0.1:5000/home_owner_dashboard/search`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('homeownerToken')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        search_by: this.searchBy,
        search_term: this.searchTerm
      })
    });
    if (!response.ok) {
      const error = await response.json();
      console.error(error);
      this.errorMessage = `Server returned an error: ${response.status} ${response.statusText} - ${error.message}`;
    } else {
      const result = await response.json();
      this.services = result.services;
      console.log(result)
    }
  } catch (error) {
    console.error(error);
    this.errorMessage = "Unable to connect to the server";
  }
}
      },
    };
  </script>
