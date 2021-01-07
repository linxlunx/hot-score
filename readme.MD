# Hot Score

Refactored some magic from [BeautyPredict](https://github.com/ustcqidi/BeautyPredict). Created the dashboard with [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [AdminLTE](https://adminlte.io/)

Because the purpose of this tool is to label and score the images based on your preference, please find your own dataset.

## Prerequisite
- cmake
- lapack
- blas
- MongoDB

# Notes
- There are 2 directories under `dataset` forlder, `images` and `csv`. You can save the image dataset to `images` and save the score to `csv`
- `labelled` is a folder where you save the post processing data to be trained
- You can find the scripts to prepare, train, and predict the image under `scoring` folder
- For the rating tool, you can find it under `webapp` folder, I am using mongodb for the database
- Then you can use export script under folder `tools` after you feel enough with the data labelling
- For another notes, you can read the script directly :P
