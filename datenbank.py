from asyncio import sleep
import mysql.connector
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

datenbank = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="finanzen",
)


#bei Spezifizierung Parameter: Ausgabe aller Inhalte der Tabelle "ausgaben" mit dieser Kategorie als Attribut 
#bei keiner Spezifizierung: Ausgabe aller Inhalte der Tabelle "ausgaben" 
def alleAusgaben(kategorie=None):
    cursor = datenbank.cursor()
    if kategorie == all or kategorie is None:
        cursor.execute(
            "SELECT * FROM ausgaben")
    else:
        cursor.execute(
            "SELECT * FROM ausgaben WHERE kategorie = %s", [kategorie])
    columns = cursor.description

    ergebnis = [{columns[index][0]:column for index,
                 column in enumerate(value)} for value in cursor.fetchall()]
    return ergebnis


#erstellt neuen Eintrag in der Tabelle "ausgaben" mit den angegebenen Parametern als Werte
def neueAusgabe(grund, wert, datum, kategorie):                                                                  
    cursor = datenbank.cursor()
    cursor.execute("INSERT INTO ausgaben (grund, wert, datum, kategorie) values (%s, %s, %s, %s)",
                   (grund, wert, datum, kategorie))
    datenbank.commit()


#löscht Eintrag in der Tabelle "ausgaben", der den angegebenen Parameter als id trägt
def loescheAusgabe(id):
    cursor = datenbank.cursor()
    cursor.execute("DELETE FROM ausgaben WHERE id = %s", [id])
    datenbank.commit()


#ändert die Werte eines Eintrags mit einer bestimmten id in der Tabelle "ausgaben" zu den in den Parametern angegebenen anderen Werten
def bearbeiteAusgabe(grund, wert, datum, kategorie, id):
    cursor = datenbank.cursor()
    cursor.execute("UPDATE ausgaben SET grund = %s, wert = %s, datum = %s, kategorie = %s WHERE id = %s", [
                   grund, wert, datum, kategorie, id])
    datenbank.commit()


#gibt die Summe von "wert" aller Einträge mit der als Parameter angegebenen Kategorie aus
def gesamtwertKategorie(kategorie):
    cursor = datenbank.cursor()
    cursor.execute(
        "SELECT wert FROM ausgaben WHERE kategorie = %s", [kategorie])
    ergebnis = cursor.fetchall()
    summe = 0
    for eintrag in ergebnis:
        summe += eintrag[0]
    return summe


#Ausgabe aller Inhalte der Tabelle "kategorie"
def alleKategorien():
    cursor = datenbank.cursor()
    cursor.execute("SELECT * FROM kategorie")
    columns = cursor.description

    ergebnis = [{columns[index][0]:column for index,
                 column in enumerate(value)} for value in cursor.fetchall()]
    return ergebnis


#erstellt neuen Eintrag in der Tabelle "kategorie" mit den angegebenen Parametern als Werte
def neueKategorie(name, farbe, maximal):
    cursor = datenbank.cursor()
    cursor.execute("INSERT INTO kategorie (name, farbe, maximal) values (%s, %s, %s)",
                   (name, farbe, maximal))
    datenbank.commit()


#löscht Eintrag in der Tabelle "kategorie", der den angegebenen Parameter als id trägt
def loescheKategorie(id):
    cursor = datenbank.cursor()
    cursor.execute("DELETE FROM kategorie WHERE id = %s", [id])
    datenbank.commit()


#ändert die Werte eines Eintrags mit einer bestimmten id in der Tabelle "kategorie" zu den in den Parametern angegebenen anderen Werten
def bearbeiteKategorie(name, farbe, maximal, id):
    cursor = datenbank.cursor()
    cursor.execute("UPDATE kategorie SET name = %s, farbe = %s, maximal = %s WHERE id = %s", [
                   name, farbe, maximal, id])
    datenbank.commit()


class Kategorie(BaseModel):
    id: int | None = None
    name: str
    farbe: str
    maximal: float


class Ausgabe(BaseModel):
    id: int | None = None
    grund: str
    wert: float
    datum: str
    kategorie: int


@ app.get("/")
def index():
    return {"message": "Hallo Welt"}


@ app.get("/ausgaben")
def ausgaben():
    # return als json mit key value pairs
    return alleAusgaben()


@ app.get("/ausgaben/{kategorie}")
def ausgaben(kategorie):

    return alleAusgaben(kategorie)


@ app.post("/ausgaben")
def ausgaben(ausgabe: Ausgabe):
    neueAusgabe(ausgabe.grund, ausgabe.wert,
                ausgabe.datum, ausgabe.kategorie)
    return {"message": "Ausgabe wurde hinzugefügt", "ausgabe": ausgabe}


@ app.delete("/ausgaben/{id}")
def ausgaben(id: int):
    loescheAusgabe(id)
    return {"message": "Ausgabe wurde gelöscht", "id": id}


@ app.put("/ausgaben/{id}")
def ausgaben(ausgabe: Ausgabe, id: int):
    bearbeiteAusgabe(ausgabe.grund, ausgabe.wert,
                     ausgabe.datum, ausgabe.kategorie, id)
    return {"message": "Ausgabe wurde bearbeitet", "ausgabe": ausgabe}


@app.get("/ausgaben/kategorie/{kategorie}")
def ausgaben(kategorie):
    return {"gesamtwert": gesamtwertKategorie(kategorie)}


@app.get("/kategorien")
def kategorien():
    return alleKategorien()
