Dataset **Power Plant Satellite Imagery Dataset** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://www.dropbox.com/scl/fi/vmgrhs065lczf17hm6fn2/power-plant-satellite-imagery-dataset-DatasetNinja.tar?rlkey=ka5vygxcx5l2pxe5rwyj681dh&dl=1)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Power Plant Satellite Imagery Dataset', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be downloaded here:

- [Download All](https://figshare.com/ndownloader/articles/5307364/versions/1)
- [eGRID2014_Data_v2_US_EPA_with_imagery_list_for_power_plants.xlsx](https://figshare.com/ndownloader/files/9097597)
- [Power Plant Satellite Imagery Dataset Overview.pdf](https://figshare.com/ndownloader/files/9104302)
