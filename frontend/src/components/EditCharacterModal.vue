<template>
    <!-- Modal se zobrazí jen, pokud je "visible" true -->
    <div class="modal-backdrop" v-if="visible">
      <div class="modal-content">
        <h2>Upravit postavu (ID: {{ localCharacter.charidentifier }})</h2>
  
        <!-- Základní info (příklad) -->
        <div class="form-group">
          <label for="firstname">First Name:</label>
          <input id="firstname" type="text" v-model="localCharacter.firstname" />
        </div>
  
        <div class="form-group">
          <label for="lastname">Last Name:</label>
          <input id="lastname" type="text" v-model="localCharacter.lastname" />
        </div>
  
        <div class="form-group">
          <label for="nickname">Nickname:</label>
          <input id="nickname" type="text" v-model="localCharacter.nickname" />
        </div>
  
        <div class="form-group">
          <label for="money">Money:</label>
          <input id="money" type="number" v-model.number="localCharacter.money" />
        </div>
  
        <!-- Výběr pohlaví, který nastaví i skinPlayer.sex -->
        <div class="form-group">
          <label for="gender">Gender (Male/Female):</label>
          <select id="gender" v-model="localCharacter.gender" @change="updateSex">
            <option value="Male">Muž</option>
            <option value="Female">Žena</option>
          </select>
        </div>
  
        <!-- Příklad: výběr vzhledu postavy, binding do skinPlayer (které je objekt) -->
        <div class="form-group">
          <label for="headType">Hlava (HeadType):</label>
          <select id="headType" v-model="localCharacter.skinPlayer.HeadType">
            <option
              v-for="(headVal, hIndex) in skinOptions.Heads"
              :key="hIndex"
              :value="headVal"
            >
              {{ headVal }}
            </option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="bodyType">Tělo (BodyType):</label>
          <select id="bodyType" v-model="localCharacter.skinPlayer.BodyType">
            <option
              v-for="(bodyVal, bIndex) in skinOptions.Body"
              :key="bIndex"
              :value="bodyVal"
            >
              {{ bodyVal }}
            </option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="legsType">Nohy (LegsType):</label>
          <select id="legsType" v-model="localCharacter.skinPlayer.LegsType">
            <option
              v-for="(legsVal, lIndex) in skinOptions.Legs"
              :key="lIndex"
              :value="legsVal"
            >
              {{ legsVal }}
            </option>
          </select>
        </div>
  
        <!-- Tlačítka "Uložit" a "Zavřít" -->
        <div class="button-group">
          <button @click="save">Uložit</button>
          <button @click="$emit('close')">Zavřít</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "EditCharacterModal",
    props: {
      visible: {
        type: Boolean,
        default: false,
      },
      character: {
        type: Object,
        required: true,
      },
      // Např. {Heads: [...], Body: [...], Legs: [...]} – definice ras, typů, atd.
      skinOptions: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        // Lokální kopie postavy, abychom neměnili přímo props
        localCharacter: {},
      };
    },
    watch: {
      // Kdykoliv se změní "character" zvenku, načteme nová data
      character: {
        immediate: true,
        handler(newVal) {
          // 1) Převezmeme data a parse-neme skinPlayer, pokud je string
          const newCharCopy = JSON.parse(JSON.stringify(newVal));
          // Bezpečné klonování (ale i tak zkusíme parse-nout skinPlayer)
          if (typeof newCharCopy.skinPlayer === "string") {
            try {
              newCharCopy.skinPlayer = JSON.parse(newCharCopy.skinPlayer);
            } catch (e) {
              console.warn("Nepodařilo se parse-nout skinPlayer:", e);
              newCharCopy.skinPlayer = {};
            }
          }
          // Ujistíme se, že je to objekt
          if (!newCharCopy.skinPlayer) {
            newCharCopy.skinPlayer = {};
          }
          // Pokud sex není definován, nastavíme podle newCharCopy.gender
          if (!newCharCopy.skinPlayer.sex) {
            const g = (newCharCopy.gender || "").trim();
            newCharCopy.skinPlayer.sex = (g === "" || g === "Male") ? "mp_male" : "mp_female";
          }
  
          // Teď můžeme naplnit do localCharacter
          this.localCharacter = newCharCopy;
        },
      },
    },
    methods: {
      updateSex() {
        // Při změně pohlaví aktualizujeme i localCharacter.skinPlayer.sex
        const g = (this.localCharacter.gender || "").trim();
        this.localCharacter.skinPlayer.sex = (g === "" || g === "Male") ? "mp_male" : "mp_female";
      },
      save() {
        // Emitneme lokální data, rodič si s nimi naloží
        this.$emit("save", this.localCharacter);
      },
    },
  };
  </script>
  
  <style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .modal-content {
    background: #fff;
    padding: 1.5rem;
    border-radius: 8px;
    max-height: 90%;
    overflow-y: auto;
    width: 500px;
  }
  .form-group {
    margin-bottom: 1rem;
  }
  .form-group label {
    display: block;
    margin-bottom: 0.25rem;
  }
  .form-group input,
  .form-group select {
    width: 100%;
    padding: 0.5rem;
    box-sizing: border-box;
  }
  .button-group {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
  }
  </style>
  