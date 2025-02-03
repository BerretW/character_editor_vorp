<template>
    <div class="character-card">
      <h2>{{ character.firstname }} {{ character.lastname }}</h2>
      <p>Nickname: {{ character.nickname }}</p>
      <p>Steam Name: {{ character.steamname }}</p>
      <button @click="$emit('edit', character)">Edit</button>
      <button @click="$emit('delete', character.charidentifier)">Delete</button>
      <button @click="$emit('copy', character.charidentifier)">Copy</button>
      <button @click="$emit('move', character.charidentifier)">Move</button>
    </div>
  </template>
  
  <script>
  export default {
    name: "CharacterCard",
    props: {
      character: Object,
    },
  };
  </script>
  
  <style scoped>
  .character-card {
    border: 1px solid #ccc;
    margin: 0.5rem;
    padding: 0.5rem;
  }
  </style>
  