from app import mongo
from pymongo import InsertOne
import os
import sys


def import_base_images():
    print('=' * 20)
    print('This command will import base images')
    print('=' * 20)

    if mongo.db.base_images.count() > 0:
        print(
            "You have already imported base images!\n" 
            "If you want to reimport the data, please remove base_images collection"
        )
        sys.exit()

    base_images_dir = 'app/static/dataset'

    bulk_images = []
    images_total = 0
    for root, directory, imgs in os.walk(base_images_dir):
        clean_root = root.replace('app/static/', '')
        for img in imgs:
            if not img.endswith('.jpg'):
                continue
            full_path_img = os.path.join(clean_root, img)
            images_total += 1
            bulk_images.append(
                InsertOne({'image': full_path_img, 'is_labeled': False, 'is_skipped': False, 'rate': 0})
            )
            if len(bulk_images) == 1000:
                mongo.db.base_images.bulk_write(bulk_images)
                bulk_images = []

    if bulk_images:
        mongo.db.base_images.bulk_write(bulk_images)

    print('Successfully imported {} images to base_images collection'.format(images_total))
