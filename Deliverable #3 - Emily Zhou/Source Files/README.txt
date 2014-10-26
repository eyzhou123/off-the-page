Off the Page:

This program will scan a drawing of a character and provide you with the options to:
1) Save GIFs of your character (walking, dancing and bobbing movements)
2) Interact with your character (make your character move around and perform actions using key presses)

This program requires:
1) OpenCV 
2) Python Imaging Library


Instructions for installing Homebrew and OpenCV:
Using terminal, enter the following:
>>> ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)”
>>> brew doctor
(follow all instructions)
>>> brew install python
(follow all instructions)
>>> brew tap homebrew/science
>>> brew install opencv
(follow all instructions, eg. pip install numpy, link files etc.)

detailed instructions for installing Homebrew and OpenCV at http://www.jeffreythompson.org/blog/2013/08/22/update-installing-opencv-on-mac-mountain-lion/


Instructions for installing PIL:
Using terminal, enter the following:
>>> sudo easy_install pip
>>> sudo pip install PIL

steps for installing PIL were found at http://blog.artooro.com/2013/01/04/how-to-install-pil-python-imaging-library-on-mac-os-x-10-8/


Instructions for installing libjpeg library (so that jpeg files can be read):
Using terminal, enter the following (involves reinstalling PIL)
>>> brew update
>>> brew install libjpeg libpng
>>> sudo pip install -I PIL

detailed instructions for installing libjpeg library at http://geekforbrains.com/how-to-fix-the-decoder-jpeg-not-available-error-when-using-pil-in-python