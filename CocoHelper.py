import os

import numpy as np
from pycocotools.coco import COCO
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt


class CocoHelper(COCO):
    # load coco data
    def __init__(self, annotation_file, images_path):
        super().__init__(annotation_file)
        self.ids = []
        self.image_list = []
        self.coco_classes = []
        self.images_path = images_path

    def load_coco_images_list(self, image_begin_index=0, image_end_index=100):
        # get all image index info
        self.ids = list(sorted(self.imgs.keys()))
        print("number of images: {}".format(len(self.ids)))

        # get all coco class labels
        self.coco_classes = dict([(v["id"], v["name"]) for k, v in self.cats.items()])

        if image_end_index == 0 or image_end_index > len(self.ids):
            image_end_index = len(self.ids)

        image_list = []
        # Traverse the first N pictures
        for img_id in self.ids[image_begin_index:image_end_index]:
            # get image file name
            image_name = self.loadImgs(img_id)[0]['file_name']
            image_list.append({
                'image_path': os.path.join(self.images_path, image_name),
                'image_id': img_id
            })

        return image_list

    def image_pillow(self, image_id):
        # get image file name
        path = self.loadImgs(image_id)[0]['file_name']
        # if we do not convert image to ‘RGB’ , the image may have 4 channels ,such as  'RGBA'
        img = Image.open(os.path.join(self.images_path, path)).convert('RGB')
        return img

    def image_show(self, image_id):
        # show image
        plt.imshow(self.image_pillow(image_id))
        plt.show()

    def image_bbox_pillow(self, image_id):
        # get all annotation index  of the corresponding image ID
        ann_ids = self.getAnnIds(imgIds=image_id)
        # according annotation index get all of label information
        targets = self.loadAnns(ann_ids)
        # get image file name
        path = self.loadImgs(image_id)[0]['file_name']
        # if we do not convert image to ‘RGB’ , the image may have 4 channels ,such as  'RGBA'
        img = Image.open(os.path.join(self.images_path, path)).convert('RGB')
        draw = ImageDraw.Draw(img)
        # draw box to image
        for target in targets:
            x, y, w, h = target["bbox"]
            x1, y1, x2, y2 = x, y, int(x + w), int(y + h)
            draw.rectangle((x1, y1, x2, y2))
            draw.text((x1, y1), self.coco_classes[target["category_id"]])
        return img

    def image_bbox_show(self, image_id):
        # show image
        plt.imshow(self.image_bbox_pillow(image_id))
        plt.show()

    def image_keypoint_pillow(self, image_id):
        # get all annotation index  of the corresponding image ID
        ann_ids = self.getAnnIds(imgIds=image_id)
        # according annotation index get all of label information
        targets = self.loadAnns(ann_ids)
        # get image file name
        path = self.loadImgs(image_id)[0]['file_name']
        # if we do not convert image to ‘RGB’ , the image may have 4 channels ,such as  'RGBA'
        img = Image.open(os.path.join(self.images_path, path)).convert('RGB')
        draw = ImageDraw.Draw(img)
        # draw keypoint to image
        targets = self.loadAnns(ann_ids)

        for target in targets:
            keypoints_info = np.array(target["keypoints"]).reshape([-1, 3])
            visible = keypoints_info[:, 2]
            keypoints = keypoints_info[:, :2]
            for i in range(len(keypoints)):
                if visible[i] != 2:
                    continue
                x, y = keypoints[i]
                draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=250)
        return img


if __name__ == '__main__':
    coco_helper = CocoHelper(annotation_file='', images_path='')
