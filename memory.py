# 01/06/2019
#
# @Author Lúcio Reis, Kayalla Pontes, Rodrigo Fabricante
#
# lucio at midiacom dot uff dot br
#
#
# Sistemas Operacionais
#
#
# imports
#
#
class Memory:

	size = 16384
	occupied = 0
	process_list = []

	realTimeQueue = []
	userQueue = []

	feedback1 = []
	feedback2 = []
	feedback3 = []

	primary_memory = []
	swap_memory = []

	def __init__(self, size=size):
		self.size = size
		pass

	def add_process(self, process):
		self.process_list.append(process)
		return