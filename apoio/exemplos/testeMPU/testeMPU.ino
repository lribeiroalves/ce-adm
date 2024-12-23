//Programa : Teste MPU6050 e LCD 20x4
//Alteracoes e adaptacoes : MakerHero
//
//Baseado no programa original de JohnChi
 
//Carrega a biblioteca Wire
#include<Wire.h>
//Carrega a biblioteca do LCD
//#include <LiquidCrystal.h>
 
// Inicializa o LCD
//LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
 
//Endereco I2C do MPU6050
const int MPU=0x68;  
//Variaveis para armazenar valores dos sensores
short AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;
void setup()
{
  Serial.begin(9600);
  //Inicializa o LCD
  //lcd.begin(20, 4);
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B); 
   
  //Inicializa o MPU-6050
  Wire.write(0); 
  Wire.endTransmission(true);
     
  //Informacoes iniciais do display
  /*
  lcd.setCursor(0,0);
  lcd.print("Acelerometro");
  lcd.setCursor(0,2);
  lcd.print("Giroscopio");
  */
}
void loop()
{
  short iteracao[3] = {0, 0, 0};
  for (int i = 0; i < 10; i++)
  {
  
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  //Solicita os dados do sensor
  Wire.requestFrom(MPU,14,true);  
  //Armazena o valor dos sensores nas variaveis correspondentes
  
  AcX=Wire.read()<<8|Wire.read();  //0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)     
  if (AcX < 0) {AcX = AcX * (- 1);}
  
  AcY=Wire.read()<<8|Wire.read();  //0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  if (AcY < 0) {AcY = AcY * (- 1);}
  
  AcZ=Wire.read()<<8|Wire.read();  //0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  if (AcZ < 0) {AcZ = AcZ * (- 1);}

  Tmp = Wire.read()<<8|Wire.read();
  
  GyX=Wire.read()<<8|Wire.read();  //0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  if (GyX < 0) {GyX = GyX * (- 1);}
  GyX = GyX - 150;
  if (GyX < 0) {GyX = 0;}
  if (GyX > iteracao[0]) {iteracao[0] = GyX;}                  
  
  GyY=Wire.read()<<8|Wire.read();  //0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  if (GyY < 0) {GyY = GyY * (- 1);}
  GyY = GyY - 150;
  if (GyY < 0) {GyY = 0;}
  if (GyY > iteracao[1]) {iteracao[1] = GyY;}

  GyZ=Wire.read()<<8|Wire.read();  //0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
  if (GyZ < 0) {GyZ = GyZ * (- 1);}
  GyZ = GyZ - 150;
  if (GyZ < 0) {GyZ = 0;}
  if (GyZ > iteracao[2]) {iteracao[2] = GyZ;}

  delay(100);
}

  /*Serial.print(AcX);
   Serial.print("      ");
  Serial.print(AcY);
   Serial.print("      ");
  Serial.print(AcZ);
   Serial.print("      ");*/
  Serial.print(iteracao[0]);
   Serial.print("      ");
  Serial.print(iteracao[1]);
   Serial.print("      ");
  Serial.println(iteracao[2]);
  
}