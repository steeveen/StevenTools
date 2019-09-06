def getCircile(img):
    import numpy as np
    result=np.ones((512,512))
    for i in range(512):
        for j in range(512):
            if img[i,j,0]==img[i,j,1] and img[i,j,0]==img[i,j,2]:
                result[i,j]=0
    return result


ip=r'D:\dataset\caData\result'
op=r'D:\dataset\caData\d'



from glob import glob
from natsort import natsorted
from skimage import io as sio
import os
p=r'G:\实验\finaltest\肿瘤标签'
fps=natsorted(glob(os.path.join(p,'*')))
import shutil
for i in range(len((fps))):
    shutil.move(fps[i],os.path.join(p,str(i)+'.jpg'))