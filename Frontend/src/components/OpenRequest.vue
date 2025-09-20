<template>
    <div>
      <nav class="navbar navbar-expand-lg fade-in-up">
        <div class="container">
          <a class="navbar-brand" href="/service_professional_dashboard">Service Professional Dashboard : {{ customerName }}</a>
          <button class="navbar-toggler" type="button" data-mdb-toggle="collapse" data-mdb-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
              <li class="nav-item">
                <router-link class="nav-link" to="/service_professional_dashboard">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/service_professional_dashboard/open_requests_service_professional">Open Requests</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/data_export">Export Data</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/logout" @click="logout">Logout</router-link>
              </li>
              
            </ul>
          </div>
        </div>
      </nav>
      <section class="container page-section fade-in-up">
        <h3>Open Requests</h3>
        <div v-if="receivedRequests.length > 0" class="stagger-child">
          <div v-for="request in receivedRequests" :key="request.id" class="card mt-3">
            <div class="card-body">
              <h5 class="card-title">{{ request.service_name }}</h5>
              <p class="card-text">Requested by {{ request.home_owner_name }}</p>
              <p class="card-text">Created on {{ request.date_of_request }}</p>
              <router-link :to="`/service_professional_dashboard/bid_request/${request.id}`" class="btn btn-primary mt-3">Bid Request</router-link>
            </div>
          </div>
        </div>
        <p v-else class="text-center text-muted">No open requests are available.</p>
      </section>

      <section class="container page-section fade-in-up">
        <h3>Sent Requests</h3>
        <div v-if="sentRequests.length > 0" class="stagger-child">
          <div v-for="request in sentRequests" :key="request.id" class="card mt-3">
            <div class="card-body">
              <h5 class="card-title">{{ request.service_name }}</h5>
              <p class="card-text">Requested by {{ request.customer_name }}</p>
              <p class="card-text">Submitted on {{ request.date_of_request }}</p>
              <p class="card-text">Message: {{ request.description }}</p>
            </div>
          </div>
        </div>
        <p v-else class="text-center text-muted">No sent requests.</p>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        customerName: '',
        receivedRequests: [],
        sentRequests: []
      };
    },
    methods: {
      async logout() {
        const response = await fetch('http://127.0.0.1:5000/logout', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${localStorage.getItem('serviceProfessionalToken')}` },
        });
        await response.json();
        this.$router.push('/');
      },
      async fetchRequests() {
        try {
          const response = await fetch('http://127.0.0.1:5000/service_professional_dashboard/open_requests_service_professional', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('serviceProfessionalToken')}`,
              'Content-Type': 'application/json'
            },
          });
          const result = await response.json();
          
          // Safely assign data
          this.customerName = result.customer_name || 'Unknown';
          this.receivedRequests = result.received_requests || [];
          this.sentRequests = result.sent_requests || [];
        } catch (error) {
          console.error("Error fetching requests:", error);
        }
      }
    },
    mounted() {
      this.fetchRequests();
    }
  };
  </script>
  
