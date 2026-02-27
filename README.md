# BTE - Bancada de testes estáticos para motores-foguete 🚀 

A Bancada de Testes Estáticos (BTE) é um projeto _open-source_ de instrumentação de baixo custo para aquisição de curvas de empuxo em testes em solo com motores-foguete. Para mais informações sobre como montar e utilizar o sistema, consulte esta [_playlist_](https://www.youtube.com/watch?v=_8YHjeDHnX8&list=PLclQeqrxJVevlfCTWFB4jwwu5vRZRwuAt).

<img width="768" height="512" alt="imagem de um sensor " src="https://github.com/user-attachments/assets/c937234a-d677-4c6d-82ec-9b3301d7b43b" />

# Hardware
O _hardware_ é composto basicamente por uma célula de carga (sensor de força), um ADC (HX711), que amplifica o sinal analógico do sensor e o converte para um sinal digital, e um microcontrolador para transmissão dos dados para o computador (Arduino Nano). A figura abaixo ilustra a placa principal (abaixo) e a mesma placa com os componentes soldados (acima).

<img width="384" height="256" alt="imagem de um sensor " src="https://github.com/user-attachments/assets/2157d9b1-2bb3-40f0-972a-68935054aa61" />

Lista de componentes
--------------------
- Placa principal;
- Arduino Nano;
- Módulo HX711 (módulo roxo);
- Conector USB tipo B;
- Cabo USB tipo B (para conectar a célula de carga à placa principal);
- Cabo USB tipo A/mini USB (para conectar o Arduino ao computador);
- Caixa de proteção produzida por impressão em 3D ([todo link]);
- 2x Parafuso M3x5mm - cabeça chanfrada;
- Célula de carga;

# Firmware
Após a montagem do _hardware_, é necessário carregar o _firmware_ no Arduino. Este procedimento é realizado apenas uma vez.

Procedimento de carregamento de _firmware_
------------------------------------------
1. Baixe e instale o [Arduino IDE](https://www.arduino.cc/en/software/);
1. Baixe o [scketch](https://github.com/gbertoldo/BancadaTestesEstaticos/tree/master/BancadaArduino) para programar o Arduino;
1. Abra o _scketch_ no Arduino IDE e selecione a placa Arduino Nano;
1. Plugue o cabo USB no Arduino e no computador e faça o upload do _firmware_ via Arduino IDE.

# Interface Gráfica 
A [interface gráfica](https://github.com/gbertoldo/BancadaTestesEstaticos/releases) exibe a força como função do tempo informada pelo Arduino. Além disso, o _software_ permite realizar a calibração da célula de carga e o armazenamento dos dados coletados.

<img width="768" height="512" alt="BTE" src="https://github.com/user-attachments/assets/35be1180-4fc8-4119-b035-2172c4810750" />

# Como contribuir
Caso deseje contribuir com o projeto, por gentileza, entre em contato comigo: gbertoldo@utfpr.edu.br.
