Dataset **Power Plant Satellite Imagery Dataset** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzMyMDJfUG93ZXIgUGxhbnQgU2F0ZWxsaXRlIEltYWdlcnkgRGF0YXNldC9wb3dlci1wbGFudC1zYXRlbGxpdGUtaW1hZ2VyeS1kYXRhc2V0LURhdGFzZXROaW5qYS50YXIiLCAic2lnIjogIjFraTJGVVR6NFJ1ZHpqeVZ0T016d2ExMURZQUpIZ1hKdG1pc3JTQkFKWHc9In0=)

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
