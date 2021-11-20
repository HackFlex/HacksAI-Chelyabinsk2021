class Camera:
	def __init__(self, X=3840, Y=2160, SizeX=7.2 / 10 / 100, SizeY=5.3 / 10 / 100, F=0.08, angle_x=5.6, angle_y=3.74):
		# param camera
		self.X = X
		self.Y = Y
		self.SizeX = SizeX  # m
		self.SizeY = SizeY  # m
		self.F = F  # m
		self.Cx = SizeX / X
		self.Cy = SizeY / Y
		self.angle_y = angle_y
		self.angle_x = angle_x

	def find_distance(self, list_labels, real_size):
		distance_list = []
		X_real = real_size[0]
		Y_real = real_size[1]
		for i in range(len(list_labels)):
			label = list_labels[i]
			width = int(float(label[3]) * self.X) / 2
			distance1 = (X_real / 2 * self.F / (width * self.Cx))
			height = int(float(label[4]) * self.Y) / 2
			distance2 = (Y_real / 2 * self.F / (height * self.Cy))
			distance = (distance1 + distance2) / 2
			distance_list.append(distance)
		return distance_list

	def find_angle_mesta(self, list_labels):
		angle_list = []
		for i in range(len(list_labels)):
			label = list_labels[i]
			center_y = float(label[2])
			angle = -self.angle_y * center_y + self.angle_y / 2
			angle_list.append(angle)
		return angle_list

	def find_angle_azimut(self, list_labels):
		angle_list = []
		for i in range(len(list_labels)):
			label = list_labels[i]
			center_x = float(label[1])
			angle = self.angle_x * center_x - self.angle_x / 2
			angle_list.append(angle)
		return angle_list

	def find_distance(self, list_labels, X_real, perc = 1.):
		distance_list = []
		for i in range(len(list_labels)):
			label = list_labels[i]
			width = int(float(label[3]) * self.X) / 2
			distance = (X_real / 2 * self.F / (width * self.Cx)) * perc
			distance_list.append(distance)
		return distance_list

	def find_angle_mesta(self, list_labels):
		angle_list = []
		for i in range(len(list_labels)):
			label = list_labels[i]
			center_y = float(label[2])
			angle = -self.angle_y * center_y + self.angle_y / 2
			angle_list.append(angle)
		return angle_list

	def find_angle_azimut(self, list_labels):
		angle_list = []
		for i in range(len(list_labels)):
			label = list_labels[i]
			center_x = float(label[1])
			angle = self.angle_x * center_x - self.angle_x / 2
			angle_list.append(angle)
		return angle_list