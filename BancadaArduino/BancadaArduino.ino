// Bibliotecas
#include "HX711.h"
#include <EEPROM.h>

// Pinos para conexao ao HX711
uint8_t pinData  = A4; // Dados
uint8_t pinClock = A5; // Clock

// Objeto responsavel por ler o HX711
HX711 loadcell;

// Fator de conversao do sinal eletrico para forca 
// (salvo na memoria permanente do Arduino - EEPROM)
float conversionFactor;

void setup()
{
  // Inicializa a comunicacao serial 
  Serial.begin(115200);

  // Inicializa o objeto para leitura do HX711
  loadcell.begin(pinData, pinClock);

  // Tara a forca
  loadcell.tare();

  // Le da EEPROM o fator conversao
  EEPROM.get(0,conversionFactor);

  /*
    Se o fator de conversao for muito pequeno, entao
    trata-se do primeiro uso e a memoria estava apagada
    (zeros). Usar o fator 1 para evitar erros ate a 
    calibracao.
  */ 
  if ( fabs(conversionFactor) < 1E-10 )
  {
    conversionFactor = 1.0;

    EEPROM.put(0,conversionFactor);
  }

  // Definindo o fator de calibracao...
  loadcell.set_scale(conversionFactor);
}


void loop()
{
    /*
      Protocolo de comunicacao
      ========================
        Mensagens enviadas
        ------------------
          Toda a mensagem enviada para o computador segue o padrao
            <x,y>
          onde 
            x = codigo identificador da mensagem e 
            y = restante da mensagem.

        Mensagens recebidas
        -------------------
          As mensagens recebidas seguem o padrao
            x,y
          onde
            x = caracter identificador da mensagem e
            y = restante da mensagem
    */

  // Verificando se ha solicitacao de comunicacao com o computador...
  if ( Serial.available() > 0 )
  {
    char cmd = Serial.read();

    // Computador solicitando a alteracao do fator de conversao

    if ( cmd == 's' )
    {
      conversionFactor = Serial.parseFloat();
      loadcell.set_scale(conversionFactor);
      EEPROM.put(0,conversionFactor);
    }

    // Computador solicitando o envio do fator de conversao
    // <2, fatordeconversao>
    if ( cmd == 'g' )
    {
      Serial.print("<");
      Serial.print("2,");
      Serial.print(loadcell.get_scale(),5);
      Serial.println(">");
    }
  }
  // Lendo o instante e a forca atual 
  float  time = millis()*1E-3;
  float force = loadcell.get_units();

  // Enviando o tempo e a forca para o computador
  // <1, tempo, forca>
  Serial.print("<");
  Serial.print("1,");
  Serial.print(time,3);
  Serial.print(",");
  Serial.print(force,4);
  Serial.println(">");
  
}
