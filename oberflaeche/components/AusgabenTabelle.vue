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
      <b-tooltip label="Neuen Eintrag anlegen">
        <b-button type="is-primary" @click="istNeuDialogAktiv = true" expanded
          >Neu</b-button
        >
      </b-tooltip>

      <div style="height: 20px" />
      <b-tooltip label="Ausgewählte Ausgabe bearbeiten" type="is-light">
        <b-button
          type="is-primary is-light"
          @click="vorbereiteBearbeiteAusgabe"
          :disabled="!selected"
          expanded
          >Bearbeiten</b-button
        >
      </b-tooltip>

      <div style="height: 20px" />
      <b-tooltip label="Ausgewählte Ausgabe löschen">
        <b-button
          type="is-danger"
          @click="confirmCustomDelete"
          :disabled="!selected"
          tooltip="Ausgabe löschen"
          expanded
          >Löschen</b-button
        >
      </b-tooltip>

      <div style="height: 20px" />
      <b-tooltip label="Auswahl in Tabelle zurücksetzen">
        <b-button
          v-if="selected"
          type="is-info is-outlined "
          @click="selected = null"
          expanded
          >Auswahl zurücksetzen</b-button
        >
      </b-tooltip>
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
      // Dialog zum Bestäigen der Löschung einer Ausgabe ("Sind Sie sicher?")
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
      // Anfrage an den Server senden mit ID der markierten Ausgabe
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
      // Wenn Dialog zum Bearbeiten geöffnet ist, dann Ausgabe bearbeiten und sonst nichts tun
      if (this.bearbeiten) {
        this.bearbeiteAusgabe();
        return;
      }

      // Daten aus dem Formular auslesen...
      let ausgabe = {
        grund: this.grund,
        wert: this.wert,
        datum: this.getDate(this.datum),
        kategorie: this.kategorie.id,
      };

      // ...und zum Server senden
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
      // Datum in das Format YYYY-MM-DD umwandeln (für MySQL wichtig)

      const date = ("0" + t.getDate()).slice(-2);
      const month = ("0" + (t.getMonth() + 1)).slice(-2);
      const year = t.getFullYear();
      return `${year}-${month}-${date}`;
    },
    zuruecksetzen() {
      // Alle Formularfelder leeren

      this.datum = new Date();
      this.wert = 0.0;
      this.grund = "";
      this.kategorie = {};
      this.bearbeiten = false;
      this.istNeuDialogAktiv = false;
    },
    vorbereiteBearbeiteAusgabe() {
      // Daten aus der markierten Tabellenzeile auslesen und in die Formularfelder schreiben

      this.bearbeiten = true;

      this.datum = new Date(this.selected.datum);
      this.wert = this.selected.wert;
      this.grund = this.selected.grund;
      this.kategorie = this.kategorien.find(
        (kategorie) => kategorie.id === this.selected.kategorie
      );

      // Dialog öffnen
      this.istNeuDialogAktiv = true;
    },

    bearbeiteAusgabe() {
      // Daten auslesen...
      let ausgabe = {
        id: this.selected.id,
        grund: this.grund,
        wert: this.wert,
        datum: this.getDate(this.datum),
        kategorie: this.kategorie.id,
      };

      // ...und an den Server senden
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
    try {
      // Daten laden bei pageload
      const kategorien = await this.$axios.$get("/kategorien");
      // und speichern im state des components
      this.kategorien = kategorien;

      const ausgaben = await this.$axios.$get("/ausgaben");
      this.data = ausgaben;
    } catch (error) {
      // wenn load vom server kommt, dann funktioniert localhost nicht => nutze direkt die interne docker-adresse
      if (error.code === "ECONNREFUSED") {
        const kategorien = await this.$axios.$get("http://api:8000/kategorien");
        this.kategorien = kategorien;

        const ausgaben = await this.$axios.$get("http://api:8000/ausgaben");
        this.data = ausgaben;
      }
    }
  },
  name: "AusgabenTabelle",
};
</script>

<style scoped>
.modal .animation-content .modal-card {
  overflow: visible !important; /* damit datepicker nicht abgeschnitten wird */
}

.modal-card-body {
  overflow: visible !important; /* -"- */
}

.cool-modal {
  overflow: visible; /* -"- */
}

.b-tooltip {
  margin-bottom: 0.5em;
  width: 100%; /* buttons gehen sonst nicht auf volle breite, expanded wirkt innerhalb tooltip nicht */
}
</style>
