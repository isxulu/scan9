#   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]
'''
1 PINHOLE 1600 1200 925.5456 922.6144 263.42592 198.10208
'''
###########################################################################################################
# 因为特征提取生成的 database 中图片的次序并不规则，则需先生成 databse，再根据其次序生成 images.txt                 #
# colmap request: Each image in images.txt must have the same image_id (first column) as in the database  #
###########################################################################################################
import numpy as np
import os
import sqlite3

current_dir = os.getcwd()
# 连接到.db文件
conn = sqlite3.connect('/data/xulu/datasets/mvs_dtu/scan9/database.db')

# 创建游标对象
cursor = conn.cursor()

'''
cameras
sqlite_sequence
images
keypoints
descriptors
matches
two_view_geometries
'''
# 执行SQL查询
cursor.execute('SELECT * FROM images')
# 获取查询结果
result = cursor.fetchall()
# # 遍历结果并打印数据
# for row in result:
#     print(row)
# 关闭数据库连接
conn.close()


output_lines = []
for row in result:
    image_name = row[1]
    cam_id = row[0]   # idx from 1 same with database.db not 0 
    image_num = image_name.split('.')[0]  # 提取文件名中的序号部分
    # print(image_num)
    file_name = f"{str(image_num).zfill(8)}_cam.txt"
    loc_file = os.path.join("./cams", file_name)
    if os.path.exists(loc_file):
        # 读取txt文件
        with open(loc_file, 'r') as f:
            lines = f.readlines()

        # 提取intrinsic部分的矩阵参数
        intrinsic_matrix = []
        start_index = lines.index('intrinsic\n') + 1
        for j in range(start_index, start_index + 3):
            row = [float(val) for val in lines[j].split()]
            intrinsic_matrix.append(row)

        intrinsic_matrix = np.array(intrinsic_matrix)

        fx = intrinsic_matrix[0, 0]
        fy = intrinsic_matrix[1, 1]
        cx = intrinsic_matrix[0, 2]
        cy = intrinsic_matrix[1, 2]

        # > output.file
        camera_id = 1

        output_line = f"{cam_id} PINHOLE 1600 1200 {fx} {fy} {cx} {cy}"
        output_lines.append(output_line)

# 将结果隔行写入image.txt文件
with open('./sparse_model/cameras.txt', 'w') as f:
    for line in output_lines:
        f.write(line + '\n')