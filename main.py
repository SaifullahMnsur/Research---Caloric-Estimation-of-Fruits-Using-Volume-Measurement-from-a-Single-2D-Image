import os

from ultralytics import YOLO
from ultralytics.engine.results import Boxes, Masks

import utils.data as dt
from utils.math import Estimator


def main():
    model_name = "Models\yolov8x-seg.pt"
    model = YOLO(model=model_name)
    
    # image on which test will be performed
    image_name = 'apple_96gm'
    img_paths: list[str] = [f'Images\\{image_name}.jpg']

    # get the prediction on
    results: any = model.predict(source=img_paths, retina_masks=True, conf=0.8)

    # setup the folder to store output data
    save_dir: str = os.getcwd() + '\Outputs\\'
    save_dir: str = dt.create_folder(save_dir, image_name)

    # Process results generator
    for i, result in enumerate(results):
        boxes: Boxes = result.boxes  # Boxes object for bounding box outputs
        masks: Masks = result.masks  # Masks object for segmentation masks outputs

        # save to disk
        result.save(filename=f"{save_dir}\\predicted_image_{i}.jpg", )

        # save json data
        dt.save_json(result.tojson(), save_dir, i)

        # separate the values of each point
        coord = masks.xy[0]
        x, y = [], []
        for xx, yy in coord:
            x.append(xx)
            y.append(yy)

        # Collected from various references
        density = 75/100  # weight density of apple
        cphg = 52/100  # calorie per hundred grams

        # Manually calculated values
        ppcm = 180  # pixel per cm for the performed test
        fov_angle = 16.72659694010  # angle of field of view of the apple

        # create estimator class
        estimator = Estimator(density, ppcm, cphg)
        # call to estimate the volume, weight and calorie
        estimator.estimate(x, y, fov_angle, save_dir)

        output = f"Density: {density}/cm^2\n"
        output += f"Average Pixel per cm: {ppcm:.2f}\n"
        output += f"Average calorie per hundred grams: {cphg*100} kcal\n"

        output += f"Predicted item: {result.names[int(boxes.cls[0])]}\n"
        output += f"Confidence: {(boxes.conf[0]*100):.2f}%\n"

        output += f"Final Average volume: {estimator.final_volume:.2f} cm^3\n"
        output += f"Final weight: {estimator.weight:.2f} grams\n"
        output += f"Final calorie: {estimator.calorie:.2f} calorie\n"

        print(output)
        dt.save_txt(output, save_dir, i)


if __name__ == '__main__':
    main()
