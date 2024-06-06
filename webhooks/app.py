from flask import Flask

from kaggle_manager import run_notebook

app = Flask(__name__)


@app.route("/notebooks/notebook-runner")
def notebook_runner():
	run_notebook("bemnetatlaw/notebookrunner", {})
	return "", 200


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8889)

