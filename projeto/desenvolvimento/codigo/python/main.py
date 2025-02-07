""" Use esse arquivo apenas para chamar o arquivo princiapal para cada ESP """

# from main_sala import main
from main_via import main

ESP_ADDR = {'sensor': 0x01, 'controle': 0x02, 'sala': 0x03}

main(addr = ESP_ADDR['via'])