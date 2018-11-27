==========================================
SOFTWARE REQUIREMENTS
==========================================
OpenCV
Keras with Tensorflow backend
Pandas
NumPy
Pillow

==========================================
HOW TO RUN
==========================================

SCRIPT
-------------
sh runClothing.sh

sh Clean.sh


FOR TESTING
-------------
python fashion.py background1.jpg ./background1mask.png
python fashion.py background2.jpg ./background2mask.png

python clothing.py


OUTPUT FILES
-------------
background1mask.jpg / background2mask.jpg -> Shows the clothing extracted from the image
backgroundbounding1.png / backgroundbounding2.png -> Shows where the algorithm thinks the shirt is in the program with a blue rectangle
roi1.png / roi2.png -> background mask image cropped to only contain the clothing
roi1Extract.png / roi2Extract.png -> The clothing with the black background turned transparent
Output1.jpg / Output2.jpg -> Shows the shirts swapped, The two roiExtract images are placed inside the bounding rectangles of the opposite pictures


