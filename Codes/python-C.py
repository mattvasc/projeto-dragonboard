import time
import subprocess
from subprocess import Popen, PIPE

# compila o arquivo que capta os dados em C
subprocess.call("gcc rand.c -o rand", shell=True)
while(True):
	time.sleep(3)
	# recebe todos os stdout do seu arquivo .c, aqui utilizamos rand.c
	out = Popen(["./rand"], stdout=PIPE)
	# le stdout do mesmo formato em que foi printado
	t = out.stdout.read()
	saida = str(t.decode()).split('\n')
	# exemplo do que podemos fazer com os dados
	print("A temperatura é de "+str(saida[0]))
	print("O slider tem valor de "+str(saida[1]))
