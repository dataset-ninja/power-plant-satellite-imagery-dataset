The authors present the **Power Plant Satellite Imagery Dataset (US Power Plants NAIP/LANDSAT8)**, comprising 4,454 instances of satellite imagery capturing mainland power plants in the United States. The dataset offers both high resolution (1m) and medium resolution (30m data pansharpened to 15m) for detection and segmentation tasks. The data sources include NAIP for high-resolution imagery, Landsat8 for medium-resolution imagery, and EPA EGRID documents for latitude and longitude locations

<img src="https://github.com/dataset-ninja/power-plant-satellite-imagery-dataset/assets/78355358/19ed20f5-9f3a-40e8-8493-d2ade92403e5" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Example of NAIP/LANDSAT8 images and corresponding masks.</span>


The dataset was created by the authors, who are part of the Duke University Electricity Access Team within the Duke Data+ Program. The primary objective is to detect electricity access in developing countries using aerial imagery. Power plants were specifically chosen as indicators due to their clear association with electricity access and their visibility in globally-available 30m resolution satellite imagery.

To ensure annotation accuracy, the authors employed a two-fold approach. Firstly, they conducted a visual inspection of all submissions, rejecting annotations that were blatantly incorrect. Secondly, multiple annotators reviewed each image, aiming to mitigate the impact of human error. The confidence in each pixel was established by considering the number of annotators including it in their annotations. Subsequently, a threshold was applied to create final binary labels.

The dataset offers various possibilities for data usage. The authors have previously explored image segmentation through pixel-based classification. It can also be leveraged for multi-class training, allowing users to classify by energy type. For those interested in deep learning problems, the dataset is particularly suitable for implementing Fully Convolutional Networks (FCN). Additionally, researchers in economics, statistics, energy, and the environment may find valuable insights in the energy type, capacity, and emission data provided by the dataset.

## Data description

**NAIP Imagery (uspp_naip)**

- High-resolution power plant images (1m/pixel, ~1115x1115 pix, ~5M/ea).
- Utilized for ground truth gathering (outline of power plants) with human effort.
- Acts as a reference for resolving confusions in lower resolutions.

**Landsat8 Imagery (uspp_landsat)**

- Medium-resolution power plant images (15m/pixel, ~75x75 pix, ~17K/ea).
- Intended for machine learning practice.

Fuel types:

| Fuel Category |Description (the primary fuel is derived from)|Count |
| --------- |-------|---------|
|GAS|gas|1160|
|SOLAR|solar power|850|
|HYDRO|hydro power|688|
|WIND|wind power|457|
|BIOMASS|biomass sources|427|
|COAL|coal|357|
|OIL|oil|326|
|GEOTHERMAL|geothermal power|59|
|OTHF|waste heat/unknown/purchased |53|
|NUCLEAR|nuclear|46|
|UNKNOWN|not on the document|19|
|OFSL|another fossil fuel|12|
|__Total__|__-__|__4454__|
