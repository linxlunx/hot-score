import cv2
import os
import pickle
import numpy as np
import random
from PIL import Image
from PIL import ImageEnhance
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file-rating", help="Rating file", required=True)
args = parser.parse_args()

rating_file_name = args.file_rating.split('/')[-1]
rating_path = "dataset/csv"

if not os.path.exists('{}/{}'.format(rating_path, rating_file_name)):
    print('Cannot find rating file!')
    sys.exit()

data_path = "dataset/images"
labelled_path = 'labelled'
model_path = "common/haarcascade_frontalface_alt.xml"
face_cascade = cv2.CascadeClassifier(model_path)

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

datagen = ImageDataGenerator(
                 featurewise_center = False,
                 samplewise_center  = False,
                 featurewise_std_normalization = False,
                 samplewise_std_normalization = False,
                 zca_whitening = False,
                 rotation_range = 20,
                 width_shift_range = 0.2,
                 height_shift_range = 0.2,
                 horizontal_flip = True,
                 vertical_flip = False)


def detectFace(detector,image_path, image_name):
    imgAbsPath = image_path + image_name
    img = cv2.imread(imgAbsPath)
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    w = img.shape[1]
    faces = detector.detectMultiScale(gray, 1.1, 5, 0, (w//2, w//2))

    resized_im = 0

    if len(faces) == 1:
        face = faces[0]
        croped_im = img[face[1]:face[1]+face[3],face[0]:face[0]+face[2],:]
        resized_im = cv2.resize(croped_im, (224,224))

        if resized_im.shape[0] != 224 or resized_im.shape[1] != 224:
            print("invalid shape")

    else:
        print(image_name+" error " + str(len(faces)))
    return resized_im


_errstr = "Mode is unknown or incompatible with input array shape."


def bytescale(data, cmin=None, cmax=None, high=255, low=0):
    if data.dtype == np.uint8:
        return data

    if high > 255:
        raise ValueError("`high` should be less than or equal to 255.")
    if low < 0:
        raise ValueError("`low` should be greater than or equal to 0.")
    if high < low:
        raise ValueError("`high` should be greater than or equal to `low`.")

    if cmin is None:
        cmin = data.min()
    if cmax is None:
        cmax = data.max()

    cscale = cmax - cmin
    if cscale < 0:
        raise ValueError("`cmax` should be larger than `cmin`.")
    elif cscale == 0:
        cscale = 1

    scale = float(high - low) / cscale
    bytedata = (data - cmin) * scale + low
    return (bytedata.clip(low, high) + 0.5).astype(np.uint8)


def toimage(arr, high=255, low=0, cmin=None, cmax=None, pal=None,
            mode=None, channel_axis=None):
    data = np.asarray(arr)
    if np.iscomplexobj(data):
        raise ValueError("Cannot convert a complex-valued array.")
    shape = list(data.shape)
    valid = len(shape) == 2 or ((len(shape) == 3) and
                                ((3 in shape) or (4 in shape)))
    if not valid:
        raise ValueError("'arr' does not have a suitable array shape for "
                         "any mode.")
    if len(shape) == 2:
        shape = (shape[1], shape[0])  # columns show up first
        if mode == 'F':
            data32 = data.astype(np.float32)
            image = Image.frombytes(mode, shape, data32.tostring())
            return image
        if mode in [None, 'L', 'P']:
            bytedata = bytescale(data, high=high, low=low,
                                 cmin=cmin, cmax=cmax)
            image = Image.frombytes('L', shape, bytedata.tostring())
            if pal is not None:
                image.putpalette(np.asarray(pal, dtype=np.uint8).tostring())
                # Becomes a mode='P' automagically.
            elif mode == 'P':  # default gray-scale
                pal = (np.arange(0, 256, 1, dtype=np.uint8)[:, np.newaxis] *
                       np.ones((3,), dtype=np.uint8)[np.newaxis, :])
                image.putpalette(np.asarray(pal, dtype=np.uint8).tostring())
            return image
        if mode == '1':  # high input gives threshold for 1
            bytedata = (data > high)
            image = Image.frombytes('1', shape, bytedata.tostring())
            return image
        if cmin is None:
            cmin = np.amin(np.ravel(data))
        if cmax is None:
            cmax = np.amax(np.ravel(data))
        data = (data*1.0 - cmin)*(high - low)/(cmax - cmin) + low
        if mode == 'I':
            data32 = data.astype(np.uint32)
            image = Image.frombytes(mode, shape, data32.tostring())
        else:
            raise ValueError(_errstr)
        return image

    # if here then 3-d array with a 3 or a 4 in the shape length.
    # Check for 3 in datacube shape --- 'RGB' or 'YCbCr'
    if channel_axis is None:
        if (3 in shape):
            ca = np.flatnonzero(np.asarray(shape) == 3)[0]
        else:
            ca = np.flatnonzero(np.asarray(shape) == 4)
            if len(ca):
                ca = ca[0]
            else:
                raise ValueError("Could not find channel dimension.")
    else:
        ca = channel_axis

    numch = shape[ca]
    if numch not in [3, 4]:
        raise ValueError("Channel axis dimension is not valid.")

    bytedata = bytescale(data, high=high, low=low, cmin=cmin, cmax=cmax)
    if ca == 2:
        strdata = bytedata.tostring()
        shape = (shape[1], shape[0])
    elif ca == 1:
        strdata = np.transpose(bytedata, (0, 2, 1)).tostring()
        shape = (shape[2], shape[0])
    elif ca == 0:
        strdata = np.transpose(bytedata, (1, 2, 0)).tostring()
        shape = (shape[2], shape[1])
    if mode is None:
        if numch == 3:
            mode = 'RGB'
        else:
            mode = 'RGBA'

    if mode not in ['RGB', 'RGBA', 'YCbCr', 'CMYK']:
        raise ValueError(_errstr)

    if mode in ['RGB', 'YCbCr']:
        if numch != 3:
            raise ValueError("Invalid array shape for mode.")
    if mode in ['RGBA', 'CMYK']:
        if numch != 4:
            raise ValueError("Invalid array shape for mode.")

    # Here we know data and mode is correct
    image = Image.frombytes(mode, shape, strdata)
    return image


def randomUpdate(img):
    img = toimage(img)

    rotate = random.random() * 30 - 30
    image_rotated = img.rotate(rotate)

    enh_bri = ImageEnhance.Brightness(image_rotated)
    bright = random.random() * 0.8 + 0.6
    image_brightened = enh_bri.enhance(bright)
    # image_brightened.show()

    enh_con = ImageEnhance.Contrast(image_brightened)
    contrast = random.random() * 0.6 + 0.7
    image_contrasted = enh_con.enhance(contrast)
    # image_contrasted.show()

    enh_col = ImageEnhance.Color(image_contrasted)
    color = random.random() * 0.6 + 0.7
    image_colored = enh_col.enhance(color)

    enhance_im = np.asarray(image_colored)

    return enhance_im

label_distribution = []

pre_vote_image_name = ''
pre_vote_image_score1_cnt = 0
pre_vote_image_score2_cnt = 0
pre_vote_image_score3_cnt = 0
pre_vote_image_score4_cnt = 0
pre_vote_image_score5_cnt = 0

rating_file = open('{}/{}'.format(rating_path, rating_file_name), 'r')

lines = rating_file.readlines();
lines.pop(0)
lineIdx = 0

for line in lines:
    line = line.strip().split(',')
    lineIdx += 1
    curr_row_image_name = line[1]
    score = int(line[2])

    if pre_vote_image_name == '':
        pre_vote_image_name = curr_row_image_name

    if (curr_row_image_name != pre_vote_image_name) or (lineIdx == lines.__len__()):
        total_vote_cnt = pre_vote_image_score1_cnt + pre_vote_image_score2_cnt + pre_vote_image_score3_cnt \
                + pre_vote_image_score4_cnt + pre_vote_image_score5_cnt
        score1_ld = pre_vote_image_score1_cnt / total_vote_cnt
        score2_ld = pre_vote_image_score2_cnt / total_vote_cnt
        score3_ld = pre_vote_image_score3_cnt / total_vote_cnt
        score4_ld = pre_vote_image_score4_cnt / total_vote_cnt
        score5_ld = pre_vote_image_score5_cnt / total_vote_cnt

        im = detectFace(face_cascade, data_path, pre_vote_image_name)

        if isinstance(im, np.ndarray):
            normed_im = (im - 127.5) / 127.5

            ld = []
            ld.append(score1_ld)
            ld.append(score2_ld)
            ld.append(score3_ld)
            ld.append(score4_ld)
            ld.append(score5_ld)
            label_distribution.append([pre_vote_image_name, normed_im, ld])

        else:
            print(pre_vote_image_name + " No face detected")

        pre_vote_image_name = curr_row_image_name
        pre_vote_image_score1_cnt = 0
        pre_vote_image_score2_cnt = 0
        pre_vote_image_score3_cnt = 0
        pre_vote_image_score4_cnt = 0
        pre_vote_image_score5_cnt = 0

    if score == 1:
        pre_vote_image_score1_cnt += 1
    elif score == 2:
        pre_vote_image_score2_cnt += 1
    elif score == 3:
        pre_vote_image_score3_cnt += 1
    elif score == 4:
        pre_vote_image_score4_cnt += 1
    elif score == 5:
        pre_vote_image_score5_cnt += 1

rating_file.close()


data_split_index = int(label_distribution.__len__() - label_distribution.__len__()*0.1)

random.shuffle(label_distribution)
test_label_distribution = label_distribution[data_split_index:]
train_label_distribution = label_distribution[:data_split_index]


train_data_len = train_label_distribution.__len__()
for i in range(0, train_data_len):
    im = train_label_distribution[i][1]
    enhance_im = randomUpdate(im)
    enhance_normed_im = (enhance_im - 127.5) / 127.5

    train_label_distribution.append([pre_vote_image_name, enhance_normed_im, ld])

random.shuffle(train_label_distribution)
pickle.dump(train_label_distribution, open('{}/train_label_distribution.dat'.format(labelled_path), 'wb'))

random.shuffle(test_label_distribution)
pickle.dump(test_label_distribution, open('{}/test_label_distribution.dat'.format(labelled_path), 'wb'))
