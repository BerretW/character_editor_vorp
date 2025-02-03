<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="login">
            <label>Username: <input type="text" v-model="username"/></label><br>
            <label>Password: <input type="password" v-model="password"/></label><br>
             <button type="submit">Login</button>
             <div v-if="errorMessage" class="error">{{errorMessage}}</div>
        </form>
    </div>
</template>
<script>
import axios from 'axios';
export default{
    data() {
        return{
            username:'',
            password:'',
            errorMessage:'',
            apiUrl:'http://localhost:5000'
        }
    },
    methods: {
        async login() {
           try {
                   const formData = new FormData();
                  formData.append('username', this.username);
                   formData.append('password', this.password);

                  const response = await axios.post(`${this.apiUrl}/login`,formData);
                   localStorage.setItem('token', response.data.access_token);
                   this.$router.push('/'); // Redirect to home after login.

           } catch (error) {
             this.errorMessage='Invalid username or password.';
              console.error('Login failed:', error);
           }
        }
    }
}
</script>