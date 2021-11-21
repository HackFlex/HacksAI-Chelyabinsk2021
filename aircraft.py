from math import sin, cos, pi, tan

class AirCraft:
	'''
	pnts[i][j] - массив ключевых точек самолета точек.
	i - размеры в метрах:
		0 - правая консоль (окончание)
		1 - левая консоль (окончание)
		2 - нижняя часть шасси
		3 - нос
		4 - верхняя часть киля
		5 - левое окончание хвотового оперения
		6 - правое окончание хвотового оперения
	j:
		0 - x
		1 - y
		2 - z
	'''
	def __init__(self):
		self.pnts = [
		[-29.85, 2.7, -11.4],
		[29.85, 2.7, -11.4],
		[0, -5.1, 24.6],
		[0, 0, 29.4],
		[0, 11.1, -33.9],
		[10.2, 3, -32.4],
		[-10.2, 3, 32.4]
		]
		
	def rotate_tang(self, tang):
		# try:
		tang = tang * pi / 180.
		for i in range(len(self.pnts)):
			x_old = self.pnts[i][0]
			y_old = self.pnts[i][1]
			z_old = self.pnts[i][2]
			self.pnts[i][0] = x_old
			self.pnts[i][1] = y_old * cos(tang) + z_old * sin(tang)
			self.pnts[i][2] = -y_old * sin(tang) + z_old * cos(tang)
		# except:
		# 	print('rotate_tang fail')
		# 	self.pnts = [
		# [-29.85, 2.7, -11.4],
		# [29.85, 2.7, -11.4],
		# [0, -5.1, 24.6],
		# [0, 0, 29.4],
		# [0, 11.1, -33.9],
		# [10.2, 3, -32.4],
		# [-10.2, 3, 32.4]
		# ]
		

	def rotate_risk(self, risk):
		risk = risk * pi / 180.
		for i in range(len(self.pnts)):
			x_old = self.pnts[i][0]
			y_old = self.pnts[i][1]
			z_old = self.pnts[i][2]
			self.pnts[i][0] = x_old * cos(risk) + z_old * sin(risk)
			self.pnts[i][1] = y_old
			self.pnts[i][2] = -x_old * sin(risk) + z_old * cos(risk)

	def rotate_kren(self, kren):
		kren = kren * pi / 180.
		for i in range(len(self.pnts)):
			x_old = self.pnts[i][0]
			y_old = self.pnts[i][1]
			z_old = self.pnts[i][2]
			self.pnts[i][0] = x_old * cos(kren) - y_old * sin(kren)
			self.pnts[i][1] = x_old * sin(kren) + y_old * cos(kren)
			self.pnts[i][2] = z_old
			kren

	def rotate_aircraft(self, tang, kren, risk):
		self.rotate_tang(tang)
		self.rotate_kren(kren)
		self.rotate_risk(risk)
	'''
	заходит 3 угла.
	Функция поворачивает модель на углы, выделяет
	максимальные и минимальные Х и Y. И выдает 2 размера реальных
	arr_size[X, Y]
	'''
	def find_real_size(self, list_tang, list_kren, list_risk):
		size_list = []
		for j in range(len(list_tang)):
			tang = list_tang[j]
			kren = list_kren[j]
			risk = list_risk[j]
			self.rotate_aircraft(tang, kren, risk)
			X_min = self.pnts[0][0]
			X_max = self.pnts[0][0]
			Y_min = self.pnts[0][1]
			Y_max = self.pnts[0][1]
			for i in range(len(self.pnts)):
				if self.pnts[i][0] < X_min:
					X_min = self.pnts[i][0]
				if self.pnts[i][0] > X_max:
					X_max = self.pnts[i][0]
				if self.pnts[i][1] < Y_min:
					Y_min = self.pnts[i][1]
				if self.pnts[i][1] > Y_max:
					Y_max = self.pnts[i][1]
			X_real = X_max - X_min
			Y_real = Y_max - Y_min
			arr_size = [X_real, Y_real]
			size_list.append(arr_size)
		return size_list

if __name__ == "__main__":
	list_tang = [0.]
	list_kren = [0.]
	list_risk = [0.]
	air = AirCraft()
	list_size = air.find_real_size(list_tang, list_kren, list_risk)
	print(list_size)