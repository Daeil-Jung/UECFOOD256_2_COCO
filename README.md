# Introduce
 UECFOOD256 dataset to COCO dataset structure. 

# Dataset download
### UECFOOD101 download
**Currently not supported by my project.**  
~~[http://foodcam.mobi/dataset100.html](http://foodcam.mobi/dataset100.html)~~
### UECFOOD256 download
[http://foodcam.mobi/dataset256.html](http://foodcam.mobi/dataset256.html)  
### Split information
For the train-test split we also use:  
[http://foodcam.mobi/uecfood_split.zip](http://foodcam.mobi/uecfood_split.zip)  

# Split rule
In split information,

`Training set` = `val0.txt`, `val1.txt`, `val2.txt`  
`Validation set` = `val3.txt`  
`Test set` = `val4.txt`

# Installation and example usage
```bash
git clone https://github.com/Daeil-Jung/UECFOOD256_2_COCO
pip install pillow
cd UECFOOD256_2_COCO
python uecfood256_2_coco.py UECFOOD256
```

# How to use
```bash
uecfood256_2_coco.py [-h] [--path PATH] [--dest DEST] {UECFOOD256,UECFOOD100}
```

Transform UECFOOD dataset like COCO dataset structure

### positional arguments:
  `{UECFOOD256,UECFOOD100}`: Choose UECFOOD256 or UECFOOD100, now support only UECFOOD256

### optional arguments:

|Header|Description|
|:---:|---|
|-h, --help|show this help message and exit|
|--path PATH, -p PATH|Path of target dataset|
|--dest DEST, -d DEST|Where you make coco dataset|

# Default tree structure 
```bash
├UECFOOD256_2_COCO
├─dataset256
│  └─UECFOOD256
│      ├─1.jpg
│      ├─10.jpg
│      ├─100.jpg
│      ├─ ...
├uecfood_split
│  ├─uecfood100_split
│  └─uecfood256_split
│      ├─val0.txt
│      ├─val1.txt
│      ├─val2.txt
│      ├─val3.txt
│      ├─val4.txt
├─uecfood256_2_coco.py
```

# Output
```bash
├uecfood256_coco
├─classes.txt
├─*.jpg
├─annotations
│  ├─train_anno.json
│  ├─test_anno.json
│  └─valid_anno.json
```

# To-do list
- Expand the contents to be applicable to UECFOOD101 dataset