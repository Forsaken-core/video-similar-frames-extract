import cv2
import matplotlib.pyplot as plt

def dhash(image):    # 将图片转化为9*8    
    image = cv2.resize(image, (9, 8), interpolation=cv2.INTER_CUBIC)    # 将图片转化为灰度图    
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) 
    # plt.imshow(gray,cmap ='gray')
    # plt.show()
    # cv2.imshow("1",gray)
    # cv2.waitKey(0)   
    dhash_str = ''    
    for i in range(8):        
        for j in range(8):            
            if gray[i, j] > gray[i, j + 1]:                
                dhash_str = dhash_str + '1'            
            else:                
                dhash_str = dhash_str + '0'    
    result = ''    
    for i in range(0, 64, 4):        
        result += ''.join('%x' % int(dhash_str[i: i + 4], 2))    
    # print("dhash值",result)

    return result

#计算两个哈希值之间的差异
def campHash(hash1, hash2):    
    n = 0    # hash长度不同返回-1,此时不能比较    
    if len(hash1) != len(hash2):        
        return -1    # 如果hash长度相同遍历长度    
    for i in range(len(hash1)):        
        if hash1[i] != hash2[i]:            
            n = n + 1    
    return n
def simlarity(img1,img2):
    return campHash(dhash(img1),dhash(img2))
