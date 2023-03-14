from asyncio import sleep
from os import environ
import mysql.connector
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    environ.get("FRONTEND_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datenbank-Verbindung als pool, um mehrere Abrufe parallel zu ermöglichen
datenbank = mysql.connector.connect(
    pool_name="mypool",
    pool_size=25,
    host=environ.get("DB_HOST"),
    user="root",
    password="root",
    database="finanzen",
)


# bei Spezifizierung Parameter: Ausgabe aller Inhalte der Tabelle "ausgaben" mit dieser Kategorie als Attribut
# bei keiner Spezifizierung: Ausgabe aller Inhalte der Tabelle "ausgaben"
def alle_ausgaben(kategorie=None):
    # für jeden Abruf nutzen wir einen "frischen" Cursor (=Datenbank-Interaktionsobjekt)
    cursor = datenbank.cursor()
    if kategorie == "all" or kategorie is None:
        cursor.execute(
            "SELECT * FROM ausgaben")
    else:
        cursor.execute(
            "SELECT * FROM ausgaben WHERE kategorie = %s", [kategorie])

    # namen der Spalten werden als Schlüssel für die Werte verwendet
    columns = cursor.description
    ergebnis = [{columns[index][0]:column for index,
                 column in enumerate(value)} for value in cursor.fetchall()]
    return ergebnis


# erstellt neuen Eintrag in der Tabelle "ausgaben" mit den angegebenen Parametern als Werte
def neue_ausgabe(grund, wert, datum, kategorie):
    cursor = datenbank.cursor()
    cursor.execute("INSERT INTO ausgaben (grund, wert, datum, kategorie) values (%s, %s, %s, %s)",
                   (grund, wert, datum, kategorie))
    datenbank.commit()


# löscht Eintrag in der Tabelle "ausgaben", der den angegebenen Parameter als id trägt
def loesche_ausgabe(id):
    cursor = datenbank.cursor()
    cursor.execute("DELETE FROM ausgaben WHERE id = %s", [id])
    datenbank.commit()


# ändert die Werte eines Eintrags mit einer bestimmten id in der Tabelle "ausgaben" zu den in den Parametern angegebenen anderen Werten
def bearbeite_ausgabe(grund, wert, datum, kategorie, id):
    cursor = datenbank.cursor()
    cursor.execute("UPDATE ausgaben SET grund = %s, wert = %s, datum = %s, kategorie = %s WHERE id = %s", [
                   grund, wert, datum, kategorie, id])
    datenbank.commit()


# gibt die Summe von "wert" aller Einträge mit der als Parameter angegebenen Kategorie aus
def gesamtwert_kategorie(kategorie):
    cursor = datenbank.cursor()

    cursor.execute(
        "SELECT SUM(wert) FROM ausgaben WHERE kategorie = %s", [kategorie])
    summe = cursor.fetchone()[0]

    return summe


# Ausgabe aller Inhalte der Tabelle "kategorie"
def alle_kategorien():
    cursor = datenbank.cursor()
    cursor.execute("SELECT * FROM kategorie")

    # namen der Spalten werden als Schlüssel für die Werte verwendet
    columns = cursor.description
    ergebnis = [{columns[index][0]:column for index,
                 column in enumerate(value)} for value in cursor.fetchall()]
    return ergebnis

# alle kategorien mit gesamtwert


def alle_kategorien_gesamtwert():
    kategorien = alle_kategorien()
    for kategorie in kategorien:
        kategorie["gesamtwert"] = gesamtwert_kategorie(kategorie["id"])
    return kategorien


# erstellt neuen Eintrag in der Tabelle "kategorie" mit den angegebenen Parametern als Werte
def neue_kategorie(name, farbe, maximal):
    cursor = datenbank.cursor()
    cursor.execute("INSERT INTO kategorie (name, farbe, maximal) values (%s, %s, %s)",
                   (name, farbe, maximal))
    datenbank.commit()


# löscht Eintrag in der Tabelle "kategorie", der den angegebenen Parameter als id trägt
def loesche_kategorie(id):
    cursor = datenbank.cursor()
    cursor.execute("DELETE FROM kategorie WHERE id = %s", [id])
    datenbank.commit()


# ändert die Werte eines Eintrags mit einer bestimmten id in der Tabelle "kategorie" zu den in den Parametern angegebenen anderen Werten
def bearbeite_kategorie(name, farbe, maximal, id):
    cursor = datenbank.cursor()
    cursor.execute("UPDATE kategorie SET name = %s, farbe = %s, maximal = %s WHERE id = %s", [
                   name, farbe, maximal, id])
    datenbank.commit()


# definiert die möglichen Parameter für die API
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
    kategorie: int  # verweis auf id in Tabelle "kategorie"


# API-Routen werden registriert und die entsprechenden Funktionen aufgerufen

@app.get("/")
async def index():
    return {"message": "Hallo Welt"}


@app.get("/ausgaben")
async def get_alle_ausgaben():
    return alle_ausgaben()


@app.get("/ausgaben/{kategorie}")
async def get_alle_ausgaben_kategorie(kategorie):
    return alle_ausgaben(kategorie)


@app.post("/ausgaben")
async def post_neue_ausgabe(ausgabe: Ausgabe):
    neue_ausgabe(ausgabe.grund, ausgabe.wert,
                 ausgabe.datum, ausgabe.kategorie)
    return {"message": "Ausgabe wurde hinzugefügt", "ausgabe": ausgabe}


@app.delete("/ausgaben/{id}")
async def delete_loesche_ausgabe(id: int):
    loesche_ausgabe(id)
    return {"message": "Ausgabe wurde gelöscht", "id": id}


@app.put("/ausgaben/{id}")
async def put_bearbeite_ausgabe(ausgabe: Ausgabe, id: int):
    bearbeite_ausgabe(ausgabe.grund, ausgabe.wert,
                      ausgabe.datum, ausgabe.kategorie, id)
    return {"message": "Ausgabe wurde bearbeitet", "ausgabe": ausgabe}


@app.get("/ausgaben/kategorie/{kategorie}")
async def get_gesamtwert_kategorie(kategorie):
    return {"gesamtwert": gesamtwert_kategorie(kategorie)}


@app.get("/kategorien")
async def get_alle_kategorien():
    return alle_kategorien()


@app.get("/kategorien/gesamtwert")
async def get_alle_kategorien_gesamtwert():
    return alle_kategorien_gesamtwert()
