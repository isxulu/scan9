### 功能介绍

`run.sh` 脚本用于实现已知**poses**的情况下，重建稀疏点云并导出为`.ply`格

式。脚本内容包括utils文件夹下python文件及run.sh。

### 原理分析

1. 按照[COLMAP documentation](https://colmap.github.io/faq.html#reconstruct-sparse-dense-model-from-known-camera-poses)进行三部曲分别为特征提取、特征匹配、三角化。

2. 特别注意的是，doc要求：<!--Each image above must have the same `image_id` (first column) as in the database (next step).-->；意味着我们手动创建的camera.txt与images.txt，需要以database.db处理图片的顺序为准，这也就是为什么运行write_cam.py与write_image.py要在前两部曲之后的原因。
3. database.db中的相机内参与相机的poses需要覆盖。

### 运行方式

需要按照scan9的文件目录结构进行。

