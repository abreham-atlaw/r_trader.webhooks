import os
import time
import json

from kaggle import ApiClient
from kaggle.configuration import Configuration

import config

os.environ["KAGGLE_USERNAME"] = config.KAGGLE_USERNAME
os.environ["KAGGLE_KEY"] = config.KAGGLE_KEY
from kaggle.api.kaggle_api_extended import KaggleApi


import logging

logging.basicConfig(level=logging.DEBUG)


def __create_api():
	kaggle_config = Configuration()
	kaggle_config.proxy = config.KAGGLE_NETWORK_PROXY
	api = KaggleApi(ApiClient(kaggle_config))
	api.authenticate()
	return api


def __clean(path):
	os.system(f"rm -fr \"{path}\"")

def __pull_notebook(api, kernel: str) -> str:
	pull_path = f".notebook-{kernel}".replace("/", "-")
	__clean(pull_path)
	os.mkdir(pull_path)
	api.kernels_pull(kernel, pull_path, metadata=True)
	return pull_path


def __update_meta(meta_data, path):
	meta_data["enable_internet"] = True
	meta_path = os.path.join(path, "kernel-metadata.json")
	with open(meta_path, "r") as file:
		meta = json.load(file)

	meta.update(meta_data)

	with open(meta_path, "w") as file:
		json.dump(meta, file)


def run_notebook(kernel, meta_data):
	path = __pull_notebook(api, kernel)
	try:
		__update_meta(meta_data, path)
		api.kernels_push(path)
	finally:
		__clean(path)


api = __create_api()
