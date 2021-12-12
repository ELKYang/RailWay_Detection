import cv2
import os

def video2pic():
    cap = cv2.VideoCapture("./video/194526AA_Trim.mp4")
    c = 1
    frameRate = 1  # 帧数截取间隔
    k=1
    while(True):
        ret, frame = cap.read()
        if ret:
            if(c % frameRate == 0):
                print("开始截取视频第：" + str(k) + " 张")
                # 这里就可以做一些操作了：显示截取的帧图片、保存截取帧到本地
                cv2.imwrite("./video/194526AA/" + str(k) + '.jpg', frame)  # 这里是将截取的图像保存在本地
                k=k+1
            c += 1
            cv2.waitKey(0)
        else:
            print("所有帧都已经保存完成")
            break
    cap.release()

def pic2video():
    file_dir='./video/194526AA_detected'
    def get_images_by_dir(dirname):
        img_names = os.listdir(dirname)
        img_names.sort(key=lambda x:int(x.split('.')[0]))
        img_paths = [dirname+'/'+img_name for img_name in img_names]
        return img_paths
    paths=get_images_by_dir(file_dir)
    video=cv2.VideoWriter('./video/194526AA_result.mp4',cv2.VideoWriter_fourcc(*'MJPG'),30,(1280,720))  #定义保存视频目录名称及压缩格式，fps=10,像素为1280*720
    for i in range(1,len(paths)):
        img=cv2.imread(paths[i-1])  #读取图片
        print("process num:{}".format(i))
    #     img=cv2.resize(img,(1280,720)) #将图片转换为1280*720
        video.write(img)   #写入视频
    video.release()
