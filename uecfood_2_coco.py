import argparse
import os
from PIL import Image
import shutil
import json

parser = argparse.ArgumentParser(description='Transform UEC FOOD dataset like COCO dataset structure')
parser.add_argument('dataset', type=str, help='Choose UECFOOD256 or UECFOOD100', choices=["UECFOOD256", "UECFOOD100"])
parser.add_argument('--path', '-p', type=str, help="Path of target dataset", default="")
parser.add_argument('--dest', '-d', type=str, help="Where you make coco dataset", default="")
args = parser.parse_args()


def img_n_anno_proc(data_list, target_path, dest_path):
    anno_id = 1
    images = list()
    annotations = list()

    for pth in data_list:
        image_path = pth.replace("\n", "")
        prefix, cat_id, img_name = image_path.split("/")

        # Add image infos and copy into destination directory
        image = Image.open(target_path + "/" + image_path)
        if not any(row['file_name'] == image_path.split("/")[-1] for row in images):
            images.append({"file_name": image_path.split("/")[-1], "height": image.height, "width": image.width,
                           "id": int(image_path.split("/")[-1].split(".")[0])})
            shutil.copy(target_path + "/" + image_path, dest_path + "/" + image_path.split("/")[-1])

        # Add annotations
        with open(target_path + "/" + prefix + "/" + cat_id + "/bb_info.txt") as f:
            lines = f.readlines()[1:]

        for line in lines:
            line = line.replace("\n", "").split(" ")
            if line[0] == image_path.split("/")[-1].split(".")[0]:
                img, x1, y1, x2, y2 = line
                annotations.append(
                    {"id": anno_id, "bbox": [int(x1), int(y1), (int(x2) - int(x1)), (int(y2) - int(y1))],
                     "image_id": int(img),
                     "segmentation": [[int(x1), int(y1), int(x2), int(y1), int(x2), int(y2), int(x1), int(y2)]],
                     "ignore": 0, "iscrowd": 0, "category_id": int(cat_id),
                     "area": (int(x2) - int(x1)) * (int(y2) - int(y1))})
                anno_id += 1

    return images, annotations


if __name__ == '__main__':
    if args.dataset == "UECFOOD256":
        target_path = args.path + "dataset256"
        dest_path = args.dest + "uecfood256_coco"
    else:
        target_path = args.path + "dataset100"
        dest_path = args.dest + "uecfood100_coco"

    # Exception handling
    if not os.path.exists(target_path):
        raise NameError('Incorrect target dataset path')
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
        os.mkdir(dest_path + "/annotations")

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
    with open(target_path + "/" + args.dataset + "/category.txt") as f:
        cat_txt = f.readlines()[1:]

    for cat_line in cat_txt:
        cat_line = cat_line.replace("\n", "")
        cat_id, cat_name = cat_line.split("\t")
        categories.append({"supercategory": "none", "id": int(cat_id), "name": cat_name})
        cat_output = cat_output + cat_name + "', '"

    cat_output = cat_output + "\b"
    with open(dest_path + "/classes.txt", "w") as f:
        f.write(cat_output)

    attrDict["categories"] = categories
    attrDict["type"] = "instances"

    print("#####################")
    print("Generating train annotations")
    images, annotations = img_n_anno_proc(tr_list, target_path, dest_path)

    attrDict["images"] = images
    attrDict["annotations"] = annotations

    jsonString = json.dumps(attrDict)
    with open(dest_path + "/annotations/train_anno.json", "w") as f:
        f.write(jsonString)

    print("#####################")
    print("Generating validation annotations")
    images, annotations = img_n_anno_proc(va_list, target_path, dest_path)

    attrDict["images"] = images
    attrDict["annotations"] = annotations

    jsonString = json.dumps(attrDict)
    with open(dest_path + "/annotations/valid_anno.json", "w") as f:
        f.write(jsonString)

    print("#####################")
    print("Generating test annotations")
    images, annotations = img_n_anno_proc(ts_list, target_path, dest_path)

    attrDict["images"] = images
    attrDict["annotations"] = annotations

    jsonString = json.dumps(attrDict)
    with open(dest_path + "/annotations/test_anno.json", "w") as f:
        f.write(jsonString)
