<template>
  <div>
    <nav class="navbar navbar-expand-lg fade-in-up">
      <div class="container">
        <router-link class="navbar-brand" to="/admin_dashboard">Admin Dashboard</router-link>
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
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_dashboard/summary">Summary</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div v-if="isAuthenticated" class="container page-section compact fade-in-up">
      <h1 class="text-center">Services</h1>
      <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th>Service Name</th>
            <th>Description</th>
            <th>Price</th>
            <th>Service Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in services" :key="service.id">
            <td>{{ service.service_name }}</td>
            <td>{{ service.description }}</td>
            <td>{{ service.price }}</td>
            <td>{{ service.service_type }}</td>
            <td>
              <router-link class="btn btn-primary" :to="`/admin_dashboard/edit_service/${service.id}`">Edit</router-link>
              <button class="btn btn-danger" @click="deleteService(service.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      </div>
      <div class="d-flex justify-content-end mt-3">
        <router-link class="btn btn-primary" to="/admin_dashboard/create_service">Create Service</router-link>
      </div>
    </div>

    <div v-if="isAuthenticated" class="container page-section compact fade-in-up">
      <h1 class="text-center">Homeowners</h1>
      <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th>Name</th>
            <th>Address</th>
            <th>Pincode</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in home_owners" :key="user.id">
            <td>{{ user.customer_name }}</td>
            <td>{{ user.address }}</td>
            <td>{{ user.pincode }}</td>
            <td>
              <button class="btn btn-danger" @click="block(user.id)" v-if="!user.is_blocked">Block</button>
              <button class="btn btn-info" @click="unblock(user.id)" v-else>Unblock</button>
            </td>
          </tr>
        </tbody>
      </table>
      </div>
    </div>

    <div v-if="isAuthenticated" class="container page-section compact fade-in-up">
      <h1 class="text-center">Approved Service Professionals</h1>
      <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th>Name</th>
            <th>Address</th>
            <th>Service</th>
            <th>Experience</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sp in approved_service_professionals" :key="sp.id">
            <td><router-link :to="{ name: 'view_service_professional', params: { customer_id: sp.id } }">{{ sp.customer_name }}</router-link></td>
            <td>{{ sp.address }}</td>
            <td>{{ sp.service}}</td>
            <td>{{ sp.service_professional_experience }}</td>
            <td>
              <button class="btn btn-danger" @click="block(sp.id)" v-if="!sp.is_blocked">Block</button>
              <button class="btn btn-info" @click="unblock(sp.id)" v-else>Unblock</button>
            </td>
          </tr>
        </tbody>
      </table>
      </div>
    </div>

    <div v-if="isAuthenticated" class="container page-section compact fade-in-up">
      <h1 class="text-center">Unapproved Service Professionals</h1>
      <div class="table-responsive">
      <table class="table table-striped table-hover">  
        <thead>
          <tr>
            <th>Name</th>
            <th>Address</th>
            <th>Service</th>
            <th>Experience</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sp in unapproved_service_professionals" :key="sp.id">
            <td><router-link :to="`/admin_dashboard/view_service_professional/${sp.id}`">{{ sp.customer_name }}</router-link></td>
            <td>{{ sp.address }}</td> 
            <td>{{ sp.service}}</td>
            <td>{{ sp.service_professional_experience }}</td>
            <td>
              <button class="btn btn-success" @click="approveServiceProfessional(sp.id)">Approve</button>
              <button class="btn btn-danger" @click="rejectServiceProfessional(sp.id)">Reject</button>
            </td> 
          </tr>
        </tbody>
      </table>
      </div>
    </div>
  </div>
</template>
  
  
<script>

