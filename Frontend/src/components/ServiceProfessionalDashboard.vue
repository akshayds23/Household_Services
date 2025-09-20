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
        <h2>Pending Requests</h2>
        <div v-if="pendingRequests.length > 0" class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>Service Name</th>
                <th>Description</th>
                <th>Price</th>
                <th>Home Owner</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in pendingRequests" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.description }}</td>
                <td>{{ request.price }}</td>
                <td>{{ request.home_owner_name }}</td>
                <td class="d-flex flex-wrap gap-2">
                  <button class="btn btn-success" @click="acceptRequest(request.id)">Accept</button>
                  <button class="btn btn-danger" @click="rejectRequest(request.id)">Reject</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="text-muted">No pending requests.</p>
      </section>

      <section class="container page-section fade-in-up">
        <h2>Accepted Requests</h2>
        <div v-if="acceptedRequests.length > 0" class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>Service Name</th>
                <th>Description</th>
                <th>Price</th>
                <th>Home Owner</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in acceptedRequests" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.description }}</td>
                <td>{{ request.price }}</td>
                <td>{{ request.home_owner_name }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="text-muted">No accepted requests.</p>
      </section>

      <section class="container page-section fade-in-up">
        <h2>Closed Requests</h2>
        <div v-if="closedRequests.length > 0" class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>Service Name</th>
                <th>Description</th>
                <th>Price</th>
                <th>Home Owner</th>
                <th>Rating</th>
                <th>Review</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in closedRequests" :key="request.id">
                <td>{{ request.service_name }}</td>
                <td>{{ request.description }}</td>
                <td>{{ request.price }}</td>
                <td>{{ request.home_owner_name}}</td>
                <td>{{ request.rating }}</td>
                <td>{{ request.review }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="text-muted">No closed requests.</p>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        customerName: '',
        pendingRequests: [],
        acceptedRequests: [],
        closedRequests: []
      }
    },
    mounted() {
      this.fetchServiceProfessionalDashboardData();
    },
    methods: {
      async logout() {
        const response = await fetch('http://127.0.0.1:5000/logout', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('adminToken')}` },
          });
          const result = await response.json();
          this.$router.push('/');
      },
      async fetchServiceProfessionalDashboardData() {
        try {
          const response = await fetch('http://127.0.0.1:5000/service_professional_dashboard', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('serviceProfessionalToken')}`,
              'Content-Type': 'application/json'
            }
          });
          const result = await response.json();
          this.customerName = result.customer_name;
          this.pendingRequests = result.pending_requests;
          this.acceptedRequests = result.accepted_requests;
          this.closedRequests = result.closed_requests;
        } catch (error) {
          console.error("Unable to connect to the server");
        }
      },
      async acceptRequest(requestId) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/service_professional_dashboard/accept_request/${requestId}`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('serviceProfessionalToken')}`,
              'Content-Type': 'application/json'
            }
          });
          const result = await response.json();
          console.log(result);
          this.fetchServiceProfessionalDashboardData(); // Refresh the dashboard data
        } catch (error) {
          console.error("Unable to connect to the server");
        }
      },
      async rejectRequest(requestId) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/service_professional_dashboard/reject_request/${requestId}`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('serviceProfessionalToken')}`,
              'Content-Type': 'application/json'
            }
          });
          const result = await response.json();
          console.log(result);
          this.fetchServiceProfessionalDashboardData(); // Refresh the dashboard data
        } catch (error) {
          console.error("Unable to connect to the server");
        }
      },
    }
  }
  </script> 
