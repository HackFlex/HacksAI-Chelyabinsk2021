# from predict_angle import

def func_kostya(img_name, box_pnts):
    return [0, 0, 0]

def get_angle_aircraft(img_name, list_label):
    list_kren = []
    list_tang = []
    list_risk = []
    for i in range(len(list_label)):
        label = list_label[i]
        width = label[3] * 1.2
        if width > 1:
            width = 1
        height = label[4] * 1.2
        if height > 1:
            height = 1
        pnt1_x = label[1] - width / 2
        pnt2_x = label[1] + width / 2
        pnt1_y = label[2] - height / 2
        pnt2_y = label[2] + height / 2
        box_pnts = [pnt1_x, pnt1_y, pnt2_x, pnt2_y]

        arr_angle = func_kostya(img_name, box_pnts)

        kren = arr_angle[0]
        tang = arr_angle[1]
        risk = arr_angle[2]
        list_kren.append(kren)
        list_tang.append(tang)
        list_risk.append(risk)
    return list_kren, list_tang, list_risk