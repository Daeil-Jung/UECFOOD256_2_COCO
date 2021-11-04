import argparse
import glob
import os
from PIL import Image
import shutil
import json

parser = argparse.ArgumentParser(description='Transform UECFOOD dataset like COCO dataset structure')
parser.add_argument('dataset', type=str, help='Choose UECFOOD256 or UECFOOD100, now support only UECFOOD256',
                    default="UECFOOD256", choices=["UECFOOD256", "UECFOOD100"])
parser.add_argument('--path', '-p', type=str, help="Path of target dataset", default="dataset256")
parser.add_argument('--dest', '-d', type=str, help="Where you make coco dataset", default="uecfood256_coco")

args = parser.parse_args()

if __name__ == '__main__':
    # Exception handling
    if not os.path.exists(args.path):
        raise NameError('Incorrect target dataset path')
    if not os.path.exists(args.dest):
        os.mkdir(args.dest)

    # Define variables
    attrDict = dict()
    categories = list()
    images = list()
    annotations = list()
    anno_id = 1

    # Add categories attribute
    with open(args.path + "/UECFOOD256/category.txt") as f:
        cat_txt = f.readlines()[1:]

    for cat_line in cat_txt:
        cat_line = cat_line.replace("\n", "")
        cat_id, cat_name = cat_line.split("\t")
        categories.append({"supercategory": "none", "id": int(cat_id), "name": cat_name})

    attrDict["categories"] = categories

    # Walk directory process
    folders = glob.glob(args.path + "/*/*/")
    for folder in folders:
        image_paths = glob.glob(folder + "*.jpg")
        cat_id = folder.split(os.sep)[-2]
        print("Now processing ", cat_id, "folder")

        # Add image infos and copy into destination directory
        for image_path in image_paths:
            image = Image.open(image_path)
            if not any(row['file_name'] == image_path.split(os.sep)[-1] for row in images):
                images.append({"file_name": image_path.split(os.sep)[-1], "height": image.height, "width": image.width,
                               "id": int(image_path.split(os.sep)[-1].split(".")[0])})
                shutil.copy(image_path, args.dest + "/" + image_path.split(os.sep)[-1])

        # Add annotations
        with open(folder + "bb_info.txt") as f:
            lines = f.readlines()[1:]
        for line in lines:
            line = line.replace("\n", "")
            img, x1, y1, x2, y2 = line.split(" ")

            annotations.append(
                {"id": anno_id, "bbox": [int(x1), int(y1), (int(x2) - int(x1)), (int(y2) - int(y1))], "image_id": int(img),
                 "segmentation": [], "ignore": 0, "iscrowd": 0, "category_id": cat_id, "area": 0})
            anno_id += 1

    attrDict["images"] = images
    attrDict["annotations"] = annotations
    attrDict["type"] = "instances"

    jsonString = json.dumps(attrDict)
    with open(args.dest + "/annotations.json", "w") as f:
        f.write(jsonString)
