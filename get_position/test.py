from yolov5.detect import run as run_classifier

class Camera:
	def __init__(self, X=3840, Y=2160, SizeX=7.2 / 10 / 100, 
	SizeY=5.3 / 10 / 100, F=0.08, angle_x=5.6, angle_y=3.74):
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


def print_param(path_img, list_dist, list_angle_mesta, list_angle_azimut,
				list_tang, list_kren, list_risk):
	params = []
	for i in range(len(list_dist)):
		print('Название тестового файла: ', path_img)
		print(f'Расстояние до самолета:    {list_dist[i]:.2f}, м')
		print('Углы в СК камеры:')
		print(f'	Угол места:            {list_angle_mesta[i]:.4}, гр')
		print(f'	Азимут:                {list_angle_azimut[i]:.4}, гр')
		# print("Углы в СК аэродрома:")	
		# print(f'	Угол места:            {list_angle_mesta[i]:.4}, гр')
		# print(f'	Азимут:                {list_angle_azimut[i]:.4}, гр')	
		print(f'Тангаж:                    {list_tang[i]:.4}, гр')
		print(f'Крен:                      {list_kren[i]:.4}, гр')
		print(f'Рысканье:                  {list_risk[i]:.4}, гр')

		params.append({
			'Название тестового файла': path_img,
			'Расстояние до самолета': list_dist[i],
			'Угол места': list_angle_mesta[i],
			'Азимут': list_angle_azimut[i],
			'Тангаж': list_tang[i],
			'Крен': list_kren[i],
			'Рысканье': list_risk[i]
		})
	return params

def get_position(items):
	if not items or len(items) < 1:
		raise Exception('Неправильное количество аргументов')
	for i in range(len(items)):
		path_img = items[i]
		list_label = run_classifier(conf_thres=0.25, return_koord=True, classes=[4], save_txt=False, source='./' + path_img)#, imgsz=3840)
		cam = Camera()
		Xreal = 59.7  # m
		# Xreal = find_Xreal(тангаж, крен, рысканье)
		list_dist = cam.find_distance(list_label, Xreal)
		list_angle_mesta = cam.find_angle_mesta(list_label)
		list_angle_azimut = cam.find_angle_azimut(list_label)
		return print_param(path_img, list_dist, list_angle_mesta, list_angle_azimut)
			