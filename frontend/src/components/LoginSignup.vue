<template>
    <div class="container mx-auto">
      <div class="max-w-md mx-auto my-10">
        <div class="text-center mb-6">
          <h1 class="text-3xl font-semibold">Spotfest</h1>
          <p v-if="isLogin">Please login to your account</p>
          <p v-else>Sign up for a new account</p>
        </div>
        <div class="m-7">
          <form @submit.prevent="handleSubmit">
            <div class="mb-6">
              <!-- Email Input -->
              <label for="email" class="block mb-2 text-sm text-gray-600">Email</label>
              <input type="text" v-model="email" name="email" id="email" placeholder="Email" class="w-full px-3 py-2 placeholder-gray-300 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-300" required>
            </div>

            <div class="mb-6" v-if="!isLogin">
              <!-- Username Input -->
              <label for="username" class="block mb-2 text-sm text-gray-600">Username</label>
              <input type="text" v-model="username" name="username" id="username" placeholder="username" class="w-full px-3 py-2 placeholder-gray-300 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-300" required>
            </div>

            <div class="mb-6">
              <!-- Password Input -->
              <label for="password" class="text-sm text-gray-600">Password</label>
              <input type="password" v-model="password" name="password" id="password" placeholder="Password" class="w-full px-3 py-2 placeholder-gray-300 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-300" required>
            </div>
            
            <div class="mb-6">
              <!-- Submit Button -->
              <button type="submit" class="w-full px-3 py-4 text-white bg-blue-500 rounded-md focus:bg-blue-600 focus:outline-none">{{ isLogin ? 'Login' : 'Sign Up' }}</button>
            </div>
            <p class="text-sm text-center text-gray-400">
              {{ isLogin ? 'No account yet?' : 'Already have an account?' }}
              <button @click="toggleLogin" class="text-blue-500 focus:outline-none focus:underline">{{ isLogin ? 'Sign up' : 'Login' }}</button>
            </p>

            <div v-if="errorMessage" class="text-red-500 text-sm mt-2">
                {{ errorMessage }}
            </div>
            <div v-if="successMessage" class="text-green-500 text-sm mt-2">
                {{ successMessage }}
            </div>

          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>

  import axios from '@/services/axios';

  export default {
    data() {
      return {
        isLogin: true,
        email: '',
        password: '',
        username: '',
        errorMessage: '',
        successMessage: ''
      };
    },
    methods: {
      toggleLogin() {
        this.isLogin = !this.isLogin;
      },
      async handleSubmit() {

        try {
            this.errorMessage = '';
            this.successMessage = '';
            if (this.isLogin) {
                const response = await axios.post("/login", {email: this.email, password: this.password});
                this.successMessage = "Login successful!";
                console.log(response);
                return response;
            } else {
                const response = await axios.post("/signup", {email: this.email, password: this.password, username: this.username});
                this.successMessage = 'Signup successful! Check your email to confirm your account.';
                console.log(response);
                this.$router.push("/login");
            }

        } catch (error) {
            if (error.response && error.response.data) {
                // Set the error message from the response
                this.errorMessage = error.response.data.detail;
            } else {
                // Generic error message if the response is not available
                this.errorMessage = 'An error occurred. Please try again.';
            }
        }
      },
    },
  };
  </script>
  
  <style>
  /* Add any additional styling here */
  </style>
  