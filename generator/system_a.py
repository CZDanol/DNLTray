import systems
import cargs

class System_A(systems.System):
	name = "A"

	config = {
		"unitSize": [25, 25, 15],
		"horizontalMountConenctorDistance": 6
	}

	def shouldGenerateComponent(self, s, t):
		s.targetReleases = []

		uc = s.config["unitCount"]

		if cargs.args.allCombinations:
			return True

		if t == "tray":
			hUnitCounts = [2, 3, 4, 6, 8]
			vUnitCounts = [1, 2, 3, 4, 6, 8]

			if uc[0] not in hUnitCounts:
				return False
				
			if uc[1] not in hUnitCounts:
				return False

			if uc[2] not in vUnitCounts:
				return False

			if uc[2] in [1, 2, 4, 6, 8] and uc[0:2] in [[2, 2], [3, 3], [4, 2], [4, 4], [6, 2], [6, 4], [6, 6], [8, 2], [8, 4], [8, 6], [8, 8]]:
				s.targetReleases += ["trays"]

		elif t == "drawerTray" or t == "drawer":
			if uc[0] not in [2, 3, 4]:
				return False

			if uc[1] not in [2, 4, 6]:
				return False

			if uc[2] not in [1, 2, 4]:
				return False

			if uc[2] > uc[0]:
				return False

			if uc in [[2, 2, 2], [4, 2, 2], [2, 3, 2], [2, 4, 2], [3, 4, 2], [4, 4, 4]]:
				s.targetReleases += ["drawers"]

		elif t == "wall":
			if uc[0] not in [1, 2, 3, 4, 6, 8]:
				return False

			if uc[2] not in [1, 2, 4, 6, 8]:
				return False

			s.targetReleases += ["drawers", "trays"]

		else:
			raise Exception("Not supported: " + t)

		return True


systems.systems.append(System_A())