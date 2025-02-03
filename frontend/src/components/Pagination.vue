<template>
    <div class="pagination">
      <button :disabled="currentPage === 1" @click="previousPage">
        Previous
      </button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="nextPage">
        Next
      </button>
    </div>
  </template>
  
  <script>
  export default {
    name: "Pagination",
    props: {
      currentPage: Number,
      totalPages: Number,
    },
    methods: {
      previousPage() {
        this.$emit("previous");
      },
      nextPage() {
        this.$emit("next");
      },
    },
  };
  </script>
  
  <style scoped>
  .pagination {
    margin-top: 1rem;
  }
  </style>
  