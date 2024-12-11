/*
 https://www.electronicwings.com/
  SD Card Interface code for ESP32
  SPI Pins of ESP32 SD card as follows:
  CS    = 5;
  MOSI  = 23;
  MISO  = 19;
  SCK   = 18; 
*/

#include <SPI.h>
#include <SD.h>

File myFile;
const int CS = 5;

void WriteFile(const char * path, const char * data) {
  // Abrir arquivo (apenas um de cada vez)
  myFile = SD.open(path, FILE_APPEND);

  if (myFile) {
    Serial.printf("Escrevendo no arquivo %s\n", path);
    myFile.println(data);
    myFile.close();
    Serial.println("Concluído.");
  }
  else {
    Serial.println("Erro na abertura do arquivo.");
  }
}

void ReadFile(const char * path) {
  // abrir o arquivo para leitura
  myFile = SD.open(path);

  if (myFile) {
    Serial.printf("Leitura do arquivo %s\n", path);

    // realizar a leitura do arquivo até que não tenha mais nada para ser lido
    while (myFile.available()){
      Serial.write(myFile.read());
    }

    // fechar o arquivo
    myFile.close();
  }
  else {
    // caso o arquivo não abra corretamente
    Serial.printf("Erro ao abrir o arquivo %s\n", path);
  }
}

void setup() {
  Serial.begin(9600);
  delay(1500);
  while (!Serial) {;}
  
  Serial.println("Inicializando SD Card");
  if (!SD.begin(CS)) {
    Serial.println("Falha na Inicialização");
    return;
  }
  Serial.println("Inicialização concluída.");

  WriteFile("/test.txt", "Novo");
  WriteFile("/test.txt", "Teste");
  WriteFile("/test.txt", "SD Card");
  ReadFile("/test.txt");
}

void loop() {
  // put your main code here, to run repeatedly:

}
