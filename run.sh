#!/bin/sh
PROJECT_PATH=$(dirname "$PWD")
echo $PROJECT_PATH

echo "1. Extracting features now!"
colmap feature_extractor \
    --database_path $PROJECT_PATH/scan9/database.db \
    --image_path $PROJECT_PATH/scan9/images

echo "2. Matching features now!"
colmap exhaustive_matcher --database_path $PROJECT_PATH/scan9/database.db

echo "** modify sparse_model in sequence of 'images' table in the database"
python ./utils/write_cam.py
python ./utils/write_image.py

echo "** modify database in terms of sparse_model"
python ./utils/write_dbcam_intrinsics.py \
    --db_path $PROJECT_PATH/scan9/database.db \
    --camera_path $PROJECT_PATH/scan9/sparse_model/cameras.txt --imagestxt_path $PROJECT_PATH/scan9/sparse_model/images.txt
python ./utils/write_dbimage_poses.py \
    --db_path $PROJECT_PATH/scan9/database.db \
    --imagestxt_path $PROJECT_PATH/scan9/sparse_model/images.txt

echo "3. Triangulating points now!"
colmap point_triangulator \
    --database_path $PROJECT_PATH/scan9/database.db  \
    --image_path $PROJECT_PATH/scan9/images \
    --input_path $PROJECT_PATH/scan9/sparse_model \
    --output_path $PROJECT_PATH/scan9/triangulated_model

echo "4. convert model into ply format!"
colmap model_converter \
        --input_path $PROJECT_PATH/scan9/triangulated_model \
        --output_path $PROJECT_PATH/scan9/output_ply/tri.ply \
        --output_type PLY