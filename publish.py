import os
import re
from shutil import rmtree


pardir = os.path.realpath(os.path.dirname(__file__))


def get_next_version(string):
	new = str(int(string.replace(".", "")) + 1)
	new = "0"*(3-len(new)) + new
	return new[0] + "." + new[1] + "." + new[2]


with open(os.path.join(pardir, "setup.py"), "r") as orig:
	text = orig.read()
	prev_name = re.search(r"name ?= ?[\"\'].*[\"\'],", text)
	name_text = text[prev_name.start():prev_name.end()]
	name = re.search(r"[\"\'].*[\"\']", name_text)
	module = text[name.start()+1 + prev_name.start():name.end()-1 + prev_name.start()]
	version = re.search(r"\d+\.\d+\.\d+", text)
	pos_start = version.start()
	pos_end = version.end()
	text = text[:pos_start] + get_next_version(text[pos_start:pos_end]) + text[pos_end:]
	with open(os.path.join(pardir, "setup.py"), "w") as f:
		f.write(text)

os.chdir(pardir)
os.system("python setup.py sdist bdist_wheel")
_ = os.system("twine upload dist/*")
rmtree(os.path.join(pardir, "build"))
rmtree(os.path.join(pardir, "dist"))
rmtree(os.path.join(pardir, f"{module}.egg-info"))
