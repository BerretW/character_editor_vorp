<template>
  <div>
    <SearchBar v-model="searchTerm" @search="fetchCharacters" />

    <div v-if="characters.length > 0">
      <CharacterCard
        v-for="character in characters"
        :key="character.charidentifier"
        :character="character"
        @edit="openEdit"
        @delete="deleteCharacter"
        @copy="copyCharacter"
        @move="openMove"
      />
      <Pagination
        :currentPage="currentPage"
        :totalPages="totalPages"
        @previous="previousPage"
        @next="nextPage"
      />
    </div>
    <div v-else>
      <p>No characters found.</p>
    </div>

    <EditCharacterModal
      :visible="showEditModal"
      :character="editData"
      :skinOptions="currentSkinOptions"
      @save="saveEditedCharacter"
      @close="closeEditModal"
    />

    <MoveCharacterModal
      :visible="showMoveModal"
      @move="submitMove"
      @close="closeMoveModal"
    />

    <button @click="logout">Logout</button>
  </div>
</template>

<script>
import axios from "axios";
import SearchBar from "./components/SearchBar.vue";
import CharacterCard from "./components/CharacterCard.vue";
import Pagination from "./components/Pagination.vue";
import EditCharacterModal from "./components/EditCharacterModal.vue";
import MoveCharacterModal from "./components/MoveCharacterModal.vue";
import { Config } from "./components/config.js";

export default {
  name: "CharacterList",
  components: {
    SearchBar,
    CharacterCard,
    Pagination,
    EditCharacterModal,
    MoveCharacterModal,
  },
  data() {
    return {
      characters: [],
      currentPage: 1,
      totalPages: 1,
      perPage: 10,
      searchTerm: "",
      apiUrl: "http://localhost:5000",

      showEditModal: false,
      editData: {},
      showMoveModal: false,
      moveCharId: null,

      // Skin options
      skinOptions: Config.DefaultChar.Male,
      currentSkinOptions: Config.DefaultChar.Male[0],
    };
  },
  methods: {
    async fetchCharacters() {
    const token = localStorage.getItem("token");
    try {
    const response = await axios.get(`${this.apiUrl}/characters`, {
        headers: { Authorization: `Bearer ${token}` },
        params: {
        page: this.currentPage,
        per_page: this.perPage,
        search: this.searchTerm,
        },
    });
    
    // Parsování skinPlayer při načítání dat
    this.characters = response.data.map(char => {
        if (typeof char.skinPlayer === 'string') {
            try {
                char.skinPlayer = JSON.parse(char.skinPlayer);
            } catch (e) {
                console.warn("Nepodařilo se parse-nout skinPlayer:", e);
                char.skinPlayer = {};
            }
        }
        if (!char.skinPlayer) {
            char.skinPlayer = {};
        }

        return char;
    });


    this.totalPages =
        this.characters.length < this.perPage
        ? this.currentPage
        : this.currentPage + 1;
    } catch (error) {
    if (error.response && error.response.status === 401) {
        this.$router.push("/login");
    }
    console.error("Error fetching characters:", error);
    }
},
    openEdit(character) {
      console.log("Otevírám modal pro postavu:", character);
      // Uděláme kopii postavy
      this.editData = JSON.parse(JSON.stringify(character));
      // Nastavíme skin options podle genderu
      this.currentSkinOptions =
        (this.editData.gender === "Male" || this.editData.gender === " ")
          ? Config.DefaultChar.Male[this.editData.skinType || 0]
          : Config.DefaultChar.Female[this.editData.skinType || 0];
      // Nastavení skinPlayer.sex
      this.editData.skinPlayer = this.editData.skinPlayer || {};
      this.editData.skinPlayer.sex =
        (this.editData.gender === "Male" || this.editData.gender === " ")
          ? "mp_male"
          : "mp_female";
      this.showEditModal = true;
    },
    saveEditedCharacter(updatedCharacter) {
  const token = localStorage.getItem("token");
  const payload = {
    ...updatedCharacter,
    inventory: JSON.stringify(updatedCharacter.inventory),
    status: JSON.stringify(updatedCharacter.status),
    meta: JSON.stringify(updatedCharacter.meta),
    info: JSON.stringify(updatedCharacter.info),
    ammo: JSON.stringify(updatedCharacter.ammo),
    lastjoined: JSON.stringify(updatedCharacter.lastjoined),
    crafting: JSON.stringify(updatedCharacter.crafting),
    skinPlayer: JSON.stringify(updatedCharacter.skinPlayer),
    compPlayer: JSON.stringify(updatedCharacter.compPlayer),
    compTints: JSON.stringify(updatedCharacter.compTints),
    coords: JSON.stringify(updatedCharacter.coords),
  };
  axios
    .put(`${this.apiUrl}/characters/${payload.charidentifier}`, payload, {
      headers: { Authorization: `Bearer ${token}` },
    })
    .then(() => {
      this.showEditModal = false;
      this.fetchCharacters();
    })
    .catch((error) => {
      if (error.response && error.response.status === 401) {
        this.$router.push("/login");
      }
      console.error("Error updating character:", error);
    });
},
    closeEditModal() {
      this.showEditModal = false;
    },
    deleteCharacter(charidentifier) {
      const token = localStorage.getItem("token");
      if (confirm("Are you sure you want to delete this character?")) {
        axios
          .delete(`${this.apiUrl}/characters/${charidentifier}`, {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then(() => this.fetchCharacters())
          .catch((error) => {
            if (error.response && error.response.status === 401) {
              this.$router.push("/login");
            }
            console.error("Error deleting character:", error);
          });
      }
    },
    copyCharacter(charidentifier) {
      const newIdentifier = prompt("Enter new identifier for the copied character");
      if (!newIdentifier) return;
      const token = localStorage.getItem("token");
      axios
        .post(
          `${this.apiUrl}/characters/${charidentifier}/copy`,
          { new_identifier: newIdentifier },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        .then(() => this.fetchCharacters())
        .catch((error) => {
          if (error.response && error.response.status === 401) {
            this.$router.push("/login");
          }
          console.error("Error copying character:", error);
        });
    },
    openMove(charId) {
      this.moveCharId = charId;
      this.showMoveModal = true;
    },
    submitMove(newIdentifier) {
      const token = localStorage.getItem("token");
      axios
        .post(
          `${this.apiUrl}/characters/${this.moveCharId}/move`,
          { new_identifier: newIdentifier },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        .then(() => {
          this.showMoveModal = false;
          this.fetchCharacters();
        })
        .catch((error) => {
          if (error.response && error.response.status === 401) {
            this.$router.push("/login");
          }
          console.error("Error moving character:", error);
        });
    },
    closeMoveModal() {
      this.showMoveModal = false;
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
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
  },
  mounted() {
    this.fetchCharacters();
  },
};
</script>

<style scoped>
/* Styly pro hlavní komponentu mohou zůstat sem */
</style>
