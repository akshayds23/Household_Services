<template>
    <div>
      <nav class="navbar navbar-expand-lg fade-in-up">
        <div class="container">
          <a class="navbar-brand" href="/home_owner_dashboard">Homeowner Dashboard : {{ customerName }}</a>
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
              <li class="nav-item">
                <router-link class="nav-link" to="/home_owner_dashboard/bidding_requests">Bidding Requests</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/logout" @click="logout">Logout</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <section class="container page-section fade-in-up">
        <h2>Available Services</h2>
        <div v-if="services.length > 0">
          <div class="row">
            <div v-for="service in services" :key="service.id" class="col-md-4 mb-4">
              <div class="card h-100">
                <div class="card-body d-flex flex-column justify-content-between">
                  <div>
                    <h5 class="card-title">{{ service.service_name }}</h5>
                    <p class="card-text">{{ service.description }}</p>
                    <p class="card-text">Price: {{ service.price }}</p>
                  </div>
                  <router-link :to="`/home_owner_dashboard/create_request/${service.id}`" class="btn btn-primary mt-3">Create Request</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
        <p v-else class="text-center text-muted">No services available.</p>
      </section>

      <section class="container page-section fade-in-up">
        <h2>Service History</h2>
        <div v-if="serviceHistory.length > 0" class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>Service Name</th>
                <th>Description</th>
                <th>Service Professional</th>
                <th>Request Type</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in serviceHistory" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.description }}</td>
                <td>{{ request.service_professional}}</td>
                <td>{{ request.type_of_request }}</td>
                <td>{{ request.service_status }}</td>
                <td class="d-flex flex-wrap gap-2">
                  <a v-if="request.service_status === 'accepted'" @click="navigateToCloseRequest(request.id)" class="btn btn-success">Close Request</a>
                  <button v-else-if="request.service_status === 'rejected'" class="btn btn-secondary" disabled>Rejected</button>
                  <button v-else-if="request.service_status === 'closed'" class="btn btn-secondary" disabled>Closed</button>
                  <button v-else-if="request.service_status === 'pending' && request.type_of_request === 'public'" class="btn btn-secondary" disabled>Pending</button>
                  <div v-else class="d-flex flex-wrap gap-2">
                    <router-link class="btn btn-warning" :to="`/home_owner_dashboard/edit_request/${request.id}`">Edit</router-link>
                    <a class="btn btn-danger" @click="deleteRequest(request.id)">Delete</a>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="text-muted">No service history yet.</p>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        customerName: '',
        services: [],
        serviceHistory: []
      }
    },
    mounted() {
      this.fetchHomeOwnerDashboardData();
    },
    methods: {
      async logout() {
        const response = await fetch('http://127.0.0.1:5000/logout', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('adminToken')}` },
          });
          const result = await response.json();
          this.services = result.services;
          this.$router.push('/');
      },
      async fetchHomeOwnerDashboardData() {
        try {
          const response = await fetch('http://127.0.0.1:5000/home_owner_dashboard', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('homeownerToken')}`,
              'Content-Type': 'application/json',
            }
          });
  
          const result = await response.json();
          console.log(result)
          if (!response.ok) {
            console.error(result.message || 'An error occurred');
          } else {
            this.customerName = result.customer_name;
            this.services = result.services;
            this.serviceHistory = result.service_history;
          }
        } catch (error) {
          console.error("Unable to connect to the server");
        }
      },
      async deleteRequest(requestId) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/home_owner_dashboard/delete_request/${requestId}`, {  
            method: 'DELETE', 
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('homeownerToken')}`,
              'Content-Type': 'application/json',
            },  
          });
  
          const result = await response.json();
  
          if (!response.ok) {
            console.error(result.message || 'An error occurred');
          } else {
            this.serviceHistory = this.serviceHistory.filter(request => request.id !== requestId);
          }
        } catch (error) {
          console.error("Unable to connect to the server"); 
        }
      },
      navigateToCloseRequest(requestId) {
      console.log('Request ID:', requestId);
      this.$router.push({ name: 'CloseRequest', params: { service_request_id: requestId } });
    }
    }
  }
  </script>
