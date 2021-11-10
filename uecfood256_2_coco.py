import argparse
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


def img_n_anno_proc(data_list):
    anno_id = 1
    images = list()
    annotations = list()

    for pth in data_list:
        image_path = pth.replace("\n", "")
        prefix, cat_id, img_name = image_path.split("/")

        # Add image infos and copy into destination directory
        image = Image.open(args.path + "/" + image_path)
        if not any(row['file_name'] == image_path.split("/")[-1] for row in images):
            images.append({"file_name": image_path.split("/")[-1], "height": image.height, "width": image.width,
                           "id": int(image_path.split("/")[-1].split(".")[0])})
            shutil.copy(args.path + "/" + image_path, args.dest + "/" + image_path.split("/")[-1])

        # Add annotations
        with open(args.path + "/" + prefix + "/" + cat_id + "/bb_info.txt") as f:
            lines = f.readlines()[1:]

        for line in lines:
            line = line.replace("\n", "").split(" ")
            if line[0] == image_path.split("/")[-1].split(".")[0]:
                img, x1, y1, x2, y2 = line
                annotations.append(
                    {"id": anno_id, "bbox": [int(x1), int(y1), (int(x2) - int(x1)), (int(y2) - int(y1))],
                     "image_id": int(img),
                     "segmentation": [], "ignore": 0, "iscrowd": 0, "category_id": cat_id, "area": 0})
                anno_id += 1

    return images, annotations


if __name__ == '__main__':
    # Exception handling
    if not os.path.exists(args.path):
        raise NameError('Incorrect target dataset path')
    if not os.path.exists(args.dest):
        os.mkdir(args.dest)
        os.mkdir(args.dest + "/annotations")

    # Define variables
    attrDict = dict()
    categories = list()
    cat_output = "'"

    # train, validation, test list set up
    if args.dataset == "UECFOOD256":
        split_dir = "uecfood_split/uecfood256_split/"
    else:
        split_dir = "uecfood_split/uecfood100_split/"

    with open(split_dir + "val0.txt") as f:
        val0 = f.readlines()
    with open(split_dir + "val1.txt") as f:
        val1 = f.readlines()
    with open(split_dir + "val2.txt") as f:
        val2 = f.readlines()
    with open(split_dir + "val3.txt") as f:
        va_list = f.readlines()
    with open(split_dir + "val4.txt") as f:
        ts_list = f.readlines()

    tr_list = val0 + val1 + val2

    # Add categories attribute
    with open(args.path + "/" + args.dataset + "/category.txt") as f:
        cat_txt = f.readlines()[1:]

    for cat_line in cat_txt:
        cat_line = cat_line.replace("\n", "")
        cat_id, cat_name = cat_line.split("\t")
        categories.append({"supercategory": "none", "id": int(cat_id), "name": cat_name})
        cat_output = cat_output + cat_name + "', '"

    cat_output = cat_output + "\b"
    with open(args.dest + "/classes.txt", "w") as f:
        f.write(cat_output)

    attrDict["categories"] = categories
    attrDict["type"] = "instances"

    print("#####################")
    print("Generating train annotations")
    images, annotations = img_n_anno_proc(tr_list)

    attrDict["images"] = images
    attrDict["annotations"] = annotations

    jsonString = json.dumps(attrDict)
    with open(args.dest + "/annotations/train_anno.json", "w") as f:
        f.write(jsonString)

    print("#####################")
    print("Generating validation annotations")
    images, annotations = img_n_anno_proc(va_list)

    attrDict["images"] = images
    attrDict["annotations"] = annotations

    jsonString = json.dumps(attrDict)
    with open(args.dest + "/annotations/valid_anno.json", "w") as f:
        f.write(jsonString)

    print("#####################")
    print("Generating test annotations")
    images, annotations = img_n_anno_proc(ts_list)

    attrDict["images"] = images
    attrDict["annotations"] = annotations

    jsonString = json.dumps(attrDict)
    with open(args.dest + "/annotations/test_anno.json", "w") as f:
        f.write(jsonString)
