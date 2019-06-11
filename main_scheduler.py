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
from tkinter import *
import logging
import process
import memory
import random
import time
from random import randint

# TK INTER FOR GRAPHICAL INTERFACE

class Application:

	system = None
	def __init__(self, master=None, system=system):
		self.system = system

		self.firstContainer = Frame(master)
		self.firstContainer["pady"] = 50
		self.firstContainer.pack()

		self.secondContainer = Frame(master)
		self.secondContainer["pady"] = 20
		self.secondContainer.pack()

		self.thirdContainer = Frame(master)
		self.thirdContainer["pady"] = 50
		self.thirdContainer.pack()

		# Duration Label and Entry
		self.title = Label(self.firstContainer,relief="groove", border=2, text="Process Scheduling Simulator")
		self.title["font"] = ("Arial", "18", "italic")
		self.title.pack()

		###############################  Second Container  #####################################
		lbl1= Label(self.secondContainer,relief="groove", border=2, text="CPU 1")
		lbl1.grid(row=0,column=0, padx= 10, pady=10)

		# Scheduler Label and Options
		lbl2= Label(self.secondContainer,relief="groove", border=2, text="CPU 2")
		lbl2.grid(row=0,column=1,padx= 10, pady=10)

		# Scheduler Label and Options
		lbl2= Label(self.secondContainer,relief="groove", border=2, text="CPU 3")
		lbl2.grid(row=0,column=2,padx= 10, pady=10)
		
		# Scheduler Label and Options
		lbl2= Label(self.secondContainer,relief="groove", border=2, text="CPU 4")
		lbl2.grid(row=0,column=3,padx= 10, pady=10)

		self.list = Listbox(self.thirdContainer, selectmode=EXTENDED)
		self.list.pack(fill=BOTH, expand=1)
		self.current = None
		self.list.insert(END, "teste")

	def fill_list(self):
		for proc in self.system.submission_queue:
			self.list.insert(END, proc.process_id)


# CPU CLASS

class Cpu:

	# CPU ATTRIBUTES
	process = None
	state = "FREE"
	system = None
	name = None
	quantum = 0

	# Init defines the system which each cpu belongs to
	def __init__(self, system=system, name=name):
		self.system = system
		self.name = name
		pass

	# Each step of the simulation doest a lot of things
	# cpu gets a new process if is free, it defines the quantum for the feedback queues etc
	# also starts i/o events for user level processes and so on

	def handle_step(self):
		if self.process == None:
			self.process, feedback = self.system.get_process()
			if(self.process != None):
				print("Process taken by ", self.name)
				if self.process.priority == 0:
					self.quantum = self.process.duration_time
				else:
					if feedback == "feedback1":
						self.quantum = 2
					elif feedback == "feedback2":
						self.quantum = 4
					elif feedback == "feedback3":
						self.quantum = 8

				self.state = "OCCUPIED"
				self.process.state = "RUNNING"
		else:
			self.process.duration_time -= 1
			self.quantum -= 1

			if self.process.duration_time == 0:
				self.process.state = "TERMINATED"
				print("Processo finalizado na ", self.name)
				self.handle_terminated_process(self.process)
				self.system.terminated_processes.append(self.process)
				self.process = None
				self.state = "FREE"
				self.quantum = 0

			elif self.quantum <= 0:
				self.process.state = "READY"
				self.state = "FREE"
				if self.process in self.system.memory.feedback1:
					#print("Processo {} indo para feedback2".format(self.process.process_id))
					self.system.memory.feedback2.append(self.process)
					self.system.memory.feedback1.remove(self.process)
				elif self.process in self.system.memory.feedback2:
					#print("Processo {} indo para feedback3".format(self.process.process_id))
					self.system.memory.feedback3.append(self.process)
					self.system.memory.feedback2.remove(self.process)
				elif self.process in self.system.memory.feedback3:
					#print("Processo {} indo para feedback1".format(self.process.process_id))
					self.system.memory.feedback1.append(self.process)
					self.system.memory.feedback3.remove(self.process)


				self.process = None

			elif self.process.priority > 0:
				io = randint(10,100)
				if io < 10:
					self.process.state = "SUSPENDED"
					self.process.waiting_io = True
					self.process.io_quantum = 3

					self.state = "FREE"
					if self.process in self.system.memory.feedback1:
						#print("Processo {} indo para feedback2".format(self.process.process_id))
						self.system.memory.feedback2.append(self.process)
						self.system.memory.feedback1.remove(self.process)
					elif self.process in self.system.memory.feedback2:
						#print("Processo {} indo para feedback3".format(self.process.process_id))
						self.system.memory.feedback3.append(self.process)
						self.system.memory.feedback2.remove(self.process)
					elif self.process in self.system.memory.feedback3:
						#print("Processo {} indo para feedback1".format(self.process.process_id))
						self.system.memory.feedback1.append(self.process)
						self.system.memory.feedback3.remove(self.process)

				#print("Feedback ON {}".format(self.name))

			else:
				print("CPU RUNNING PROCESS ID {}".format(self.process.process_id))

	# Takes the process from memory when it finishes and removes from queries etc

	def handle_terminated_process(self, process):
		if process.priority == 0:
			print("Processo {} Removido da Memória".format(process.process_id))
			self.system.memory.realTimeQueue.remove(process)
			self.system.memory.occupied -= process.size
		else:
			print("Processo {} Removido da Memória".format(process.process_id))
			self.system.memory.userQueue.remove(process)
			if process in self.system.memory.feedback1:
				self.system.memory.feedback1.remove(process)
			elif process in self.system.memory.feedback2:
				self.system.memory.feedback2.remove(process)
			elif process in self.system.memory.feedback3:
				self.system.memory.feedback3.remove(process)
			self.memory.occupied -= process.size
		return


