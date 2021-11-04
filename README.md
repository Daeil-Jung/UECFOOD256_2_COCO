# Introduce
 UECFOOD256 dataset to COCO dataset structure

# Requirement
```
pip install pillow
```

# How to use
```
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
│      ├─1
│      ├─10
│      ├─100
│      ├─ ...
├─uecfood256_2_coco.py
```
