# Introduce
 UEC FOOD dataset to COCO dataset structure. 

# Dataset download
### UECFOOD101 download
[http://foodcam.mobi/dataset100.html](http://foodcam.mobi/dataset100.html)
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
git clone https://github.com/Daeil-Jung/UECFOOD_2_COCO
pip install pillow
cd UECFOOD_2_COCO
python uecfood_2_coco.py UECFOOD256 # or UECFOOD100
```

# How to use
```bash
python uecfood_2_coco.py [-h] [--path PATH] [--dest DEST] {UECFOOD256,UECFOOD100}
```

Transform UEC FOOD dataset like COCO dataset structure

### positional arguments:
  `{UECFOOD256,UECFOOD100}`: Choose UECFOOD256 or UECFOOD100

### optional arguments:

|Header|Description|
|:---:|---|
|-h, --help|Show this help message and exit|
|--path PATH, -p PATH|Path of target dataset|
|--dest DEST, -d DEST|Where you make coco dataset|

# Default tree structure 
```bash
├UECFOOD_2_COCO
├─dataset256 # or dataset100
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
├─uecfood_2_coco.py
```

# Output
```bash
├uecfood256_coco # or uecfood100_coco
├─classes.txt
├─*.jpg
├─annotations
│  ├─train_anno.json
│  ├─test_anno.json
│  └─valid_anno.json
```