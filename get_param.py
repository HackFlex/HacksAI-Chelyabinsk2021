from yolov5.detect import run as run_classifier
from camera import Camera
from aircraft import AirCraft

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

def get_param(items):
	if not items or len(items) < 1:
		raise Exception('Неправильное количество аргументов')
	for i in range(len(items)):
		path_img = items[i]
		list_label = run_classifier(conf_thres=0.25, return_koord=True, classes=[4], save_txt=False, source='./' + path_img)#, imgsz=3840)
		cam = Camera()
		# Xreal = 59.7  # m
		Xreal = AirCraft.find_Xreal()
		list_dist = cam.find_distance(list_label, Xreal)
		list_angle_mesta = cam.find_angle_mesta(list_label)
		list_angle_azimut = cam.find_angle_azimut(list_label)
		return print_param(path_img, list_dist, list_angle_mesta, list_angle_azimut)
			