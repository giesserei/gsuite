# gsuite
Giesserei G-Suit tools, scripte

# G-Suit Benutzer export
Der Giesserei Benutzer export orientiert sich an folgendem von Google bereitgestellten Beispiel[1].

## Systemvoraussetzungen

- Giesserei G-Suite Account mit Administrator Berechtigung
- python 3.x + pip

## Vor dem ersten Start

### Application Credentials

Berechtigungsdaten für das Script müssen als json in Pfad
_src/credentials.json_
verfügbar sein. Diese können hier [1] herunter geladen werden:

- API & Dienste
- Applikation "Giesserei User Export" auswählen
- Anmeldedaten
- OAuth 2.0-Client-IDs
- JSON herunterladen
- Die json Datei muss in den _src_ ordner kopiert werden


# Referenzen
[1] https://developers.google.com/admin-sdk/directory/v1/quickstart/python
[2] https://console.cloud.google.com/

