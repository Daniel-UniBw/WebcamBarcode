# WebcamBarcode
## Installation
### MacOS X
- Environment erstellen, wenn gewollt (Conda, venv)
- brew install zbox
- pip install -r requirements.txt
 
mkdir ~/lib
ln -s $(brew --prefix zbar)/lib/libzbar.dylib ~/lib/libzbar.dylib

### Windows
- Environment erstellen wenn gewollt
- pip install -r requirements
- Installation der x64 Version von https://www.microsoft.com/en-US/download/details.aspx?id=40784
