#Convert annotation format into YOLOv8 format
import os
import sys
import imageio.v2 as io

dataset_path = r'..\dataset\Task1_Image_detection'
train_labels_path = os.path.join(dataset_path, rf'train\labels_original')
valid_labels_path = os.path.join(dataset_path, rf'valid\labels_original')
test_labels_path = os.path.join(dataset_path, rf'test\labels_original')
train_images_path = os.path.join(dataset_path, rf'train\images')
valid_images_path = os.path.join(dataset_path, rf'valid\images')
test_images_path = os.path.join(dataset_path, rf'test\images')

def generate_new_labels(label_path, new_label_file_path, images_path):
    label_files = os.listdir(label_path)
    for label_file in label_files:
        image = io.imread(os.path.join(images_path, f'{label_file.split(sep=".")[0]}.jpg'))
        image_height, image_width = image.shape[0], image.shape[1]
        with open(os.path.join(label_path, label_file), 'r') as f:
            labels = [label.strip() for label in f.readlines()]
            for annot in (labels):
                #bbox_left, bbox_top, bbox_width, bbox_height, score, object_category, truncation, occlusion = annot.split(sep=',') #String format
                bbox_left, bbox_top, bbox_width, bbox_height, score, object_category, truncation, occlusion = [int(x) for x in annot.split(sep=',')] #Int format
                if (object_category == 0 or object_category == 11): #Filter the ignore and another class
                    continue
                with open(os.path.join(new_label_file_path, label_file), 'a+') as archivo:
                    archivo.write(f'{object_category-1} {(bbox_left + bbox_width//2)/image_width} {(bbox_top + bbox_height//2)/image_height} {bbox_width/image_width} {bbox_height/image_height}\n')

def main():
    new_train_label_file_path = os.path.join(dataset_path, rf'train\labels')
    new_valid_label_file_path = os.path.join(dataset_path, rf'valid\labels')
    new_test_label_file_path = os.path.join(dataset_path, rf'test\labels')

    generate_new_labels(train_labels_path, new_train_label_file_path, train_images_path)
    generate_new_labels(valid_labels_path, new_valid_label_file_path, valid_images_path)
    generate_new_labels(test_labels_path, new_test_label_file_path, test_images_path)


if __name__ == '__main__':
    main()