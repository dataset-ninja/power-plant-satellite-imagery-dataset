# https://figshare.com/articles/dataset/Power_Plant_Satellite_Imagery_Dataset/5307364

import os
import shutil
from urllib.parse import unquote, urlparse

import cv2
import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
    mkdir,
    remove_dir,
)
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "power plant satellite imagery"
    images_path = "/home/grokhi/rawdata/power-plant-satellite/uspp_naip"
    low_images_path = "/home/grokhi/rawdata/power-plant-satellite/uspp_landsat"
    masks_path = "/home/grokhi/rawdata/power-plant-satellite/annotations/binary"
    ds_name = "ds"
    batch_size = 30
    group_tag_name = "eGrid_id"
    masks_prefix = "bilabels_"
    masks_ext = ".png"
    images_ext = ".tif"

    def create_ann(image_path):
        labels = []
        tags = []

        image_name = get_file_name(image_path)

        source_value = image_name.split("_")[0]
        source = sly.Tag(source_meta, value=source_value)
        tags.append(source)

        id_data = image_name.split("_")[-3]
        group_id = sly.Tag(group_tag_meta, value=id_data)
        tags.append(group_id)

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        state_value = image_name.split("_")[2]
        state = sly.Tag(state_meta, value=state_value)
        tags.append(state)

        fuel_meta, cat_tag = category_to_tag.get(image_name.split("_")[3], (None, None))
        if fuel_meta is not None:
            tags.append(cat_tag)
            fuel = sly.Tag(fuel_meta)
        else:
            fuel = sly.Tag(unknown_meta)
        tags.append(fuel)

        if image_path.split("/")[-2] == "uspp_naip":
            mask_path = os.path.join(masks_path, masks_prefix + id_data + masks_ext)
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            mask = mask_np == 255
            ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
            for i in range(1, ret):
                obj_mask = curr_mask == i
                curr_bitmap = sly.Bitmap(obj_mask)
                if curr_bitmap.area > 10:
                    curr_label = sly.Label(curr_bitmap, obj_class)
                    labels.append(curr_label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    obj_class = sly.ObjClass("power plant", sly.Bitmap)

    group_tag_meta = sly.TagMeta(group_tag_name, sly.TagValueType.ANY_STRING)
    source_meta = sly.TagMeta("source", sly.TagValueType.ANY_STRING)
    state_meta = sly.TagMeta("state", sly.TagValueType.ANY_STRING)
    cat_meta = sly.TagMeta("category", sly.TagValueType.ANY_STRING)

    gas_meta = sly.TagMeta("gas", sly.TagValueType.NONE)
    solar_meta = sly.TagMeta("solar", sly.TagValueType.NONE)
    hydro_meta = sly.TagMeta("hydro", sly.TagValueType.NONE)
    wind_meta = sly.TagMeta("wind", sly.TagValueType.NONE)
    biomass_meta = sly.TagMeta("biomass", sly.TagValueType.NONE)
    coal_meta = sly.TagMeta("coal", sly.TagValueType.NONE)
    oil_meta = sly.TagMeta("oil", sly.TagValueType.NONE)
    geothermal_meta = sly.TagMeta("geothermal", sly.TagValueType.NONE)
    otfh_meta = sly.TagMeta("otfh", sly.TagValueType.NONE)
    nuclear_meta = sly.TagMeta("nuclear", sly.TagValueType.NONE)
    unknown_meta = sly.TagMeta("unknown", sly.TagValueType.NONE)
    ofsl_meta = sly.TagMeta("ofsl", sly.TagValueType.NONE)

    category_to_tag = {
        "BIT": [coal_meta, sly.Tag(cat_meta, value="bituminous")],
        "COG": [coal_meta, sly.Tag(cat_meta, value="coke oven gas")],
        "LIG": [coal_meta, sly.Tag(cat_meta, value="lignite")],
        "RC": [coal_meta, sly.Tag(cat_meta, value="refined coal")],
        "SGC": [coal_meta, sly.Tag(cat_meta, value="coal-derived synthetic gas")],
        "SUB": [coal_meta, sly.Tag(cat_meta, value="subbituminous coal")],
        "WC": [coal_meta, sly.Tag(cat_meta, value="waste coal")],
        "DFO": [oil_meta, sly.Tag(cat_meta, value="distillate fuel oil")],
        "JF": [oil_meta, sly.Tag(cat_meta, value="jet fuel")],
        "KER": [oil_meta, sly.Tag(cat_meta, value="kerosene")],
        "PC": [oil_meta, sly.Tag(cat_meta, value="petroleum coke")],
        "RFO": [oil_meta, sly.Tag(cat_meta, value="residual fuel oil")],
        "WO": [oil_meta, sly.Tag(cat_meta, value="waste oil")],
        "BU": [gas_meta, sly.Tag(cat_meta, value="butane gas")],
        "NG": [gas_meta, sly.Tag(cat_meta, value="natural gas")],
        "PG": [gas_meta, sly.Tag(cat_meta, value="gaseous propane")],
        "BFG": [ofsl_meta, sly.Tag(cat_meta, value="blast furnace gas")],
        "OG": [ofsl_meta, sly.Tag(cat_meta, value="other gas")],
        "TDF": [ofsl_meta, sly.Tag(cat_meta, value="tire-derived fuel")],
        "NUC": [nuclear_meta, sly.Tag(cat_meta, value="nuclear")],
        "WAT": [hydro_meta, sly.Tag(cat_meta, value="water")],
        "SUN": [solar_meta, sly.Tag(cat_meta, value="solar")],
        "WND": [wind_meta, sly.Tag(cat_meta, value="wind")],
        "GEO": [geothermal_meta, sly.Tag(cat_meta, value="geothermal")],
        "OTH": [otfh_meta, sly.Tag(cat_meta, value="other")],
        "PRG": [otfh_meta, sly.Tag(cat_meta, value="process gas")],
        "PUR": [otfh_meta, sly.Tag(cat_meta, value="purchased steam")],
        "WH": [otfh_meta, sly.Tag(cat_meta, value="waste heat")],
        "MWH": [
            otfh_meta,
            sly.Tag(cat_meta, value="electricity used for energy storage (megawatt hour)"),
        ],
        "AB": [biomass_meta, sly.Tag(cat_meta, value="agricultural byproduct")],
        "BLQ": [biomass_meta, sly.Tag(cat_meta, value="black liquor")],
        "LFG": [biomass_meta, sly.Tag(cat_meta, value="landfill gas")],
        "MSW": [biomass_meta, sly.Tag(cat_meta, value="municipal solid waste")],
        "OBG": [
            biomass_meta,
            sly.Tag(
                cat_meta, value="other biomass gas (digester gas, methane, and other biomass gases)"
            ),
        ],
        "OBL": [biomass_meta, sly.Tag(cat_meta, value="other biomass liquids")],
        "OBS": [biomass_meta, sly.Tag(cat_meta, value="other biomass solid")],
        "SLW": [biomass_meta, sly.Tag(cat_meta, value="sludge waste")],
        "WDL": [biomass_meta, sly.Tag(cat_meta, value="wood, wood waste liquid")],
        "WDS": [biomass_meta, sly.Tag(cat_meta, value="wood, wood waste solid")],
    }

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[obj_class],
        tag_metas=[
            group_tag_meta,
            source_meta,
            state_meta,
            cat_meta,
            gas_meta,
            solar_meta,
            hydro_meta,
            wind_meta,
            biomass_meta,
            coal_meta,
            oil_meta,
            geothermal_meta,
            otfh_meta,
            nuclear_meta,
            unknown_meta,
            ofsl_meta,
        ],
    )
    api.project.update_meta(project.id, meta.to_json())
    api.project.images_grouping(id=project.id, enable=True, tag_name=group_tag_name)

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    for curr_images_path in [low_images_path, images_path]:
        images_names = [
            im_name
            for im_name in os.listdir(curr_images_path)
            if get_file_ext(im_name) == images_ext
        ]

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = [
                os.path.join(curr_images_path, image_name) for image_name in img_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(img_names_batch))
    return project
