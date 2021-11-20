# import yolov5.detect as yolov5
from yolov5.detect import run as run_classifier

class camera:
    def __init__(self, X = 3840, Y = 2160, SizeX = 7.2 / 10 / 100, SizeY = 5.3 / 10 / 100, F = 0.08):
        # param camera
        self.X = 3840
        self.Y = 2160
        self.SizeX = 7.2 / 10 / 100  # m
        self.SizeY = 5.3 / 10 / 100  # m
        self.F = 0.08  # m
        self.Cx = self.SizeX / self.X
        self.Cy = self.SizeY / self.Y

    def find_distance(self, list_labels, X_real):
        distance_list = []
        for i in range(len(list_labels)):
            label = list_labels[i]
            # center_x = int(float(label[1]) * camera.X)
            # center_y = int(float(label[2]) * camera.Y)
            width = int(float(label[3]) * self.X) / 2
            # height = int(float(label[4]) * camera.Y)
            distance = X_real / 2 * self.F / (width * self.Cx)
            distance_list.append(distance)
        return distance_list


if __name__ == "__main__":
    # opt = yolov5.parse_opt()
    # list_label = yolov5.main(opt)
    # list_label = run_classifier(conf_thres=0.5, return_koord=True, classes=[4], save_txt=False, source='D:\\test.jpg')
    # list_label = run_classifier(conf_thres=0.5, return_koord=True, classes=[4], source = './polyot/Набор данных по кейсу АО ЧРЗ Полет (для обучения и тестирования решений)/Дальность 1342 метра/2) Д=1342м, Тангаж=9град, Крен=0град.mp4')
    # list_label = run_classifier(conf_thres=0.5, return_koord=True, classes=[4], save_txt=False, source='./1342 3sec.mp4')
    list_label = run_classifier(conf_thres=0.25, return_koord=True, classes=[4], save_txt=False, source='./5445 1sec.mp4')
    # print("len list 1 = ", len(list_label))
    cam = camera()
    Xreal = 59.7  # m
    # Xreal = find_Xreal()
    list_dist = cam.find_distance(list_label, Xreal)
    for i in range(len(list_dist)):
        print('Расстояние до самолета ', i + 1, " = ", list_dist[i])
