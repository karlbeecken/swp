<template>
  <section class="section">
    <AusgabenTabelle :ausgabenListe="ausgaben" />
  </section>
</template>

<script>
import Card from "~/components/Card";
import AusgabenTabelle from "~/components/AusgabenTabelle";

// fetch data on the server
export default {
  name: "IndexPage",
  components: {
    Card,
    AusgabenTabelle,
  },
  data() {
    return {
      ausgaben: [],
    };
  },
  async fetch() {
    const response = await this.$axios.$get("/ausgaben");
    this.ausgaben = response;
  },
};
</script>
