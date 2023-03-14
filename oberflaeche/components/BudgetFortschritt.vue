<template>
  <div>
    <div>
      <h1 class="subtitle"><strong>Gesamtaufteilung</strong></h1>
      <b-progress
        format="percent"
        :max="100"
        size="is-large"
        class="gesamt-bar"
      >
        <template #bar>
          <b-progress-bar
            v-for="kategorie in kategorien"
            v-bind:key="kategorie.id"
            :value="
              (kategorie.gesamtwert /
                kategorien.reduce(function (a, b) {
                  return a + b['gesamtwert'];
                }, 0)) *
              100
            "
            :type="kategorie.farbe"
            show-value
          >
            {{ kategorie.name }}
          </b-progress-bar>
        </template>
      </b-progress>
    </div>
    <h1 class="subtitle"><strong>Budgetfortschritt je Kategorie</strong></h1>
    <div v-for="kategorie in kategorien" v-bind:key="kategorie.id">
      <div class="budget-bar">
        <strong>{{ kategorie.name }}:</strong>
        {{ Math.round(kategorie.gesamtwert * 100) / 100 }} von
        {{ kategorie.maximal }}&#8239;€

        <b-progress
          :value="(kategorie.gesamtwert / kategorie.maximal) * 100"
          show-value
          format="percent"
          :type="kategorie.farbe"
          size="is-large"
        >
          <span
            :class="{
              zuviel: (kategorie.gesamtwert / kategorie.maximal) * 100 >= 100,
            }"
            >{{
              Math.floor(
                (kategorie.gesamtwert / kategorie.maximal) * 100 * 100
              ) / 100
            }}
            %</span
          >
        </b-progress>
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
.gesamt-bar {
  margin-bottom: 3em;
}
.budget-bar {
  margin-bottom: 2em;
}

.zuviel {
  color: red;
}
</style>
