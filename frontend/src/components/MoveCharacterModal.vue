<template>
    <div class="modal-backdrop" v-if="visible">
      <div class="modal-content">
        <h2>Move Character</h2>
        <form @submit.prevent="submitMove">
          <label>
            New Identifier:
            <input type="text" v-model="newIdentifier" />
          </label>
          <br />
          <button type="submit">Move</button>
          <button @click="$emit('close')">Close</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "MoveCharacterModal",
    props: {
      visible: Boolean,
    },
    data() {
      return {
        newIdentifier: "",
      };
    },
    methods: {
      submitMove() {
        if (!this.newIdentifier) {
          alert("Identifier cannot be empty");
          return;
        }
        this.$emit("move", this.newIdentifier);
        this.newIdentifier = "";
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
    padding: 1rem 2rem;
    border-radius: 6px;
    max-height: 90%;
    overflow-y: auto;
    width: 400px;
  }
  </style>
  