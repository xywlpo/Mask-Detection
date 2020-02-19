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
### 标注工具
推荐使用labelimg进行标注，最好使用命令行安装版本，可在github上搜索即可获得
### 数据编号
最好使用合理的编号，推荐在ubuntu 18.04下进行批量图像改名，可提供模式化修改，非常方便。注意数据集中的图片最好都是.jpg的图像，否则使用voc_label.py生成最后训练数据文件时会默认将所有的图片后缀设置为jpg
### 数据组织（Pascal Voc格式）
使用labelimg进行数据标注时，请选择pascal voc的标注文件格式，在此格式下，每张图片对应生成一个xml标注文件
- 在darknet目录下新建以下文件夹

![](https://github.com/xywlpo/YOLOV3-Mask-Detection/blob/master/1.bmp)

将数据集的图片拷贝到JPEGImages文件夹中，数据集的标签文件拷贝到Annotations文件夹中，在VOC2007文件夹下新建test.py（在本项目提供的数据集压缩包中包含），可自动将数据集分裂成train.txt, val.txt, test.txt, trainval.txt。最后生成的目录如下图所示

![](https://github.com/xywlpo/YOLOV3-Mask-Detection/blob/master/2.bmp)

由于yolov3的标签内容为一行5个数，分别代表：类别（从0开始编号）、bbox中心x坐标、bbox中心y坐标、bbox宽、bbox高。并且这些坐标都是归一化到0~1区间的，与VOC的标注不一样，因此这里还需进行转换，使用voc_label.py文件执行，该文件也可以下载：
```
wget https://pjreddie.com/media/files/voc_label.py
```
该文件有两处需要修改，分别是sets和classes，如下图所示

![](https://github.com/xywlpo/YOLOV3-Mask-Detection/blob/master/3.bmp)

运行该文件，则可获得2007_train.txt,2007_val.txt,2007_test.txt，VOCdevkit下的VOC2007也会多生成一个labels文件夹
```
python voc_label.py
cat 2007_train.txt 2007_val.txt  > train.txt
````
口罩数据集下载：[百度网盘](https://pan.baidu.com/s/1xAdLEfaDB3PLHyKl3Uq4Mg)，提取密码：givm。至此数据集就准备妥当了。
## 模型训练
1. 修改cfg/voc.data
```
classes = 1   #修改为自己类别的个数
train = <Path-to-Voc>/train.txt
valid = <Path-to-Voc>/2007_test.txt
names = data/voc.names
backup = backup
```
2. 修改data/voc.names和coco.names，打开对应的文件直接修改成自己的类名就可以
3. 修改模型的配置文件：cfg/yolov3.cfg。打开文件，ctrl+f搜yolo, 总共会搜出2-3个含有yolo的地方，每个地方都必须要改2处：
```
filters：3*（5+len（classes））；
其中：classes: len(classes) = 1，这里以单个类dog为例
filters = 18
classes = 1
可修改：random = 1：原来是1，显存小改为0。（是否要多尺度输出。）
```
4. cfg文件的开头可以选择batch和subdivisions的大小，batch表示多少张图进行权重更新，subdivisions表示当前批次按照几次分别送入网络

5. 预训练模型
- 下载darknet53预训练模型（适用于yolov3-416和yolov3-608，两个模型就是输入图像尺寸不同，608分辨率的效果更好一些）
```
wget https://pjreddie.com/media/files/darknet53.conv.74
[百度网盘](https://pan.baidu.com/s/1zcwCOfyivsxc_k4Ej74fKw)，提取码：oc4h
```
- 通过已有模型分离出backbone网络（通常用于yolov3-tiny的训练，yolov3-tiny不宜使用darknet53训练，因为两者结构就不相同）
```
./darknet partial cfg/yolov3-tiny.cfg yolov3-tiny.weights yolov3-tiny.conv.15 15
更多参见：https://github.com/AlexeyAB/darknet/blob/57e878b4f9512cf9995ff6b5cd6e0d7dc1da9eaf/build/darknet/x64/partial.cmd#L24
```
6. 模型训练
```
./darknet detector train cfg/voc.data cfg/yolov3.cfg darknet53.conv.74        #直接从头训练
./darknet detector train cfg/voc.data cfg/yolov3.cfg backup/yolov3.backup     #恢复训练
```
7. 训练loss绘制：本工程已修改成每隔200轮训练保存一次模型，同时保存所有的loss值为txt文件，可使用darknet目录下的draw_loss.py绘制loss

![](https://github.com/xywlpo/YOLOV3-Mask-Detection/blob/master/loss.bmp)

## Darknet网络调优技巧（from AlexeyAB）
```
- 首先对数据集进行检错，使用提供的如下库进行检测：https://github.com/AlexeyAB/Yolo_mark
- 数据集最好每个类有2000张图片，通常每个类需要2000-4000次迭代训练即可，因此总共需要至少迭代2000*类别数次迭代
- avg loss不再下降时可以停止训练，为了防止过拟合，需要在val loss由下降转向上升的拐点停止训练
- random=1可以设置适应多分辨率
- 数据集最好有没有标注的对象，即负样本，对应空的txt文件，最好有多少样本就设计多少负样本
- 对于一张图有很多个样本的情况，使用max=200属性(yolo层或者region层)
- 在训练完以后，进行目标检测的时候，可以提高网络的分辨率，以便刚好检测小目标
    - 不需要重新训练，需要使用原先低分辨率的权重，测用更高分辨率
    - 为了得到更高的检测效果，可以提升分辨率至608*608甚至832*832（需满足32的倍数）
```
## 模型测试
1. 测试命令
```
./darknet detect cfg/voc.data cfg/yolov3.cfg backup/yolov3_final.weights      #该命令本人修改过，可以之后输入图片名进行测试
```
2. 口罩训练采用cfg/yolov3.cfg，即608x608的输入分辨率，迭代4000次，测试结果如下

![](https://github.com/xywlpo/YOLOV3-Mask-Detection/blob/master/4.bmp)
![](https://github.com/xywlpo/YOLOV3-Mask-Detection/blob/master/5.bmp)
![](https://github.com/xywlpo/YOLOV3-Mask-Detection/blob/master/6.bmp)
![](https://github.com/xywlpo/YOLOV3-Mask-Detection/blob/master/7.bmp)
![](https://github.com/xywlpo/YOLOV3-Mask-Detection/blob/master/8.bmp)

## 项目实施
```
https://github.com/AlexeyAB/darknet#datasets
```
