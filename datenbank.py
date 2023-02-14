import mysql.connector

datenbank = mysql.connector.connect (
    host="localhost",
    user="root",
    password="root",
    database="finanzen",
)

print(datenbank)






def alleAusgaben():
    cursor = datenbank.cursor()
    cursor.execute("SELECT * FROM ausgaben")
    ergebnis=cursor.fetchall()
    return ergebnis

print(alleAusgaben())

def neueAusgabe(grund, wert, datum, kategorie):
    cursor = datenbank.cursor()
    cursor.execute("INSERT INTO ausgaben (grund, wert, datum, kategorie) values (%s, %s, %s, %s)", (grund, wert, datum, kategorie))
    datenbank.commit()

neueAusgabe("smoothie", 3.0, "2023-02-12", 1)
print(alleAusgaben())

def gesamtwertKategorie(kategorie):
    cursor = datenbank.cursor()
    cursor.execute("SELECT wert FROM ausgaben WHERE kategorie = %s", [kategorie])
    ergebnis=cursor.fetchall()
    summe = 0
    for eintrag in ergebnis:
        summe += eintrag[0]
        
    return summe

print(gesamtwertKategorie(1))


