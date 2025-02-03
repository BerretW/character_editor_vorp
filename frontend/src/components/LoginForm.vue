<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <label>Username: <input type="text" v-model="username" /></label><br />
      <label>Password: <input type="password" v-model="password" /></label
      ><br />
      <button type="submit">Login</button>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    </form>
  </div>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
      apiUrl: "http://localhost:5000",
    };
  },
  methods: {
    async login() {
  try {
    const data = new URLSearchParams();
    console.log([...data.entries()]);
    data.append("username", this.username);
    data.append("password", this.password);

    const response = await axios.post(`${this.apiUrl}/auth/login`, data, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    localStorage.setItem("token", response.data.access_token);
    this.$router.push("/");
  } catch (error) {
    this.errorMessage = "Invalid username or password.";
    console.error("Login failed:", error);
  }
},

  },
};
</script>
