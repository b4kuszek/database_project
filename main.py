#! /bin/python3

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="kacper",
    password="FD$kWDu^Bm7z9y",
    database="twitch.tv"
)

mcr = mydb.cursor()

# Struktura tabeli dla tabeli `english monthly perform`
# mcr.execute("CREATE TABLE `english monthly perform` (`id` int(11) NOT NULL, `active_days` int(11) NOT NULL, `hours_streames` int(11) NOT NULL, `hours_watched` int(11) NOT NULL, `name` text COLLATE utf8_polish_ci NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;")

mcr.execute(
    "INSERT INTO `english monthly perform` (`id`, `active_days`, `hours_streames`, `hours_watched`, `name`) VALUES(1, 29, 268, 19568606, 'xqcow'),(2, 23, 286, 5430523, 'trainwreckstv'),(3, 24, 148, 3353982, 'lirik'),(4, 27, 229, 5631926, 'loltyler1'),(5, 22, 124, 3011442, 'sodapoppin'),(6, 26, 199, 4430406, 'shroud'),(7, 19, 72, 1521696, 'pokimane'),(8, 28, 219, 3378964, 'fextralife'),(9, 30, 255, 3195519, 'summit1g'), (10, 29, 162, 1817253, 'forsen');")
# mcr.execute("DROP TABLE `english monthly perform`")
# mcr.execute("ALTER TABLE `english monthly perform` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;")
mcr.execute("UPDATE `english monthly perform` SET `active_days` = '2' WHERE id = '1'")

mcr.execute("SELECT * FROM `english monthly perform`")

for i in mcr:
    print(f'{i}')
