<template>
    <div>
       <input type="text" v-model="searchTerm" @input="fetchCharacters" placeholder="Search Characters" />
        <button @click="fetchCharacters">Search</button>
      <div v-if="characters.length > 0">
          <div v-for="character in characters" :key="character.charidentifier" class="character-card">
              <h2>{{ character.firstname }} {{ character.lastname }}</h2>
              <p>Nickname: {{ character.nickname }}</p>
               <p>Steam Name: {{ character.steamname }}</p>
              <button @click="editCharacter(character)">Edit</button>
              <button @click="deleteCharacter(character.charidentifier)">Delete</button>
              <button @click="copyCharacter(character.charidentifier)">Copy</button>
               <button @click="moveCharacter(character.charidentifier)">Move</button>
          </div>
      <div class="pagination">
          <button :disabled="currentPage === 1" @click="previousPage">Previous</button>
          <span>{{ currentPage }} / {{ totalPages }}</span>
          <button :disabled="currentPage === totalPages" @click="nextPage">Next</button>
      </div>
      </div>
          <div v-else>
              <p>No characters found.</p>
          </div>
          <div v-if="selectedCharacter">
              <h2>Edit Character</h2>
                  <form @submit.prevent="submitEdit">
                        <label>First Name: <input type="text" v-model="selectedCharacter.firstname" /></label><br>
                        <label>Last Name: <input type="text" v-model="selectedCharacter.lastname" /></label><br>
                        <label>Nickname: <input type="text" v-model="selectedCharacter.nickname" /></label><br>
                        <label>Steam Name: <input type="text" v-model="selectedCharacter.steamname" /></label><br>
                       <label>Group: <input type="text" v-model="selectedCharacter.group" /></label><br>
                       <label>Money: <input type="number" v-model.number="selectedCharacter.money" /></label><br>
                      <label>Gold: <input type="number" v-model.number="selectedCharacter.gold" /></label><br>
                       <label>ROL: <input type="number" v-model.number="selectedCharacter.rol" /></label><br>
                       <label>XP: <input type="number" v-model.number="selectedCharacter.xp" /></label><br>
                       <label>Health Outer: <input type="number" v-model.number="selectedCharacter.healthouter" /></label><br>
                       <label>Health Inner: <input type="number" v-model.number="selectedCharacter.healthinner" /></label><br>
                       <label>Stamina Outer: <input type="number" v-model.number="selectedCharacter.staminaouter" /></label><br>
                       <label>Stamina Inner: <input type="number" v-model.number="selectedCharacter.staminainner" /></label><br>
                       <label>Hours: <input type="number" v-model.number="selectedCharacter.hours" /></label><br>
                      <label>Slots: <input type="number" v-model.number="selectedCharacter.slots" /></label><br>
                      <label>Job: <input type="text" v-model="selectedCharacter.job" /></label><br>
                      <label>Job Label: <input type="text" v-model="selectedCharacter.joblabel" /></label><br>
                        <label>Character Description: <textarea v-model="selectedCharacter.character_desc"></textarea></label><br>
                        <label>Gender: <input type="text" v-model="selectedCharacter.gender" /></label><br>
                        <label>Age: <input type="number" v-model.number="selectedCharacter.age" /></label><br>
                         <label>Job Grade: <input type="number" v-model.number="selectedCharacter.jobgrade" /></label><br>
                          <label>isDead: <input type="checkbox" v-model="selectedCharacter.isdead" /></label><br>
                         <label>trust: <input type="number" v-model.number="selectedCharacter.trust" /></label><br>
                           <label>walk: <input type="text" v-model="selectedCharacter.walk" /></label><br>
                            <label>discordId: <input type="text" v-model="selectedCharacter.discordid" /></label><br>
                           <label>ranchId: <input type="number" v-model.number="selectedCharacter.ranchid" /></label><br>
                          <label>Inventory: <textarea v-model="selectedCharacter.inventory" /></label>
                          <label>Status: <textarea v-model="selectedCharacter.status" /></label>
                          <label>Meta: <textarea v-model="selectedCharacter.meta" /></label>
                           <label>Skin Player: <textarea v-model="selectedCharacter.skinPlayer" /></label>
                           <label>Comp Player: <textarea v-model="selectedCharacter.compPlayer" /></label>
                           <label>Comp Tints: <textarea v-model="selectedCharacter.compTints" /></label>
                            <label>Coords: <textarea v-model="selectedCharacter.coords" /></label>
                              <label>Crafting: <textarea v-model="selectedCharacter.crafting" /></label>
                              <label>Info: <textarea v-model="selectedCharacter.info" /></label>
                           <label>Gunsmith: <input type="number" v-model.number="selectedCharacter.gunsmith" /></label>
                           <label>Ammo: <textarea v-model="selectedCharacter.ammo" /></label>
                     <button type="submit">Update</button>
                     <button @click="closeEdit">Close</button>
                  </form>
          </div>
               <div v-if="moveTarget">
                    <h2>Move Character</h2>
                       <form @submit.prevent="submitMove">
                           <label>New Identifier: <input type="text" v-model="moveTarget.identifier" /></label><br>
                             <button type="submit">Move</button>
                                  <button @click="closeMove">Close</button>
                      </form>
  
                </div>
    </div>
    <button @click="logout">Logout</button>
  </template>


  <script>
  import axios from 'axios';
  
  export default {
    name: 'LogoutButton',

      data() {
          return {
              characters: [],
               selectedCharacter: null,
              moveTarget:null,
              currentPage: 1,
              totalPages: 1,
              perPage: 10,
               searchTerm: '',
              apiUrl: 'http://localhost:5000',
              itemsPerPageOptions: [10, 20, 50, 100], // Dostupné možnosti pro položek na stránku
  
          };
      },
      methods: {
        logout() {
        localStorage.removeItem('token');  // vymaže token
        this.$router.push('/login');         // přesměruje uživatele na přihlášení
      },
          async fetchCharacters() {
              const token = localStorage.getItem('token');
                try {
                    const response = await axios.get(`${this.apiUrl}/characters`, {
                      headers:{
                        Authorization:`Bearer ${token}`
                      },
                      params:{
                        page:this.currentPage,
                          per_page: this.perPage,
                            search: this.searchTerm
                             }
  
                      });
                      this.characters = response.data;
                      this.totalPages = Math.ceil(this.characters.length / this.perPage)
                  } catch (error) {
                     if(error.response && error.response.status === 401){
                       this.$router.push('/login'); // Redirect to login if token is invalid
                       }
                     console.error('Error fetching characters:', error);
                  }
              },
                editCharacter(character) {
                this.selectedCharacter = { ...character };
                // parse JSON data
                this.selectedCharacter.inventory = JSON.parse(character.inventory || '{}');
                this.selectedCharacter.status = JSON.parse(character.status || '{}');
                this.selectedCharacter.meta = JSON.parse(character.meta || '{}');
                this.selectedCharacter.skinPlayer = JSON.parse(character.skinPlayer || '{}');
                this.selectedCharacter.compPlayer = JSON.parse(character.compPlayer || '{}');
                this.selectedCharacter.compTints = JSON.parse(character.compTints || '{}');
                this.selectedCharacter.coords = JSON.parse(character.coords || '{}');
                this.selectedCharacter.crafting = JSON.parse(character.crafting || '{}');
                this.selectedCharacter.info = JSON.parse(character.info || '{}');
                  this.selectedCharacter.ammo = JSON.parse(character.ammo || '{}');
  
              },
               closeEdit(){
                  this.selectedCharacter=null;
              },
              async submitEdit() {
               if(this.selectedCharacter.inventory){
                          this.selectedCharacter.inventory = JSON.stringify(this.selectedCharacter.inventory);
                  }
                     if(this.selectedCharacter.status){
                      this.selectedCharacter.status = JSON.stringify(this.selectedCharacter.status);
                     }
                      if(this.selectedCharacter.meta){
                           this.selectedCharacter.meta = JSON.stringify(this.selectedCharacter.meta);
                      }
                       if(this.selectedCharacter.skinPlayer){
                             this.selectedCharacter.skinPlayer = JSON.stringify(this.selectedCharacter.skinPlayer)
                      }
                        if(this.selectedCharacter.compPlayer){
                             this.selectedCharacter.compPlayer = JSON.stringify(this.selectedCharacter.compPlayer)
                        }
                       if(this.selectedCharacter.compTints){
                            this.selectedCharacter.compTints = JSON.stringify(this.selectedCharacter.compTints);
                     }
                     if(this.selectedCharacter.coords){
                          this.selectedCharacter.coords = JSON.stringify(this.selectedCharacter.coords);
                       }
                     if(this.selectedCharacter.crafting){
                         this.selectedCharacter.crafting = JSON.stringify(this.selectedCharacter.crafting);
                      }
                      if(this.selectedCharacter.info){
                          this.selectedCharacter.info=JSON.stringify(this.selectedCharacter.info)
                       }
                      if(this.selectedCharacter.ammo){
                          this.selectedCharacter.ammo = JSON.stringify(this.selectedCharacter.ammo)
                        }
                     const token = localStorage.getItem('token');
                  try {
                           await axios.put(`${this.apiUrl}/characters/${this.selectedCharacter.charidentifier}`, this.selectedCharacter, {
                            headers:{
                              Authorization:`Bearer ${token}`
                              }
                         });
                        this.closeEdit();
                       this.fetchCharacters();
                      } catch (error) {
                         if(error.response && error.response.status === 401){
                           this.$router.push('/login'); // Redirect to login if token is invalid
                        }
                           console.error('Error updating character:', error);
                      }
              },
              async deleteCharacter(charidentifier) {
                  const token = localStorage.getItem('token');
                  if(confirm('Are you sure you want to delete this character?')) {
                       try {
                          await axios.delete(`${this.apiUrl}/characters/${charidentifier}`,{
                              headers:{
                                    Authorization:`Bearer ${token}`
                                   }
                          });
                           this.fetchCharacters();
                      } catch(error) {
                         if(error.response && error.response.status === 401){
                             this.$router.push('/login');
                          }
                           console.error('Error deleting character:', error);
                      }
                  }
              },
              async copyCharacter(charidentifier) {
                  const newIdentifier = prompt('Enter new identifier for the copied character');
                  if(!newIdentifier) return;
                  const token = localStorage.getItem('token');
                  try {
                           await axios.post(`${this.apiUrl}/characters/${charidentifier}/copy`,{ identifier:newIdentifier},{
                               headers:{
                                    Authorization:`Bearer ${token}`
                                  }});
                           this.fetchCharacters();
                        } catch (error) {
                             if(error.response && error.response.status === 401){
                             this.$router.push('/login');
                              }
                              console.error('Error copying character:', error);
                       }
              },
               moveCharacter(charidentifier) {
               this.moveTarget = {
                   charidentifier: charidentifier,
                 identifier: '',
                     };
                  },
              closeMove(){
                  this.moveTarget=null;
               },
            async submitMove() {
              if (!this.moveTarget.identifier) return alert('Identifier cannot be empty')
               const token = localStorage.getItem('token');
               try {
                      await axios.post(`${this.apiUrl}/characters/${this.moveTarget.charidentifier}/move`,{ identifier:this.moveTarget.identifier},{
                          headers:{
                               Authorization:`Bearer ${token}`
                              }
                      });
                      this.closeMove();
                       this.fetchCharacters();
                    } catch (error) {
                        if(error.response && error.response.status === 401){
                          this.$router.push('/login');
                         }
                       console.error('Error moving character:', error);
                      }
            },
          previousPage() {
             if (this.currentPage > 1) {
             this.currentPage--;
             this.fetchCharacters();
             }
           },
              nextPage() {
              if (this.currentPage < this.totalPages) {
                  this.currentPage++;
               this.fetchCharacters();
              }
          },
          setPerPage(perPage) {
            this.perPage = perPage;
            this.currentPage = 1;
              this.fetchCharacters();
          },
      },
      mounted() {
          this.fetchCharacters();
       }
  }
  </script>