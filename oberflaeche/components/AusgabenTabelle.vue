<template>
  <div class="columns">
    <div class="column is-four-fifths">
      <b-table
        :data="data"
        :selected.sync="selected"
        focusable
        hoverable
        striped
        default-sort="datum"
        default-sort-direction="desc"
      >
        <b-table-column
          field="datum"
          label="Datum"
          width="150"
          sortable
          v-slot="props"
        >
          <b-tag type="is-light"> {{ props.row.datum }}</b-tag>
        </b-table-column>

        <b-table-column
          field="grund"
          label="Grund der Ausgabe"
          sortable
          v-slot="props"
        >
          {{ props.row.grund }}
        </b-table-column>

        <b-table-column
          field="kategorie"
          label="Kategorie"
          centered
          sortable
          width="100"
          v-slot="props"
        >
          <b-tag
            style="width: 100%"
            v-if="props.row.kategorie !== 'Bitte wählen'"
            :type="
              kategorien.filter((k) => k.id === props.row.kategorie)[0].farbe ||
              'is-light'
            "
            >{{
              kategorien.filter((k) => k.id === props.row.kategorie)[0].name ||
              "Unbekannt"
            }}</b-tag
          >
        </b-table-column>

        <b-table-column
          sortable
          field="wert"
          label="Summe der Ausgabe"
          align-right
          numeric
          v-slot="props"
        >
          {{ props.row.wert.toFixed(2) }}&#8239;€
        </b-table-column>
      </b-table>
    </div>
    <div class="column">
      <div style="height: 2.5em" />
      <b-button type="is-primary" @click="istNeuDialogAktiv = true" expanded
        >Neu</b-button
      >
      <div style="height: 20px" />
      <b-button
        type="is-primary is-light"
        @click="vorbereiteBearbeiteAusgabe"
        :disabled="!selected"
        expanded
        >Bearbeiten</b-button
      >
      <div style="height: 20px" />
      <b-button type="is-danger" @click="confirmCustomDelete" expanded
        >Löschen</b-button
      >
    </div>

    <b-modal
      v-model="istNeuDialogAktiv"
      class="cool-modal"
      :on-cancel="zuruecksetzen"
    >
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">Ausgabe</p>
        </header>
        <section class="modal-card-body">
          <b-field label="Wert">
            <b-input
              type="number"
              step="0.01"
              v-model="wert"
              placeholder="Summe der Ausgabe"
              required
            >
            </b-input>
          </b-field>

          <b-field label="Datum">
            <b-datepicker
              v-model="datum"
              locale="de-DE"
              placeholder="Klicken zum Auswählen..."
              icon="calendar-today"
              :icon-right="selected ? 'close-circle' : ''"
              icon-right-clickable
              @icon-right-click="datum = null"
              trap-focus
            >
            </b-datepicker>
          </b-field>

          <b-field label="Kategorie">
            <b-dropdown
              v-model="kategorie"
              :triggers="['hover']"
              aria-role="list"
            >
              <template #trigger>
                <b-button
                  :label="kategorie.name || 'Bitte wählen'"
                  :type="kategorie.farbe || 'is-light'"
                  icon-right="menu-down"
                />
              </template>

              <b-dropdown-item
                v-for="kategorie in kategorien"
                :key="kategorie.id"
                :value="kategorie"
                ><b-tag
                  :type="kategorie.farbe || 'is-light'"
                  style="width: 100%"
                  >{{ kategorie.name }}</b-tag
                ></b-dropdown-item
              >
            </b-dropdown>
          </b-field>

          <b-field label="Grund">
            <b-input
              type="text"
              v-model="grund"
              placeholder="Grund der Ausgabe"
              required
            >
            </b-input>
          </b-field>
        </section>
        <footer class="modal-card-foot">
          <b-button label="Abbrechen" @click="zuruecksetzen" />
          <b-button
            label="Speichern"
            type="is-primary"
            @click="neueAusgabe()"
          />
        </footer>
      </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  methods: {
    confirmCustomDelete() {
      this.$buefy.dialog.confirm({
        title: "Lösche Ausgabe",
        message: "Bist du sicher?",
        confirmText: "Löschen",
        cancelText: "Abbrechen",
        type: "is-danger",
        hasIcon: true,
        onConfirm: () => this.loescheAusgabe(),
      });
    },
    loescheAusgabe() {
      this.$axios
        .delete("/ausgaben/" + this.selected.id)
        .then(async (response) => {
          await this.$axios.get("/ausgaben").then((response) => {
            this.data = response.data;
          });

          this.$buefy.toast.open("Ausgabe gelöscht!");
        })
        .catch((error) => {
          console.log(error);
        });
    },
    neueAusgabe() {
      if (this.bearbeiten) {
        this.bearbeiteAusgabe();
        return;
      }

      let ausgabe = {
        grund: this.grund,
        wert: this.wert,
        datum: this.getDate(this.datum),
        kategorie: this.kategorie.id,
      };

      this.$axios
        .post("/ausgaben", ausgabe)
        .then(async (response) => {
          await this.$axios.get("/ausgaben").then((response) => {
            this.data = response.data;
          });

          this.$buefy.toast.open("Ausgabe gespeichert!");
          this.zuruecksetzen();
          this.istNeuDialogAktiv = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getDate(t) {
      const date = ("0" + t.getDate()).slice(-2);
      const month = ("0" + (t.getMonth() + 1)).slice(-2);
      const year = t.getFullYear();
      return `${year}-${month}-${date}`;
    },
    zuruecksetzen() {
      this.datum = new Date();
      this.wert = 0.0;
      this.grund = "";
      this.kategorie = {};
      this.bearbeiten = false;
      this.istNeuDialogAktiv = false;
    },
    vorbereiteBearbeiteAusgabe() {
      this.bearbeiten = true;

      this.datum = new Date(this.selected.datum);
      this.wert = this.selected.wert;
      this.grund = this.selected.grund;
      this.kategorie = this.kategorien.find(
        (kategorie) => kategorie.id === this.selected.kategorie
      );

      this.istNeuDialogAktiv = true;
    },

    bearbeiteAusgabe() {
      let ausgabe = {
        id: this.selected.id,
        grund: this.grund,
        wert: this.wert,
        datum: this.getDate(this.datum),
        kategorie: this.kategorie.id,
      };

      this.$axios
        .put(`/ausgaben/${ausgabe.id}`, ausgabe)
        .then(async (response) => {
          await this.$axios.get("/ausgaben").then((response) => {
            this.data = response.data;
          });

          this.$buefy.toast.open("Ausgabe bearbeitet!");
          this.zuruecksetzen();
          this.bearbeiten = false;
          this.istNeuDialogAktiv = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  data() {
    return {
      selected: null,
      istNeuDialogAktiv: false,
      bearbeiten: false,
      data: this.ausgabenListe || [],
      datum: new Date(),
      wert: 0.0,
      grund: "",
      kategorie: "Bitte wählen",
      kategorien: [],
      columns: [
        {
          field: "id",
          label: "ID",
          width: "40",
          numeric: true,
        },
        {
          field: "grund",
          label: "Ausgabengrund",
        },
        {
          field: "wert",
          label: "Kosten in €",
        },
        {
          field: "datum",
          label: "Datum",
          centered: true,
        },
        {
          field: "kategorie",
          label: "Kategorie",
        },
      ],
    };
  },
  async fetch() {
    await this.$axios.$get("/kategorien").then((response) => {
      this.kategorien = response;
    });
  },
  name: "AusgabenTabelle",
  props: {
    ausgabenListe: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.modal .animation-content .modal-card {
  overflow: visible !important;
}

.modal-card-body {
  overflow: visible !important;
}

.cool-modal {
  overflow: visible;
}
</style>
