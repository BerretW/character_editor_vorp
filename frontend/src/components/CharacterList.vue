<template>
  <div>
    <div>
      <input
        type="text"
        v-model="searchTerm"
        @input="fetchCharacters"
        placeholder="Search Characters"
      />
      <button @click="fetchCharacters">Search</button>
    </div>

    <!-- Výpis postav -->
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

      <!-- Stránkování -->
      <div class="pagination">
        <button :disabled="currentPage === 1" @click="previousPage">Previous</button>
        <span>{{ currentPage }} / {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="nextPage">Next</button>
      </div>
    </div>
    <div v-else>
      <p>No characters found.</p>
    </div>

    <!-- Modal pro editaci (pokud je showEditModal = true) -->
    <div v-if="showEditModal" class="modal-backdrop">
      <div class="modal-content">
        <h2>
          Editace postavy (ID: {{ editData.charidentifier }})
        </h2>

        <!-- Základní údaje -->
        <h3>Basic Info</h3>
        <label>Firstname: <input type="text" v-model="editData.firstname" /></label><br />
        <label>Lastname: <input type="text" v-model="editData.lastname" /></label><br />
        <label>Nickname: <input type="text" v-model="editData.nickname" /></label><br />
        <label>Steam Name: <input type="text" v-model="editData.steamname" /></label><br />
        <label>Money: <input type="number" v-model.number="editData.money" /></label><br />
        <label>XP: <input type="number" v-model.number="editData.xp" /></label><br />

        <!-- Ukázka, jak zacházet s JSONem "skinPlayer" -->
        <h3>Skin Player</h3>
        <div v-for="(val, key) in editData.skinPlayer" :key="key" class="json-field">
          <label>{{ key }}:
            <!-- Podle typu val poznáš, jestli to je number, string apod. -->
            <input
              v-model="editData.skinPlayer[key]"
              :type="typeof val === 'number' ? 'number' : 'text'"
            />
          </label>
        </div>

        <!-- JSON "compPlayer" -->
        <h3>Comp Player</h3>
        <div v-for="(val, key) in editData.compPlayer" :key="key" class="json-field">
          <label>{{ key }}:
            <input
              v-model="editData.compPlayer[key]"
              :type="typeof val === 'number' ? 'number' : 'text'"
            />
          </label>
        </div>

        <!-- JSON "compTints" -->
        <h3>Comp Tints</h3>
        <div v-for="(val, key) in editData.compTints" :key="key" class="json-field">
          <label>{{ key }}:
            <!-- compTints je často složitá struktura se sub-objekty, je to spíš ukázka -->
            <input
              v-model="editData.compTints[key]"
              :type="typeof val === 'number' ? 'number' : 'text'"
            />
          </label>
        </div>

        <!-- Můžeš přidat totéž pro coords, inventory, status atd. -->
        <h3>Coords</h3>
        <div v-for="(val, key) in editData.coords" :key="key" class="json-field">
          <label>{{ key }}:
            <input
              v-model="editData.coords[key]"
              :type="typeof val === 'number' ? 'number' : 'text'"
            />
          </label>
        </div>

        <div style="margin-top: 1rem;">
          <button @click="saveChanges">Uložit</button>
          <button @click="closeModal">Zavřít</button>
        </div>
      </div>
    </div>

    <!-- Modal pro move (pokud moveTarget není null) -->
    <div v-if="moveTarget" class="modal-backdrop">
      <div class="modal-content">
        <h2>Move Character</h2>
        <form @submit.prevent="submitMove">
          <label>New Identifier: <input type="text" v-model="moveTarget.identifier" /></label><br>
          <button type="submit">Move</button>
          <button @click="closeMove">Close</button>
        </form>
      </div>
    </div>

    <!-- Tlačítko Logout -->
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CharacterList',
  data() {
    return {
      characters: [],
      currentPage: 1,
      totalPages: 1,
      perPage: 10,
      searchTerm: '',
      apiUrl: 'http://localhost:5000',

      // Editace (modal)
      showEditModal: false,
      editData: {},

      // Move
      moveTarget: null,

      // Můžeš si ponechat i staré selectedCharacter, ale tady už to řešíme jako editData
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    },

    async fetchCharacters() {
      const token = localStorage.getItem('token');
      try {
        const response = await axios.get(`${this.apiUrl}/characters`, {
          headers: {
            Authorization: `Bearer ${token}`
          },
          params: {
            page: this.currentPage,
            per_page: this.perPage,
            search: this.searchTerm
          }
        });
        this.characters = response.data;
        // Tady si zkus spočítat totalPages na základě nějaké reálné velikosti.
        // Pokud backend posílá jen tuto jednu "batch" a ne celkové count, musíš to řešit jinak.
        this.totalPages = this.characters.length < this.perPage
          ? this.currentPage
          : this.currentPage + 1; // orientační
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$router.push('/login');
        }
        console.error('Error fetching characters:', error);
      }
    },

    editCharacter(character) {
      // Naplníme editData včetně parsování JSON polí
      this.editData = {
        // normální klíče
        charidentifier: character.charidentifier,
        firstname: character.firstname,
        lastname: character.lastname,
        nickname: character.nickname,
        steamname: character.steamname,
        money: character.money,
        xp: character.xp,

        // JSON klíče
        skinPlayer: character.skinPlayer ? JSON.parse(character.skinPlayer) : {},
        compPlayer: character.compPlayer ? JSON.parse(character.compPlayer) : {},
        compTints: character.compTints ? JSON.parse(character.compTints) : {},
        coords: character.coords ? JSON.parse(character.coords) : {},
        // a tak dále pro inventory, status, meta...
      };

      this.showEditModal = true;
    },

    closeModal() {
      this.showEditModal = false;
      this.editData = {};
    },

    async saveChanges() {
      const updatedCharacter = {
        // Tyto klíče bere tvůj backend jako povinné:
        charidentifier: this.editData.charidentifier,
        identifier: this.editData.identifier,
        steamname: this.editData.steamname,
        group: this.editData.group,
        money: this.editData.money,
        gold: this.editData.gold,
        rol: this.editData.rol,
        xp: this.editData.xp,
        healthouter: this.editData.healthouter,
        healthinner: this.editData.healthinner,
        staminaouter: this.editData.staminaouter,
        staminainner: this.editData.staminainner,
        hours: this.editData.hours,
        LastLogin: this.editData.LastLogin,
        inventory: JSON.stringify(this.editData.inventory),
        slots: this.editData.slots,
        job: this.editData.job,
        joblabel: this.editData.joblabel,
        status: JSON.stringify(this.editData.status),
        meta: JSON.stringify(this.editData.meta),
        firstname: this.editData.firstname,
        lastname: this.editData.lastname,
        character_desc: this.editData.character_desc,
        gender: this.editData.gender,
        age: this.editData.age,
        nickname: this.editData.nickname,
        skinPlayer: JSON.stringify(this.editData.skinPlayer),
        compPlayer: JSON.stringify(this.editData.compPlayer),
        compTints: JSON.stringify(this.editData.compTints),
        jobgrade: this.editData.jobgrade,
        coords: JSON.stringify(this.editData.coords),
        isdead: this.editData.isdead,
        trust: this.editData.trust,
        walk: this.editData.walk,
        crafting: JSON.stringify(this.editData.crafting),
        info: JSON.stringify(this.editData.info),
        gunsmith: this.editData.gunsmith,
        ammo: JSON.stringify(this.editData.ammo),
        discordid: this.editData.discordid,
        lastjoined: JSON.stringify(this.editData.lastjoined),
        ranchid: this.editData.ranchid
      };

      const token = localStorage.getItem('token');
      try {
        await axios.put(
          `${this.apiUrl}/characters/${updatedCharacter.charidentifier}`,
          updatedCharacter,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        this.closeModal();
        this.fetchCharacters();
      } catch (error) {
        console.error('Error updating character:', error);
      }
    },

    async deleteCharacter(charidentifier) {
      const token = localStorage.getItem('token');
      if (confirm('Are you sure you want to delete this character?')) {
        try {
          await axios.delete(`${this.apiUrl}/characters/${charidentifier}`, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          this.fetchCharacters();
        } catch (error) {
          if (error.response && error.response.status === 401) {
            this.$router.push('/login');
          }
          console.error('Error deleting character:', error);
        }
      }
    },

    async copyCharacter(charidentifier) {
      const newIdentifier = prompt('Enter new identifier for the copied character');
      if (!newIdentifier) return;
      const token = localStorage.getItem('token');
      try {
        // Důležité: backend čeká `new_identifier`, ne `identifier`
        await axios.post(
          `${this.apiUrl}/characters/${charidentifier}/copy`,
          { new_identifier: newIdentifier },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        this.fetchCharacters();
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$router.push('/login');
        }
        console.error('Error copying character:', error);
      }
    },

    moveCharacter(charidentifier) {
      this.moveTarget = {
        charidentifier,
        identifier: ''
      };
    },

    closeMove() {
      this.moveTarget = null;
    },

    async submitMove() {
      if (!this.moveTarget.identifier) return alert('Identifier cannot be empty');
      const token = localStorage.getItem('token');
      try {
        // Backend čeká `new_identifier`, ne `identifier`
        await axios.post(
          `${this.apiUrl}/characters/${this.moveTarget.charidentifier}/move`,
          { new_identifier: this.moveTarget.identifier },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        this.closeMove();
        this.fetchCharacters();
      } catch (error) {
        if (error.response && error.response.status === 401) {
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
    }
  },
  mounted() {
    this.fetchCharacters();
  }
};
</script>

<style scoped>
.character-card {
  border: 1px solid #ccc;
  margin: 0.5rem;
  padding: 0.5rem;
}
.pagination {
  margin-top: 1rem;
}
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background: #fff;
  padding: 1rem 2rem;
  border-radius: 6px;
  max-height: 80%;
  overflow-y: auto;
}
.json-field {
  margin-left: 1rem;
}
</style>
