#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 2019/09/16 by DQ
 
import os
import matplotlib.pyplot as plt
import numpy as np
 
MainDir = '/home/siasun/JN/darknet'
TrainLogPath = os.path.join(MainDir, 'backup', 'TrainLog_2020-2-16-23-24.txt')
Loss, AgvLoss = [], []
with open(TrainLogPath, 'r') as FId:
	TxtLines = FId.readlines()
	for TxtLine in TxtLines:
		SplitStr = TxtLine.strip().split(',')
		Loss.append(float(SplitStr[0]))
		AgvLoss.append(float(SplitStr[1]))
 
IterNum = len(AgvLoss)
StartVal, EndVal, Stride = 1000, IterNum, 100 #视情况修改
Xs = np.arange(StartVal, EndVal, Stride)
Ys = np.array(AgvLoss[StartVal:EndVal:Stride])
plt.plot(Xs, Ys,label='avg_loss')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("Loss-Iter curve")
plt.legend()
plt.show()
