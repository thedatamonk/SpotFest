<template>
    <div class="min-h-screen bg-gray-100">
      <!-- Navigation bar -->
      <nav class="bg-white shadow">
        <!-- Nav content -->
      </nav>
  
      <!-- Main content area -->
      <main class="pt-8 container mx-auto px-4">
        <!-- Welcome message -->
        <div class="text-4xl font-bold text-gray-900 mb-6">
          <h1>Welcome, {{ user.username }} 👋</h1>
        </div>
  
        <!-- Event filters -->
        <div class="flex flex-col md:flex-row justify-between mb-6">
          <!-- Filter dropdowns -->
        </div>
  
        <!-- Calendar view -->
        <div class="mb-6">
          <!-- Calendar component -->
        </div>
  
        <!-- Event list header -->
        <div class="flex justify-between items-center mb-2">
          <h2 class="text-2xl font-semibold text-gray-800">Your next events</h2>
          <a href="#" class="text-blue-600 hover:text-blue-700 transition duration-300">View all</a>
        </div>
  
        <!-- Events list -->
        <div class="space-y-4">
          <!-- Event cards -->
        </div>
      </main>
    </div>
  </template>
  


<script>
    import axios from "@/services/axios";

    export default {
        data() {
            return {
                isAuthenticated: this.$store.state.isLoggedIn,
                user: {
                    username: '',
                    email: ''
                },
            };
        },

        methods: {
            async fetchUserData() {
                try {
                    const response = await axios.get("/users/me", {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                    this.user = response.data;
                } catch (error) {
                    console.error(error);
                }
            }
        },

        created() {
            this.fetchUserData();
        },
    }
</script>