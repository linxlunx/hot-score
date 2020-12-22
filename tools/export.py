from pymongo import MongoClient
import hashlib
import argparse
import sys
import pandas as pd
from shutil import copyfile

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='Username preference to be exported', required=True, type=str)
args = parser.parse_args()

client = MongoClient()
db = client['hotscore']

user = db.users.find_one({'username': args.username})
if not user:
    print('Cannot find user')
    sys.exit()

dataset_images = 'dataset/images'
dataset_csv = 'dataset/csv'
static_images = 'webapp/app/static'
base_table = '{}_{}'.format(args.username, hashlib.md5(args.username.encode('utf-8')).hexdigest())
arr = []
num = 1
for i in db[base_table].find({'is_labeled': True}):
    img_name = i['image'].split('/')[-1]
    rate = i['rate']
    src = '{}/{}'.format(static_images, i['image'])
    dest = '{}/{}'.format(dataset_images, img_name)
    arr.append([num, img_name, rate, ''])
    copyfile(src, dest)
    num += 1

df = pd.DataFrame(arr, columns=['Rater', 'Filename', 'Rating', 'original Rating'])
df.to_csv('{}/{}_pref.csv'.format(dataset_csv, args.username), index=False, header=True)

print('Successfully exported {} images, please proceed to next step, preparing dataset!'.format(num))

client.close()
