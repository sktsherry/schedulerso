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
from random import randint
class Process:

	process_id = None
	waiting_io = False
	io_quantum = 0


	state = None
	size = 512

	priority = 0
	cpu_bound = True
	arrival_time = 0
	duration_time = 0

	disk = False
	printer = False

	quantum = 0


	def __init__(self, arrival_time=0, priority=0, duration_time=0, cpu_bound=True, user_level=True, process_id=None):
		self.arrival_time = arrival_time
		self.priority = priority
		self.duration_time = duration_time
		self.cpu_bound = cpu_bound
		self.user_level = user_level
		self.process_id = process_id
		
		self.check_io_needing()

		return

	def check_io_needing(self):
		if(self.user_level):
			rand = randint(0,100)
			if rand < 20:
				self.disk = True
			rand = randint(0,100)
			if rand < 20:
				self.printer = True

		return