# swp

## Vorraussetzungen

- Docker und Docker Compose
- freie Ports 3000 und 8000

## Starten

`docker-compose up`

## Testdaten importieren

`docker exec -i swp-db-1 -uroot -proot finanzen < datenbank/testdaten.sql`

### PIP im Schulnetzwerk

```
$env:HTTPS_PROXY="http://10.16.1.1:8080"
python -m pip install -r  requirements.txt
```
