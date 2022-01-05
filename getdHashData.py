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
    :save_path:图片保存路径，结尾去掉
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

# 用于图像数据集
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
    用于所有视频都为一类的数据提取，将图片按顺序放到指定文件夹下
    '''
    video_file="F:/DataSet/xxx"
    save_path="F:/DataSet"
    for file in os.listdir(video_file): #file: 1abc.mp4 2cde.mp4....
        begin_num = len(os.listdir(save_path))
        makeVidData(video_file+"/"+file,save_path,dhash_thresh = 12,begin_num=begin_num)


if __name__ == '__main__':
    main()
    
