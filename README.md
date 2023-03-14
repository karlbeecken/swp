# Softwareprojekt Informatik-GK 12

## Vorraussetzungen

- Docker und Docker Compose
- freie Ports 3000 und 8000

## Starten

`docker-compose up -d`

Das Frontend ist dann standardmäßig unter Port 3000 erreichbar, das Backend unter Port 8000.
Die Backend-Docs sind unter Port http://localhost:8000/docs erreichbar.

## Logs einsehen

`docker-compose logs -f`

## Testdaten importieren

`docker exec -i swp-db-1 mysql -uroot -proot finanzen < datenbank/testdaten.sql`

_ggf. muss `swp-db-1` durch den mittels `docker-compose ps` ermittelbaren Containernamen des Datenbankcontainers ersetzt werden; dieser ist je nach System und Docker-Version unterschiedlich_

---

### PIP im Schulnetzwerk

```
$env:HTTPS_PROXY="http://10.16.1.1:8080"
python -m pip install -r  requirements.txt
```
