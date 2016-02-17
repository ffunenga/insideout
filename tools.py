import sys
import os


"""\
Reusable tools for insideout
"""


def filter_readme(files):
	readme = None
	_readmes = [f for f in files if f.lower().startswith('readme.')]
	if _readmes:
		_gen = (f for f in _readmes if f.lower() == 'readme.md')
		readme = next(_gen, _readmes[0])
	return readme


class OnErrorMsg:

	def __init__(self, msg):
		self.msg = msg

	def __enter__(self):
		pass

	def __exit__(self, type, value, traceback):
		if value:
			_err_msg = 'Error: %s - %s' % (self.msg, str(value))
			sys.exit(_err_msg)


class TemporaryCWD:

	def __init__(self, path):
		self.path = path

	def __enter__(self):
		self.backup_cwd = os.getcwd()
		os.chdir(self.path)

	def __exit__(self, type, value, traceback):
		os.chdir(self.backup_cwd)
		if value:
			raise
