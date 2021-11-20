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
		pnts = [
			[-29.85, 2.7, -11.4],
			[29.85, 2.7, -11.4],
			[0, -5.1, 24.6],
			[0, 0, 29.4],
			[0, 11.1, -33.9],
			[10.2, 3, -32.4],
			[-10.2, 3, 32.4]
		]
		
	def rotate_tang(self, tang):
		matrix_tang = [
				[],
				[],
				[]
			]
		for i in range(len(self.pnts)):
			self.pnts[i] = self.pnts[i] * matrix_tang

	def rotate_kren(self, tang):
		# matrix_kren =
		pass

	def rotate_risk(self, tang):
		# matrix_risk =
		pass

	def rotate_aircraft(self, tang, kren, risk):
		self.pnts = self.rotate_tang(tang)
		self.pnts = self.rotate_kren(kren)
		self.pnts = self.rotate_risk(risk)
	'''
	заходит 3 угла.
	Функция поворачивает модель на углы, выделяет
	максимальные Х и Y. И выдает мини
	
	'''
	def find_Xreal(self, tang, kren, risk):
		pass