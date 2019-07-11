# hw_controller_ap_parser
A Python script to sort the AP list of Huawei Access Controller devices by their installation site using Bing geolocalization services.

Create a new Python environment then run:
```
pip install -r requirements.txt
```

Running ```--helps``` outputs

```
usage: app.py [-h] [--src SRC] [--dest DEST]

This tool is used to obtain a markdown-styled ASCII table of the access points
currently installed on a Huawei Access Controller.

optional arguments:
  -h, --help   show this help message and exit
  --src SRC    Path to source file. By default, it's .\data.txt.
  --dest DEST  Path to destination file. By default, it's .\tables.txt.
  ```
