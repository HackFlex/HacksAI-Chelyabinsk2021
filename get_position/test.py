from yolov5.detect import run as run_classifier
import sys
import cv2

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

def print_param(path_img, list_dist, list_angle_mesta, list_angle_azimut):
	for i in range(len(list_dist)):
		print("Название тестового файла: ", path_img)
		print(f'Расстояние до самолета:    {list_dist[i]:.2f}, м')
		print("Углы в СК камеры:")	
		print(f'	Угол места:            {list_angle_mesta[i]:.4}, гр')
		print(f'	Азимут:                {list_angle_azimut[i]:.4}, гр')
		# print("Углы в СК аэродрома:")	
		# print(f'	Угол места:            {list_angle_mesta[i]:.4}, гр')
		# print(f'	Азимут:                {list_angle_azimut[i]:.4}, гр')	
		print(f'Тангаж:                    {0.:.4}, гр')
		print(f'Крен:                      {0.:.4}, гр')
		print(f'Рысканье:                  {0.:.4}, гр')

def get_sodel(img):
    ddept=cv2.CV_16S
    scale=1.2
    ksize=3
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x = cv2.Sobel(gray, ddept, 1, 0, ksize=ksize, scale=scale)
    y = cv2.Sobel(gray, ddept, 0, 1, ksize=ksize, scale=scale)
    absx= cv2.convertScaleAbs(x)
    absy = cv2.convertScaleAbs(y)
    grad = cv2.addWeighted(absx, 0.5, absy, 0.5,0)
    return grad

if __name__ == "__main__":
	num_arg = len(sys.argv)
	if (num_arg <= 1):
		print("Неправильное количество аргументов")
		exit()
	for i in range(1, num_arg):
		path_img = sys.argv[i]
		# img = cv2.imread(path_img)
		# process_img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
		# cv2.imwrite('processed image_' + path_img, process_img)
		list_label = run_classifier(conf_thres=0.25, return_koord=True, classes=[4], save_txt=False, source='./' + path_img) #, imgsz=3840
		cam = Camera()
		Xreal = 59.7  # m
		# Xreal = find_Xreal(тангаж, крен, рысканье)
		list_dist = cam.find_distance(list_label, Xreal)
		list_angle_mesta = cam.find_angle_mesta(list_label)
		list_angle_azimut = cam.find_angle_azimut(list_label)
		print_param(path_img, list_dist, list_angle_mesta, list_angle_azimut)
			