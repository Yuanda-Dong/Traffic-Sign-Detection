# Source code of CNN model training

This folder is the source code of CNN model training

### DataSet
To run the code within this folder, please download data from [google drive](https://drive.google.com/file/d/1Yb7LBgUEpvZptOeEuVzV6ZksS_xqeW17/view?usp=sharing), and put folder `data` and `shenzhen-images` under this folder.

- [Documentation of Source Code](https://github.com/Yuanda-Dong/Client-Final-Deployment/tree/main/SourceCode/doc)


## Part 1: Train CNN model with OpenCV pre-processing

1. run [Sign_Classification_Unity.ipynb](https://github.com/Yuanda-Dong/Client-Final-Deployment/blob/main/SourceCode/Sign_Classification_Unity.ipynb)
2.
```sh
python3 Sign_Classification_Unity.py
```
The trained model, is saved as `../../model/sign.h5`.

## Part 2: OpenCV pre-processing on Shenzhen track

### Part 2.1: OpenCV pre-processing on the images of Shenzhen track
1. run [Shenzhen_OpenCV.ipynb](https://github.com/Yuanda-Dong/Client-Final-Deployment/blob/main/SourceCode/Shenzhen_OpenCV.ipynb)
2.
```sh
python3 Shenzhen_OpenCV.py
```

### Part 2.1: Call `sign.h5` to test shenzhen track

1. run [ShenzhenImages_Classification.ipynb](https://github.com/Yuanda-Dong/Client-Final-Deployment/blob/main/SourceCode/ShenzhenImages_Classification.ipynb)
2.
```sh
python3 ShenzhenImages_Classification.py
```
