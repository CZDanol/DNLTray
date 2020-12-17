import state

systems = []

class System:
	name = None
	
	config = {}

	def shouldGenerateComponent(self, s, t):
		return True