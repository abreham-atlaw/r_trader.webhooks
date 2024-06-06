import os
import time
import json

os.environ["KAGGLE_USERNAME"] = "bemnetatlaw"
os.environ["KAGGLE_KEY"] = "0c9625e07a328c93a9c27fb1dda49f1a"
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

def __clean(path):
	os.system(f"rm -fr \"{path}\"")

def __pull_notebook(api, kernel: str) -> str:
	pull_path = f".notebook-{kernel}".replace("/", "-")
	__clean(pull_path)
	os.mkdir(pull_path)
	api.kernels_pull(kernel, pull_path, metadata=True)
	return pull_path

def __update_meta(meta_data, path):
	if len(meta_data) == 0:
		return

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

