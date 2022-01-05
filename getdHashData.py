# 使用dHash算法将视频数据集处理为图片数据
import cv2
import dhashSimlarity
import sys
import os
 
#进度条
def view_bar(num, total):
    rate = float(num) / float(total)
    rate_num = int(rate * 100)
    r = '\r[%s%s]%d%%,%d' % ("="*rate_num, " "*(100-rate_num), rate_num, num )
    sys.stdout.write(r)
    sys.stdout.flush()

def getimg(cap,i):
    cap.set(cv2.CAP_PROP_POS_FRAMES,i) 
    return cap.read()[1]

def makeVidData(video_file,save_path,begin_num = 0,dhash_thresh = 12):
    """
    :video_file:视频文件路径
    :save_path:图片保存路径，结尾去掉/
    :begin_num:数据保存命名的开始序号
    """
    cap = cv2.VideoCapture(video_file)#打开视频
    #创建类别文件夹
    if os.path.exists(save_path):
        pass
    else:
        os.mkdir(save_path)
    
    #保存第一帧
    img1=getimg(cap,1)
    cv2.imwrite(save_path+"/"+str(begin_num)+".jpg",img1)

    frames_num=cap.get(7)#获取帧数
    print(video_file+"         total frames: "+str(frames_num))

    # dHash剔除相似帧
    i=0
    j=begin_num
    
    while cap.isOpened():
        
        #每一次对比以上次的结尾为开始
        img1 = getimg(cap,i)  #读取帧为图片
        
        while(1):
            
            img2 = getimg(cap,i+1)
            i+=1
            view_bar(i+1,frames_num)
            if i >= frames_num-1:
                print("last frames: "+str(i))
                break
            if dhashSimlarity.simlarity(img1,img2)>=dhash_thresh:  #再继续读取，dHash>12,保存后一张
                cv2.imwrite(save_path+"/"+str(j+1)+".jpg",img2)
                # print(str(i)+"   "+str(dhashSimlarity.simlarity(img1,img2)))

                break
            
                
        # cv2.imshow('a', img1)
        # cv2.imshow('b', img2)
        # cv2.waitKey(1)
        # print("gray and average score is : "+str(SSIM.ssim(img1,img2)))
        
        if i >= frames_num-1:
            print("last frames: "+str(i))
            break
        # print(i)
        j+=1

def makeImgData(image_file,save_path,begin_num = 0,dhash_thresh = 12):
    """
    :video_file:视频文件路径
    :save_path:图片保存路径，结尾去掉/
    :begin_num:数据保存命名的开始序号
    """
    fileList = os.listdir(image_file)
    for i,f in enumerate(fileList):
        fileList[i] = int(f.split(".")[0])
    fileList.sort()
    #创建类别文件夹
    if os.path.exists(save_path):
        pass
    else:
        os.mkdir(save_path)
    
    #保存第一帧
    img1=cv2.imread(image_file+"/"+str(fileList[0])+".jpg")
    cv2.imwrite(save_path+"/"+str(begin_num)+".jpg",img1)

    frames_num=len(fileList)#获取帧数
    print(image_file+"         total frames: "+str(frames_num))

    # dHash剔除相似帧
    i=0
    j=begin_num
    
    for f in fileList:
        
        #每一次对比以上次的结尾为开始
        img1 = cv2.imread(image_file+"/"+str(fileList[i])+".jpg")  #读取帧为图片
        
        while(1):
            
            img2 = cv2.imread(image_file+"/"+str(fileList[i+1])+".jpg")
            i+=1
            view_bar(i+1,frames_num)
            if i >= frames_num-1:
                print("last frames: "+str(i))
                break
            if dhashSimlarity.simlarity(img1,img2)>=dhash_thresh:  #再继续读取，dHash>12,保存后一张
                cv2.imwrite(save_path+"/"+str(j+1)+".jpg",img2)
                # print(str(i)+"   "+str(dhashSimlarity.simlarity(img1,img2)))

                break
        
        if i >= frames_num-1:
            print("last frames: "+str(i))
            break
        # print(i)
        j+=1    


def main():
    '''
    用于一个视频文件为一类的数据集提取，视频文件名即为类别名
    '''
    # video_file="F:/DataSet/惠康/进食已使用数据"
    # save_path="H:/Software/Study/Datasets/pig/mydata"
    # for file in os.listdir(video_file): #file: 1.mp4 2.mp4....
    #     class_num = file.split(".")[0]
    #     makeVidData(video_file+"/"+file,save_path+"/"+class_num,dhash_thresh = 12)

    '''
    用于所有视频都为一类的数据提取，将图片按顺序放到指定文件夹下
    '''
    video_file="F:/DataSet/惠康/进食已使用数据"
    save_path="F:/DataSet/HuikangFeedDataset/BodyDetection/Body/mixHKJDBodySelfsup"
    for file in os.listdir(video_file): #file: 1abc.mp4 2cde.mp4....
        begin_num = len(os.listdir(save_path))
        makeVidData(video_file+"/"+file,save_path,dhash_thresh = 12,begin_num=begin_num)

    '''
    用于多个视频为一类的数据集提取
    '''
    # video_file="F:/DataSet/惠康/07"
    # save_path="F:/DataSet/huikangDataset/mydata"
    # begin_num = 0   # 数据命名开始的数字
    # for file in os.listdir(video_file): #file: 种猪13 01 1 （am）.mp4
    #     pen_num = int(file.split(" ")[1])   # 猪圈号
    #     pig_num = int(file.split(" ")[2])   # 每个圈的猪的序号
    #     folder_name = str(pen_num)+"-"+str(pig_num) # 最后，以此为每个类别的文件夹的名称
    #     last_name = 0   # 以int形式保存最后一张图片的名字
    #     if os.path.exists(save_path+"/"+folder_name):# 若目录存在，读取最后一个图片的序号
    #         sort_list = os.listdir(save_path+"/"+folder_name)
    #         sort_list = [int(i.split(".")[0]) for i in sort_list] 
    #         sort_list.sort()
    #         last_name = sort_list[-1]
    #         begin_num = last_name+1
    #     else:
    #         begin_num = 0
    #     makedata(video_file+"/"+file,save_path+"/"+folder_name,begin_num = begin_num)

    # makeImgData("F:/DataSet/HuikangFeedDataset/FaceDetection/rawpigfacePen2/5","F:/DataSet/HuikangFeedDataset/FaceDetection/pigfacePen2/5",begin_num = 0,dhash_thresh = 12)

    


if __name__ == '__main__':
    main()
    