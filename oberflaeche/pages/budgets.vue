<template>
  <section class="section">
    <div class="coolheader">
      <h1 class="title">Budgets</h1>
    </div>
    <BudgetFortschritt />
  </section>
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

<style>
.coolheader {
  margin: 1em 0 2em 0;
}
</style>
