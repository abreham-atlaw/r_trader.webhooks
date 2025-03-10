from flask import Flask

import time
import sys
import os

from api.kaggle_manager import run_notebook


app = Flask(__name__)


@app.route("/notebooks/notebook-runner")
def notebook_runner():
	from kaggle.rest import ApiException
	try:
		run_notebook("bemnetatlaw/notebookrunner", {})
		return "", 200
	except ApiException as ex:
		if ex.status in [429, 404]:
			print(f"Rate limited[{ex.status}]. Waiting 2 seconds...")
			time.sleep(2)
			return notebook_runner()
		else:
			raise ex
