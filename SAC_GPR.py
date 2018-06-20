import numpy as np

raw_array = np.fromfile("",dtype='uint8')


#print(raw_Data)
#print(np.size(raw_Data))
raw_Data = []
for i in  range(0,np.size(raw_array)-3):
    if all(raw_array[i:i+4]==[248,221,66,89]):
        if(i+812)<=np.size(raw_array):
            raw_Data.append(raw_array[i:i+812])
            i=i+812;
raw_Data = np.transpose(np.array(raw_Data))

