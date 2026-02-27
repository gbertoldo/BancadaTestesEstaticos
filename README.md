# BTE - Bancada de testes estáticos para motores-foguete 🚀 

A Bancada de Testes Estáticos (BTE) é um projeto _open-source_ de instrumentação de baixo custo para aquisição de força como função do tempo em testes em solo com motores-foguete. 

# Características principais
- Baseado em Arduino, ADC HX711 e célula de carga;
- Interface gráfica para visualização dos dados em tempo real;

# Hardware

Lista completa de componentes
-----------------------------
- [Placa principal](google.com.br);
- Arduino Nano;
- Módulo HX711;
- Conector USB tipo B;
- Cabo USB tipo B (para conectar a célula de carga à placa principal);
- Cabo USB tipo A/mini USB (para conectar o Arduino ao computador);
- Caixa de proteção (impressa em 3D);
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
Baixe a última [versão do executável](https://github.com/gbertoldo/BancadaTestesEstaticos/releases)
# Como contribuir
