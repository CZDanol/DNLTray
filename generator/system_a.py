import systems
import cargs

class System_A(systems.System):
	name = "A"

	config = {
		"unitSize": [25, 25, 15],
		"horizontalMountConenctorDistance": 6
	}

	def shouldGenerateComponent(self, s, t):
		if cargs.args.allCombinations:
			return True

		if t == "tray":
			hUnitCounts = [2, 3, 4, 6, 8]
			vUnitCounts = [1, 2, 3, 4, 6, 8]

			if s.config["unitCount"][0] not in hUnitCounts:
				return False
				
			if s.config["unitCount"][1] not in hUnitCounts:
				return False

			if s.config["unitCount"][2] not in vUnitCounts:
				return False

		elif t == "drawerTray" or t == "drawer":
			if s.config["unitCount"][0] not in [2, 3, 4]:
				return False

			if s.config["unitCount"][1] not in [2, 4, 6]:
				return False

			if s.config["unitCount"][2] not in [1, 2, 4]:
				return False

			if s.config["unitCount"][2] > s.config["unitCount"][0]:
				return False

		else:
			raise Exception("Not supported: " + t)

		return True


systems.systems.append(System_A())