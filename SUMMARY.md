**Power Plant Satellite Imagery Dataset (US Power Plants NAIP/LANDSAT8)** is a dataset for instance segmentation, semantic segmentation, object detection, and classification tasks. It is used in the energy industry. 

The dataset consists of 8908 images with 5185 labeled objects belonging to 1 single class (*power plant*).

Images in the Power Plant Satellite Imagery Dataset dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. There are 4454 (50% of the total) unlabeled images (i.e. without annotations). There are no pre-defined <i>train/val/test</i> splits in the dataset. Alternatively, the dataset could be split into 12 fuel types: ***gas*** (2320 images), ***solar*** (1700 images), ***hydro*** (1376 images), ***wind*** (914 images), ***biomass*** (854 images), ***coal*** (714 images), ***oil*** (652 images), ***geothermal*** (118 images), ***otfh*** (106 images), ***nuclear*** (92 images), ***unknown*** (38 images), and ***ofsl*** (24 images). Additionally, every image has information about its ***source***, ***eGrid_id***, ***state***, and ***category***. The dataset was released in 2017 by the Duke University, USA.

Here are the visualized examples for the classes:

[Dataset classes](https://github.com/dataset-ninja/power-plant-satellite-imagery-dataset/raw/main/visualizations/classes_preview.webm)