# SIMULATOR 

class Simulator:

	# SIMULATOR ATTRIBUTES
	cpus = [] 
	disk1 = None
	printer1 = None
	printer2 = None

	memory = None
	process = None

	submission_queue = []
	terminated_processes = []


	duration = 0

	# SIMULATOR CONSTRUCTOR
	def __init__(self, duration):
		self.memory = memory.Memory()
		self.duration = duration
		for i in range(4):
			name = "CPU" + str(i)
			tmp_cpu = Cpu(system=self,name=name)
			self.cpus.append(tmp_cpu)
		pass

	# GENERATES PROCESSES MANUALY
	def generate_manualy(self, number):
		print("\n\nCreating {} Processes\n\n".format(number))
		for i in range(number):
			priority = 0
			arrival_time = int(input("Arrival Time: "))
			duration_time = int(input("Duration Time: "))
			cpu_bound = bool(input("CPU Bound? (true or false): "))
			user_level = bool(input("User Level Process? (true or false): "))
			if user_level:
				priority = int(input("Priority 1 a 3: "))
				tmp_process = process.Process(arrival_time=arrival_time, priority=priority, duration_time=duration_time, user_level=user_level, process_id=i, cpu_bound=cpu_bound)
				self.submission_queue.append(tmp_process)
			else:
				tmp_process = process.Process(arrival_time=arrival_time, priority=priority, duration_time=duration_time, user_level=user_level, process_id=i, cpu_bound=cpu_bound)
				self.submission_queue.append(tmp_process)
		#self.show_processes()

		return

	# GENERATES PROCESSES RANDOMLY
	def generate_randomly(self, number):
		print("\n\nCreating {} Processes\n\n".format(number))
		for i in range(number):
			priority = 0
			arrival_time = randint(0, self.duration)
			duration_time = randint(0, self.duration)
			cpu_bound = bool(random.getrandbits(1))
			user_level = bool(random.getrandbits(1))
			if user_level:
				priority = randint(1,4)
				tmp_process = process.Process(arrival_time=arrival_time, priority=priority, duration_time=duration_time, user_level=user_level, process_id=i, cpu_bound=cpu_bound)
				self.submission_queue.append(tmp_process)
			else:
				tmp_process = process.Process(arrival_time=arrival_time, priority=priority, duration_time=duration_time, user_level=user_level, process_id=i, cpu_bound=cpu_bound)
				self.submission_queue.append(tmp_process)
		self.show_processes()

		return

	# SHOW PROCESSES
	def show_processes(self):
		print("\nCreated Processes => \n\n")
		for proc in self.submission_queue:
			print("Process ID {}, ARRIVED = {}, DURATION = {}, SIZE = {}, CPU BOUND = {}, USER LEVEL = {}, DISK = {}, PRINTER = {}".format(proc.process_id, proc.arrival_time, proc.duration_time, proc.size, proc.cpu_bound, proc.user_level, proc.disk, proc.printer))
		print("\n\n")
		return


	# START THE SIMULATION
	def start(self, check):
		#root = Tk()
		#app = Application(root, system=self)
		#app.fill_list()
		for step in range(self.duration):
			time.sleep(1)

			cpu_usage = self.get_pc_usage()
			memory_usage = self.memory_usage()

			print("\n#################################################\n")
			print("CPU Usage [####  ] =  {} %".format(cpu_usage), end="\t\t\t")
			print("Memory Usage [####  ] = {} %\n\n".format(memory_usage))
			print("STEP = ", step)
			print("CPU 1 = ", self.cpus[0].state)
			print("CPU 2 = ", self.cpus[1].state)
			print("CPU 3 = ", self.cpus[2].state)
			print("CPU 4 = ", self.cpus[3].state, end="\n\n")
			print("\nProcess in Real Time Queue = \n")

			self.handle_io()

			for proc in self.memory.realTimeQueue:
				print("Process {}, STATE = {}, ARRIVED = {}, DURATION = {}, SIZE = {}".format(proc.process_id, proc.state, proc.arrival_time, proc.duration_time, proc.size))
			print("\nProcess in User Queue = \n")

			for proc in self.memory.userQueue:
				print("Process {}, STATE = {}, ARRIVED = {}, DURATION = {}, SIZE = {}".format(proc.process_id, proc.state, proc.arrival_time, proc.duration_time, proc.size))
			print("\n#################################################\n")

			if(step % check == 0):
				self.handle_system(step)
			for cpu in self.cpus:
				cpu.handle_step()
		print("\n\nSimulation Finished\n\n")
		#print("Processos finalizados = ", self.terminated_processes)
		#root.mainloop()
		return

	# Handles I/O processes who are waiting for disk or printer
	def handle_io(self):
		if(len(self.memory.userQueue) > 0):
			for proc in self.memory.userQueue:
				if self.disk1 != None:
					if proc.process_id == self.disk1:
						proc.io_quantum -= 1

						if proc.io_quantum == 0:
							proc.state = "READY"
							self.disk1 = None
							proc.waiting_io = False
				else:
					if proc.waiting_io:
						if(proc.disk == True):
							self.disk1 = proc.process_id
							proc.waiting_io = False
							proc.io_quantum = 3

				if self.printer1 != None:
					if proc.process_id == printer1:
						proc.io_quantum -= 1

						if proc.io_quantum == 0:
							proc.state = "READY"
							self.printer1 = None
							proc.waiting_io = False
				else:
					if proc.waiting_io:
						if proc.printer1 == True:
							self.printer1 = proc.process_id
							proc.waiting_io = False
							proc.io_quantum = 3



	# GET CPU USAGE 
	def get_pc_usage(self):
		usage = 0
		for cpu in self.cpus:
			if cpu.state == "OCCUPIED":
				usage += 25
		return usage

	# GET MEMORY USAGE
	def memory_usage(self):
		return (self.memory.occupied * 100 / self.memory.size)

	# Handles the submissed processes
	def handle_system(self, step):
		if len(self.submission_queue) > 0:
			for proc in self.submission_queue:
				self.handle_submission_queue(proc, step)

	def handle_submission_queue(self, process, step):
		if step >= process.arrival_time:
			if process.priority == 0:
				if(self.memory.size >= process.size + self.memory.occupied):
					self.memory.occupied += process.size
					self.memory.realTimeQueue.append(process)
					self.memory.primary_memory.append(process)
					process.state = "READY"
					print("\nProcess ID = {} added to Real Time Queue".format(process.process_id))
				else:
					for proc in self.memory.userQueue:
						if(proc.state == "SUSPENDED" or proc.state == "READY"):
							self.memory.userQueue.remove(proc)
							self.memory.occupied -= proc.size
							self.memory.swap_memory.append(proc)
							self.memory.realTimeQueue.append(proc)
							self.memory.occupied += proc.size

			else:

				if self.memory.size >= process.size + self.memory.occupied:
					process.state = "READY"
					self.memory.userQueue.append(process)
					self.memory.feedback1.append(process)
					self.memory.primary_memory.append(process)
					self.memory.occupied += process.size
					print("Process ID = {} added to User Queue".format(process.process_id))
				else:
					print("Not Enough Memory for this Process")

			self.submission_queue.remove(process)
		return

	def treat_process(self):
		return

	def get_process(self):
		tmp_proc = None
		feedback = ""

		if(len(self.memory.realTimeQueue) > 0):
			tmp_proc = self.memory.realTimeQueue[0]
			i = 0

			while tmp_proc.state != "READY" and i < len(self.memory.realTimeQueue):
				tmp_proc = self.memory.realTimeQueue[i]
				i += 1

			#print(tmp_proc.state)
			if tmp_proc.state != "READY":
				if len(self.memory.feedback1) > 0:
					tmp_proc = self.memory.feedback1[0]
					i = 0
					while tmp_proc.state != "READY" and i < len(self.memory.feedback1):
						tmp_proc = self.memory.feedback1[i]
						i += 1
					feedback = "feedback1"

					if(tmp_proc.state == "READY"):
						return (tmp_proc, feedback)

				elif len(self.memory.feedback2) > 0:
					tmp_proc = self.memory.feedback2[0]
					i = 0
					while tmp_proc.state != "READY" and i < len(self.memory.feedback2):
						tmp_proc = self.memory.feedback2[i]
						i += 1

					feedback = "feedback2"

					if(tmp_proc.state == "READY"):
						return (tmp_proc, feedback)

				elif len(self.memory.feedback3) > 0:
					tmp_proc = self.memory.feedback3[0]
					i = 0
					while tmp_proc.state != "READY" and i < len(self.memory.feedback3):
						tmp_proc = self.memory.feedback3[i]
						i += 1

					feedback = "feedback3"

					if(tmp_proc.state == "READY"):
						return (tmp_proc, feedback)
				"""
				if(len(self.memory.userQueue) > 0):
					tmp_proc = self.memory.userQueue[0]
					i = 0
					while tmp_proc.state != "READY" and i < len(self.memory.userQueue):
						tmp_proc = self.memory.userQueue[i]
						i += 1

					if tmp_proc.state != "READY":
						tmp_proc = None

			#if((self.memory.occupied + tmp_proc.size) > self.memory.size):
			#	pass
			#else:
			#	self.memory.occupied += tmp_proc.size
			#self.memory.realTimeQueue.remove(tmp_proc)

		elif (len(self.memory.userQueue) > 0):
			tmp_proc = self.memory.userQueue[0]
			i = 0
			while tmp_proc.state != "READY" and i < len(self.memory.userQueue):
				tmp_proc = self.memory.userQueue[i]
				i += 1

			#print(tmp_proc.state)
			if tmp_proc.state != "READY":
				tmp_proc = None

			#if((self.memory.occupied + tmp_proc.size) > self.memory.size):
			#	pass
			#else:
			#	self.memory.occupied += tmp_proc.size
			#self.memory.userQueue.remove(tmp_proc)
		"""

		elif len(self.memory.feedback1) > 0:
			tmp_proc = self.memory.feedback1[0]
			i = 0
			while tmp_proc.state != "READY" and i < len(self.memory.feedback1):
				tmp_proc = self.memory.feedback1[i]
				i += 1
			feedback = "feedback1"

			if(tmp_proc.state == "READY"):
				return (tmp_proc, feedback)

		elif len(self.memory.feedback2) > 0:
			tmp_proc = self.memory.feedback2[0]
			i = 0
			while tmp_proc.state != "READY" and i < len(self.memory.feedback2):
				tmp_proc = self.memory.feedback2[i]
				i += 1

			feedback = "feedback2"

			if(tmp_proc.state == "READY"):
				return (tmp_proc, feedback)

		elif len(self.memory.feedback3) > 0:
			tmp_proc = self.memory.feedback3[0]
			i = 0
			while tmp_proc.state != "READY" and i < len(self.memory.feedback3):
				tmp_proc = self.memory.feedback3[i]
				i += 1

			feedback = "feedback3"

			if(tmp_proc.state == "READY"):
				return (tmp_proc, feedback)

		if(tmp_proc != None):
			if(tmp_proc.state != "READY"):
				tmp_proc = None
		return (tmp_proc, "NONE")

if __name__ == "__main__":

	logging.basicConfig(filename='scheduler.log', level=logging.INFO)
	print("##################################################################")
	print("#######            Process Scheduler Simulator             #######")
	print("##################################################################")
	print("\n\n\n")
	print("Welcome to the Process Scheduler Simulator\n")

	numberOfProcesses = int(input("Please Enter a number of Processes that you want to create: "))
	simulationDurationMs = int(input("\nInsert the duration of the Simulation (ms): "))
	overheadMs = int(input("\nInsert the overhead time for process change: "))

	choice = input("\nEnter R for random generate or M for manual generate of the processes: ")
	
	sim = Simulator(simulationDurationMs)

	if choice.upper() == "R":
		sim.generate_randomly(numberOfProcesses)

	if choice.upper() == "M":
		sim.generate_manualy(numberOfProcesses)

	sim.start(overheadMs)