## 项目概述(2020 Wuhan Fighting!)
基于Darknet版本的YOLOV3，2020年初为新型冠状病毒研发。
## Darknet安装
Darknet的安装较为容易，其项目主页为：https://pjreddie.com/darknet/yolo/  ，按照如下步骤进行即可
```
git clone https://github.com/pjreddie/darknet.git
```
修改darknet文件夹中的makefile文件
```
GPU=1 #如果使用GPU设置为1，CPU设置为0
CUDNN=1 #如果使用CUDNN设置为1，否则为0
OPENCV=1 #如果调用摄像头，还需要设置OPENCV为1，否则为0
OPENMP=0 #如果使用OPENMP设置为1，否则为0
DEBUG=0 #如果使用DEBUG设置为1，否则为0
ARCH= -gencode arch=compute_30,code=sm_30 \
-gencode arch=compute_35,code=sm_35 \
-gencode arch=compute_50,code=[sm_50,compute_50] \
-gencode arch=compute_52,code=[sm_52,compute_52] \
-gencode arch=compute_60,code=[sm_60,compute_60] \
-gencode arch=compute_61,code=[sm_61,compute_61]  #修改为自己显卡的架构
NVCC=/home/user/cuda-9.0/bin/nvcc #修改为自己的路径
```
然后进行项目代码编译
```
cd darknet
make
```
## 数据集准备
#### 标注工具
推荐使用labelimg进行标注，最好使用命令行安装版本，可在github上搜索即可获得
#### 数据编号
最好使用合理的编号，推荐在ubuntu 18.04下进行批量图像改名，可提供模式化修改，非常方便。**注意数据集中的图片最好都是.jpg的图像，否则使用voc_label.py生成最后训练数据文件时会默认将所有的图片后缀设置为jpg**
#### 数据组织（Pascal Voc格式）
使用labelimg进行数据标注时，请选择pascal voc的标注文件格式，在此格式下，每张图片对应生成一个xml标注文件
- 在darknet目录下新建以下文件夹

![](https://github.com/xywlpo/YOLOV3-Mask-Detection/blob/master/1.bmp)

将数据集的图片拷贝到JPEGImages文件夹中，数据集的标签文件拷贝到Annotations文件夹中，在VOC2007文件夹下新建test.py（在本项目提供的数据集压缩包中包含），可自动将数据集分裂成train.txt, val.txt, test.txt, trainval.txt。最后生成的目录如下图所示

![](https://github.com/xywlpo/YOLOV3-Mask-Detection/blob/master/2.bmp)








