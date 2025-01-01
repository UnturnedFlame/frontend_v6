<template>
  <form @submit.prevent="handleSubmit">
    <label for="name">Name:</label>
    <input type="text" id="name" v-model="formData.name" required />

    <label for="description">Description:</label>
    <textarea id="description" v-model="formData.description"></textarea>

    <button type="submit">Save</button>
  </form>
</template>

<script>   export default {
  props: {
    initialData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      formData: { ...this.initialData },
    };
  },
  methods: {
    handleSubmit() {
      this.$emit('update', this.formData);
    },
  },
};
</script>