from flask import Flask

import time

from kaggle_manager import run_notebook

app = Flask(__name__)


@app.route("/notebooks/notebook-runner")
def notebook_runner():
	from kaggle.rest import ApiException
	try:
		run_notebook("bemnetatlaw/notebookrunner", {})
		return "", 200
	except ApiException as ex:
		if ex.status in [429, 404]:
			print(f"Rate limited[{ex.status}]. Waiting 30 seconds...")
			time.sleep(30)
			return notebook_runner()
		else:
			raise ex


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8889)

