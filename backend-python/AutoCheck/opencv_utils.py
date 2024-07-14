import cv2



def paint(img_path, point_list_res):
    img = cv2.imread(img_path)
    for i in point_list_res:
        lt = i[0]
        rd = i[1]
        res = i[2]
        if res == 1:
            cv2.rectangle(img, lt, rd, (0, 255, 0), 2)
        elif res == 0:
            cv2.rectangle(img, lt, rd, (0, 0, 255), 2)
        else:
            print('False',type(res),res)
    # save_path = '{}.jpg'.format(img_path[:-4]+'_check_result')
    save_path = img_path[:-4]+'_check_result'+img_path[-4:]
    cv2.imwrite(save_path, img)

