<template>
  <div>
    <!-- Vyhledávání + tlačítko -->
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

    <!-- MODAL PRO EDITACI POSTAVY -->
    <div v-if="showEditModal" class="modal-backdrop">
      <div class="modal-content">
        <h2>Upravit postavu (ID: {{ editData.charidentifier }})</h2>

        <!-- 1) Základní info -->
        <h3>Základní informace</h3>
        <label>Char ID: <input type="number" v-model.number="editData.charidentifier" readonly /></label><br />
        <label>Identifier: <input type="text" v-model="editData.identifier" /></label><br />
        <label>Steam Name: <input type="text" v-model="editData.steamname" /></label><br />
        <label>Group: <input type="text" v-model="editData.group" /></label><br />
        <label>Firstname: <input type="text" v-model="editData.firstname" /></label><br />
        <label>Lastname: <input type="text" v-model="editData.lastname" /></label><br />
        <label>Nickname: <input type="text" v-model="editData.nickname" /></label><br />
        <label>Gender: <input type="text" v-model="editData.gender" /></label><br />
        <label>Age: <input type="number" v-model.number="editData.age" /></label><br />
        <label>Money: <input type="number" v-model.number="editData.money" /></label><br />
        <label>Gold: <input type="number" v-model.number="editData.gold" /></label><br />
        <label>ROL: <input type="number" v-model.number="editData.rol" /></label><br />
        <label>XP: <input type="number" v-model.number="editData.xp" /></label><br />
        <label>Health Outer: <input type="number" v-model.number="editData.healthouter" /></label><br />
        <label>Health Inner: <input type="number" v-model.number="editData.healthinner" /></label><br />
        <label>Stamina Outer: <input type="number" v-model.number="editData.staminaouter" /></label><br />
        <label>Stamina Inner: <input type="number" v-model.number="editData.staminainner" /></label><br />
        <label>Hours: <input type="number" v-model.number="editData.hours" /></label><br />
        <label>Slots: <input type="number" v-model.number="editData.slots" /></label><br />
        <label>Job: <input type="text" v-model="editData.job" /></label><br />
        <label>Job Label: <input type="text" v-model="editData.joblabel" /></label><br />
        <label>Job Grade: <input type="number" v-model.number="editData.jobgrade" /></label><br />
        <label>Is Dead: <input type="checkbox" v-model="editData.isdead" /></label><br />
        <label>Trust: <input type="number" v-model.number="editData.trust" /></label><br />
        <label>Walk: <input type="text" v-model="editData.walk" /></label><br />
        <label>Gunsmith: <input type="number" v-model.number="editData.gunsmith" /></label><br />
        <label>Discord ID: <input type="text" v-model="editData.discordid" /></label><br />
        <label>Ranch ID: <input type="number" v-model.number="editData.ranchid" /></label><br />
        <label>LastLogin: <input type="date" v-model="editData.LastLogin" /></label><br />
        <label>Character desc: 
          <textarea v-model="editData.character_desc" rows="2"></textarea>
        </label><br />

        <!-- 2) JSON: Status, Meta, Inventory, Info, Ammo, LastJoined, Crafting, etc. -->
        <h3>JSON Fields</h3>
        <fieldset>
          <legend>Status</legend>
          <div v-for="(val, key) in editData.status" :key="key">
            <label>{{ key }}:
              <input
                v-model="editData.status[key]"
                :type="typeof val === 'number' ? 'number' : 'text'"
              />
            </label>
          </div>
        </fieldset>

        <fieldset>
          <legend>Meta</legend>
          <div v-for="(val, key) in editData.meta" :key="key">
            <label>{{ key }}:
              <input
                v-model="editData.meta[key]"
                :type="typeof val === 'number' ? 'number' : 'text'"
              />
            </label>
          </div>
        </fieldset>

        <fieldset>
          <legend>Inventory</legend>
          <div v-for="(val, key) in editData.inventory" :key="key">
            <label>{{ key }}:
              <input
                v-model="editData.inventory[key]"
                :type="typeof val === 'number' ? 'number' : 'text'"
              />
            </label>
          </div>
        </fieldset>

        <fieldset>
          <legend>Info</legend>
          <div v-for="(val, key) in editData.info" :key="key">
            <label>{{ key }}:
              <input
                v-model="editData.info[key]"
                :type="typeof val === 'number' ? 'number' : 'text'"
              />
            </label>
          </div>
        </fieldset>

        <fieldset>
          <legend>Ammo</legend>
          <div v-for="(val, key) in editData.ammo" :key="key">
            <label>{{ key }}:
              <input
                v-model="editData.ammo[key]"
                :type="typeof val === 'number' ? 'number' : 'text'"
              />
            </label>
          </div>
        </fieldset>

        <fieldset>
          <legend>Last Joined (Array)</legend>
          <!-- lastjoined je v DB definované jako Text, uvnitř je to ale "[]" -> array -->
          <div v-for="(val, idx) in editData.lastjoined" :key="idx">
            <label>Index {{ idx }}:
              <input
                v-model="editData.lastjoined[idx]"
                :type="typeof val === 'number' ? 'number' : 'text'"
              />
            </label>
          </div>
          <button @click="addLastJoined">+ Add item</button>
        </fieldset>

        <fieldset>
          <legend>Crafting</legend>
          <div v-for="(val, key) in editData.crafting" :key="key">
            <label>{{ key }}:
              <input
                v-model="editData.crafting[key]"
                :type="typeof val === 'number' ? 'number' : 'text'"
              />
            </label>
          </div>
        </fieldset>

        <!-- 3) JSON: SkinPlayer, CompPlayer, CompTints, Coords -->
        <h3>Skin Player</h3>
        <div v-for="(val, key) in editData.skinPlayer" :key="key" class="json-field">
          <label>{{ key }}:
            <input
              v-model="editData.skinPlayer[key]"
              :type="typeof val === 'number' ? 'number' : 'text'"
            />
          </label>
        </div>

        <h3>Comp Player</h3>
        <div v-for="(val, key) in editData.compPlayer" :key="key" class="json-field">
          <label>{{ key }}:
            <input
              v-model="editData.compPlayer[key]"
              :type="typeof val === 'number' ? 'number' : 'text'"
            />
          </label>
        </div>

        <h3>Comp Tints</h3>
        <div v-for="(val, key) in editData.compTints" :key="key" class="json-field">
          <label>{{ key }}:
            <input
              v-model="editData.compTints[key]"
              :type="typeof val === 'number' ? 'number' : 'text'"
            />
          </label>
        </div>

        <h3>Coords</h3>
        <div v-for="(val, key) in editData.coords" :key="key" class="json-field">
          <label>{{ key }}:
            <input
              v-model="editData.coords[key]"
              :type="typeof val === 'number' ? 'number' : 'text'"
            />
          </label>
        </div>

        <!-- Tlačítka uložit / zavřít -->
        <div style="margin-top: 1rem;">
          <button @click="saveChanges">Uložit</button>
          <button @click="closeModal">Zavřít</button>
        </div>
      </div>
    </div>

    <!-- MODAL PRO MOVE -->
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

      // Edit modal
      showEditModal: false,
      editData: {},

      // Move
      moveTarget: null,
    };
  },
  methods: {
    // Odhlášení
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    },

    // Načtení seznamu postav
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
        // Jednoduchý odhad totalPages – v ideálním případě by backend posílal i "count"
        this.totalPages = this.characters.length < this.perPage
          ? this.currentPage
          : this.currentPage + 1;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$router.push('/login');
        }
        console.error('Error fetching characters:', error);
      }
    },

    // Otevření modálu a naplnění editData
    editCharacter(character) {
      // Naparsujeme JSON pole
      const parseOrEmptyObj = (val) => {
        try {
          return val ? JSON.parse(val) : {};
        } catch {
          return {};
        }
      };
      const parseOrEmptyArr = (val) => {
        try {
          return val ? JSON.parse(val) : [];
        } catch {
          return [];
        }
      };

      // Vyplníme "editData" včetně všech povinných polí z CharacterModel
      this.editData = {
        charidentifier: character.charidentifier,
        identifier: character.identifier,
        steamname: character.steamname,
        group: character.group,
        money: character.money,
        gold: character.gold,
        rol: character.rol,
        xp: character.xp,
        healthouter: character.healthouter,
        healthinner: character.healthinner,
        staminaouter: character.staminaouter,
        staminainner: character.staminainner,
        hours: character.hours,
        LastLogin: character.LastLogin || null,  // v Pydantic je Optional
        inventory: parseOrEmptyObj(character.inventory),
        slots: character.slots,
        job: character.job,
        joblabel: character.joblabel,
        status: parseOrEmptyObj(character.status),
        meta: parseOrEmptyObj(character.meta),
        firstname: character.firstname,
        lastname: character.lastname,
        character_desc: character.character_desc,
        gender: character.gender,
        age: character.age,
        nickname: character.nickname,
        skinPlayer: parseOrEmptyObj(character.skinPlayer),
        compPlayer: parseOrEmptyObj(character.compPlayer),
        compTints: parseOrEmptyObj(character.compTints),
        jobgrade: character.jobgrade,
        coords: parseOrEmptyObj(character.coords),
        isdead: character.isdead,
        trust: character.trust,
        walk: character.walk,
        crafting: parseOrEmptyObj(character.crafting),
        info: parseOrEmptyObj(character.info),
        gunsmith: character.gunsmith,
        ammo: parseOrEmptyObj(character.ammo),
        discordid: character.discordid,
        lastjoined: parseOrEmptyArr(character.lastjoined),
        ranchid: character.ranchid,
      };

      this.showEditModal = true;
    },

    // Přidat prvek do lastjoined (které je pole)
    addLastJoined() {
      if (!this.editData.lastjoined) {
        this.editData.lastjoined = [];
      }
      this.editData.lastjoined.push("");
    },

    // Zavřít modál
    closeModal() {
      this.showEditModal = false;
      this.editData = {};
    },

    // Uložit změny (PUT)
    async saveChanges() {
      // Před odesláním musíme zase JSON.stringify JSON polím
      const updatedCharacter = {
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
        // musíme z objektů/ polí udělat string:
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
        // lastjoined je pole, tak ho zas stringneme
        lastjoined: JSON.stringify(this.editData.lastjoined),
        ranchid: this.editData.ranchid,
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
        if (error.response && error.response.status === 401) {
          this.$router.push('/login');
        }
        console.error('Error updating character:', error);
      }
    },

    // Smazání postavy
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

    // Kopírování postavy
    async copyCharacter(charidentifier) {
      const newIdentifier = prompt('Enter new identifier for the copied character');
      if (!newIdentifier) return;
      const token = localStorage.getItem('token');
      try {
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

    // Move
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

    // Stránkování
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
  },
  mounted() {
    this.fetchCharacters();
  },
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
  max-height: 90%;
  overflow-y: auto;
  width: 600px;
}
.json-field {
  margin-left: 1rem;
}
fieldset {
  margin: 1rem 0;
  border: 1px solid #999;
  padding: 0.5rem;
}
</style>
