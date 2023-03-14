<template>
  <div>
    <div v-for="kategorie in kategorien" v-bind:key="kategorie.id">
      <div class="budget-bar">
        <h1 class="subtitle">
          <strong>{{ kategorie.name }}:</strong>
          {{ Math.round(kategorie.gesamtwert * 100) / 100 }} von
          {{ kategorie.maximal }}&#8239;€
        </h1>
        <b-progress
          :value="(kategorie.gesamtwert / kategorie.maximal) * 100"
          show-value
          format="percent"
          size="is-large"
        ></b-progress>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BudgetFortschritt",
  data: () => ({
    kategorien: [],
  }),

  async fetch() {
    try {
      const kategorien = await this.$axios.get("/kategorien/gesamtwert");
      this.kategorien = kategorien.data;
    } catch (error) {
      // wenn load vom server kommt, dann funktioniert localhost nicht => nutze direkt die interne docker-adresse
      if (error.code === "ECONNREFUSED") {
        const kategorien = await this.$axios.get(
          "http://api:8000/kategorien/gesamtwert"
        );
        this.kategorien = kategorien.data;
      }
    }
  },
};
</script>

<style scoped>
.budget-bar {
  margin-bottom: 2em;
}
</style>
