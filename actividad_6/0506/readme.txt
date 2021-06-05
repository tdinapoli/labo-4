mediciones 3, 4, 5, 6, y 7 son las importantes. Van escalando en sensibilidad y distintos zooms. La mas importante es la 6.
Todas estan medidas con un voltaje de entrada de 1V, para saberlo hicimos:
inst2 = rm.open_resource('USB0::0x0699::0x0346::C034165::INSTR')
inst2.query("VOLT?")