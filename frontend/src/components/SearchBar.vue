<template>
    <div class="search-bar">
      <input
        type="text"
        v-model="searchTerm"
        @input="onSearch"
        placeholder="Search Characters"
      />
      <button @click="onSearch">Search</button>
    </div>
  </template>
  
  <script>
  export default {
    name: "SearchBar",
    props: {
      modelValue: String,
    },
    computed: {
      searchTerm: {
        get() {
          return this.modelValue;
        },
        set(val) {
          this.$emit("update:modelValue", val);
        },
      },
    },
    methods: {
      onSearch() {
        this.$emit("search", this.searchTerm);
      },
    },
  };
  </script>
  
  <style scoped>
  .search-bar {
    margin-bottom: 1rem;
  }
  </style>
  