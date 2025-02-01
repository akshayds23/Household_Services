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
        <h2>Bidding Requests</h2>
        <div class="table-responsive">
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th>Request ID</th>
              <th>Service Name</th>
              <th>Service Professional</th>
              <th>Bid Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in requests" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.service_name || 'N/A' }}</td>
              <td>{{ request.service_professional_name || 'N/A' }}</td>
              <td>{{ request.service_status || 'N/A' }}</td>
              <td>
                <button class="btn btn-success" @click="acceptBid(request.id)">Accept</button>
                <button class="btn btn-danger" @click="rejectBid(request.id)">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
        </div>
        <p class="text-center text-muted" v-if="!requests.length">No requests are available.</p>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        customerName: '',
        requests: []
      }
    },
    mounted() {
      this.fetchHomeOwnerDashboardData();
    },
    methods: {
      async logout() {
        const response = await fetch('http://127.0.0.1:5000/logout', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('homeownerToken')}` },
          });
          const result = await response.json();
          this.$router.push('/');
      },
      async fetchHomeOwnerDashboardData() {
        try {
          const response = await fetch('http://127.0.0.1:5000/home_owner_dashboard/bidding_requests', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('homeownerToken')}`,
              'Content-Type': 'application/json',
            },
          });
  
          const result = await response.json();
          if (!response.ok) {
            console.error(result.message || 'An error occurred');
          } else {
            this.customerName = result.customer_name;
            this.requests = result.requests;
          }
        } catch (error) {
          console.error("Unable to connect to the server");
        }
      },
      async acceptBid(requestId) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/home_owner_dashboard/accept_bid/${requestId}`, {  
            method: 'PUT', 
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('homeownerToken')}`,
              'Content-Type': 'application/json',
            },  
          });
  
          const result = await response.json();
  
          if (!response.ok) {
            console.error(result.message || 'An error occurred');
          } else {
            this.requests = this.requests.filter(request => request.id !== requestId);
          }
        } catch (error) {
          console.error("Unable to connect to the server"); 
        }
      },
      async rejectBid(requestId) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/home_owner_dashboard/reject_bid/${requestId}`, {  
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
            this.requests = this.requests.filter(request => request.id !== requestId);      
          }
        }
        catch (error) {
          console.error("Unable to connect to the server"); 
        }
      }
    }  
  };
  </script>
