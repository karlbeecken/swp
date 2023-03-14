<template>
  <div>
    <div class="coolheader">
      <h1 class="title">Budgets</h1>
    </div>
    <BudgetFortschritt />
  </div>
</template>

<script>
import BudgetFortschritt from "~/components/BudgetFortschritt.vue";
export default {
  name: "BudgetPage",
  components: {
    BudgetFortschritt,
  },
};
</script>

<style scoped>
.coolheader {
  margin: 1em 0 2em 0;
}
</style>