export default {
  data() {
    return {
      customer_name: '',
      password: '',
      admin_name: localStorage.getItem('adminName') || '',
      isAuthenticated: !!localStorage.getItem('adminToken'),
      errorMessage: null,
      services: [],
      home_owners: [],
      approved_service_professionals: [],
      unapproved_service_professionals: [],
    };
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

    async getServices() {
      try {
        const response = await fetch('http://127.0.0.1:5000/get_services', {
          method: 'GET',
          headers: { 'Authorization': `Bearer ${localStorage.getItem('adminToken')}` },
        });
        const result = await response.json();
        this.services = result.services;
        } catch (error) {
        console.error(error);
      }
    },
    async getHomeOwners() {
      try {
        const response = await fetch('http://127.0.0.1:5000/get_home_owners', {
          method: 'GET',
          headers: { 'Authorization': `Bearer ${localStorage.getItem('adminToken')}` },
        });
        const result = await response.json();
        this.home_owners = result.home_owners;
      } catch (error) {
        console.error(error);
      }
    },
    async getApprovedServiceProfessionals() {
    try {
        const response = await fetch('http://127.0.0.1:5000/get_approved_service_professionals', {
          method: 'GET',
          headers: { 'Authorization': `Bearer ${localStorage.getItem('adminToken')}` },
        });
        const result = await response.json();
        this.approved_service_professionals = result.approved_service_professionals;
      } catch (error) {
        console.error(error);
      }
    },
    async getUnapprovedServiceProfessionals() {
      try {
        const response = await fetch('http://127.0.0.1:5000/get_unapproved_service_professionals', {
          method: 'GET',
          headers: { 'Authorization': `Bearer ${localStorage.getItem('adminToken')}` },
        });
        const result = await response.json();
        this.unapproved_service_professionals = result.unapproved_service_professionals;
      } catch (error) {
        console.error(error);
      }
    },

    async deleteService(serviceId) {
      try {
        const token = localStorage.getItem('adminToken');
        const headers = {
          'Authorization': `Bearer ${token}`,
      };
      const response = await fetch(`http://127.0.0.1:5000/admin_dashboard/delete_service/${serviceId}`, {
        method: 'DELETE',
        headers,
      });
      const result = await response.json();
      console.log(result);
      this.getServices(); // Refresh the services list
      } catch (error) {
      console.error("Fetch error:", error);
      this.errorMessage = "Unable to connect to the server";
      }
    },
    async approveServiceProfessional(serviceProfessionalId) {
      try {
        const token = localStorage.getItem('adminToken');
        const headers = {
          'Authorization': `Bearer ${token}`,
        };
        const response = await fetch(`http://127.0.0.1:5000/admin_dashboard/approve_service_professional/${serviceProfessionalId}`, {
          method: 'POST',
          headers,
        });
        const result = await response.json();
        console.log(result);
        this.getUnapprovedServiceProfessionals(); 
        this.getApprovedServiceProfessionals();
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Unable to connect to the server";
      }
    },
    async rejectServiceProfessional(serviceProfessionalId) {
      try {
        const token = localStorage.getItem('adminToken');
        const headers = {
          'Authorization': `Bearer ${token}`,
        };
        const response = await fetch(`http://127.0.0.1:5000/admin_dashboard/reject_service_professional/${serviceProfessionalId}`, {
          method: 'POST',
          headers,
        });
        const result = await response.json();
        console.log(result);
        this.getUnapprovedServiceProfessionals(); // Refresh the unapproved service professionals list
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Unable to connect to the server";
      }
    },
    async block(id) {
      try {
        const token = localStorage.getItem('adminToken');
        const headers = {
          'Authorization': `Bearer ${token}`,
        };
        const response = await fetch(`http://127.0.0.1:5000/admin_dashboard/block/${id}`, {
          method: 'POST',
          headers,
        });
        const result = await response.json();
        console.log(result);
        // Update the is_blocked status of the user
        const user = this.approved_service_professionals.find(sp => sp.id === id) || this.home_owners.find(ho => ho.id === id);
        if (user) {
          user.is_blocked = true;
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Unable to connect to the server";
      }
    },
    async unblock(id) {
      try {
        const token = localStorage.getItem('adminToken');
        const headers = {
          'Authorization': `Bearer ${token}`,
        };
        const response = await fetch(`http://127.0.0.1:5000/admin_dashboard/unblock/${id}`, {
          method: 'POST',
          headers,
        });
        const result = await response.json();
        const user = this.approved_service_professionals.find(sp => sp.id === id) || this.home_owners.find(ho => ho.id === id);
        if (user) {
          user.is_blocked = false;
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Unable to connect to the server";
      }
    },
  },
  mounted() {
    this.getServices();
    this.getHomeOwners();
    this.getApprovedServiceProfessionals();
    this.getUnapprovedServiceProfessionals();
  },
};
</script>
  
  