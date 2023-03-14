<template>
  <section class="section">
    <div class="coolheader">
      <h1 class="title">Ausgaben</h1>
    </div>
    <AusgabenTabelle />
  </section>
</template>

<script>
import AusgabenTabelle from "~/components/AusgabenTabelle";

export default {
  name: "IndexPage",
  components: {
    AusgabenTabelle,
  },
};
</script>
