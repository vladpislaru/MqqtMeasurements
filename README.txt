Pentru realizarea stack ului ne folosim de fisierul docker-compose.yaml unde am definit urmatoarele sevicii:
-   Un serviciu de tip mosquitto drep broker mqtt pentru care avem si un mic fisier pt 2 variabile de mediu "./broker/mosquitto.conf"
-   Un python server care sa preia datele datele venite de la broker si sa le introduca in InfluxDB, iar pentru acest serviciu am definit si un Dockerfile pentru a
copia fisierul sura adapter.py in containerul seviciului si pentru a instala modulele necesare 
-   Un serviciu de tip grafana pentru care am definit un volum care sa pastreze configuratia datasources si a dashboard-urilor 
-   Un serviciu de tip influsb db pentru care am definit un volum pt consistenta datelor stocate
S-a realizat si separarea serviciilor in retele diferite(numele acestora fiind sugestive pentru scopul lor)

ATENTIE ! : Chiar daca serviciul de  adapter nu da fail initial datorita conexiunii cu broker ul / influxdb 
Docker Swarn va incerca sa-l relanseze 