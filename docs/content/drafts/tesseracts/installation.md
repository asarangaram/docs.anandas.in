### Install Engine
Installing tesseract binary seems straighforward. Followed the proceedure given tesseract's [github](https://tesseract-ocr.github.io/tessdoc/Compiling-–-GitInstallation.html), title "Installing With Autoconf Tools". 

After installation, while executing the tesseract binary, got the error `tesseract: error while loading shared libraries: libtesseract.so.5: cannot open shared object file: No such file or director`. This error was solved by running `sudo ldconfig`

Now the tesseract binary is ready to use.

### Data
downloaded language models using [tessdata_downloader](https://github.com/zdenop/tessdata_downloader)



