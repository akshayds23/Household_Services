
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
    <div class="container page-section compact fade-in-up">
      <h1 class="text-center">Admin Search</h1>
      <form @submit.prevent="search">
        <div class="mb-3">
          <label for="search_by" class="form-label">Search By:</label>
          <select class="form-select" id="search_by" v-model="searchBy">
            <option value="customer_name">Home Owner</option>
            <option value="service_name">Service</option>
            <option value="service_professional_name">Service Professional</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="search_term" class="form-label">Search Term:</label>
          <input type="text" class="form-control" id="search_term" v-model="searchTerm" placeholder="Enter search term">
        </div>
        <button type="submit" class="btn btn-primary">Search</button>
      </form>
      <div v-if="home_owners.length > 0" class="mt-5 table-responsive">
        <h2>Home Owners:</h2>
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th>Customer Name</th>
              <th>Phone Number</th>
              <th>Address</th>
              <th>Pincode</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in home_owners":key="home_owners.id">
              <td>{{ user.customer_name }}</td>
              <td>{{ user.contact_phone }}</td>
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
      <div v-if="services.length > 0" class="mt-5 table-responsive">
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
      <div v-if="approved_service_professionals.length" class="mt-5 table-responsive">
        <h2>Service Professionals:</h2>
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th>Service Professional Name</th>
              <th>Phone Number</th>
              <th>Address</th>
              <th>Pincode</th>
              <th>Actions</th>
            </tr>
          </thead>
        <tbody>
          <tr v-for="asp in approved_service_professionals" :key="approved_service_professionals.id">
            <td>{{ asp.customer_name }}</td>
            <td>{{ asp.contact_phone }}</td>
            <td>{{ asp.address }}</td>
            <td>{{ asp.pincode }}</td>
            <td>
              <button class="btn btn-danger" @click="block(asp.id)" v-if="!asp.is_blocked">Block</button>
              <button class="btn btn-info" @click="unblock(asp.id)" v-else>Unblock</button>
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
        searchBy: '',
        searchTerm: '',
        customers: null,
        services: [],
        home_owners: [],
        approved_service_professionals: [],
        errorMessage: null
      };
    },
    methods: {
      async logout() {
      const response = await fetch('http://127.0.0.1:5000/logout', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${localStorage.getItem('adminToken')}` },
        });
        this.$router.push('/');
    },
    async search() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/admin_dashboard/search`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('adminToken')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            search_by: this.searchBy,
            search_term: this.searchTerm
          })
        });
        if (!response.ok) {
          throw new Error(`Server returned an error: ${response.status} ${response.statusText}`);
        }
        const result = await response.json();
        const key = Object.keys(result)[0];
        console.log(result);

        if (this.searchBy === "customer_name") {
          this.home_owners = result.home_owners;
        }else if(this.searchBy === "service_name"){
          this.services = result.services;
        }else if(this.searchBy === "service_professional_name"){
          this.approved_service_professionals = result.approved_service_professionals;
        }

      } catch (error) {
        console.error(error);
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

        console.log(user);
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
        console.log(result);
        // Update the is_blocked status of the user
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
  };
  </script>
