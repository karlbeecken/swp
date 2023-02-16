import mysql.connector


datenbank = mysql.connector.connect (
    host="localhost",
    user="root",
    password="root",
    database="finanzen",
)


def alleAusgaben(kategorie=None):
    cursor = datenbank.cursor()
    if kategorie == all or kategorie is None:
        cursor.execute("SELECT * FROM ausgaben")
    else:
        cursor.execute("SELECT * FROM ausgaben WHERE kategorie = %s", [kategorie])
    ergebnis=cursor.fetchall()
    return ergebnis


def neueAusgabe(grund, wert, datum, kategorie):
    cursor = datenbank.cursor()
    cursor.execute("INSERT INTO ausgaben (grund, wert, datum, kategorie) values (%s, %s, %s, %s)", (grund, wert, datum, kategorie))
    datenbank.commit()

def loescheAusgabe(id):
    cursor = datenbank.cursor()
    cursor.execute("DELETE FROM ausgaben WHERE id = %s", [id])
    datenbank.commit()

def bearbeiteAusgabe(grund, wert, datum, kategorie):
    cursor = datenbank.cursor()
    cursor.execute("UPDATE ausgaben SET grund = '%s', wert = %s, datum = '%s', kategorie = %s WHERE id = %s", [grund, wert, datum, kategorie, id])
    datenbank.commit()


def gesamtwertKategorie(kategorie):
    cursor = datenbank.cursor()
    cursor.execute("SELECT wert FROM ausgaben WHERE kategorie = %s", [kategorie])
    ergebnis=cursor.fetchall()
    summe = 0
    for eintrag in ergebnis:
        summe += eintrag[0]
        
    return summe


 # print(datenbank)
print(alleAusgaben(1))
# neueAusgabe("smoothie", 3.0, "2023-02-12", 1)
# print(alleAusgaben())
# print(gesamtwertKategorie(1))


