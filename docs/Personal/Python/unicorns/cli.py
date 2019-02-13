from __future__ import absolute_import
import os
import sys

class BuildException:
	pass

def build():
	print('Passing build()')
	current_dir = os.path.abspath(os.getcwd())
	print(current_dir)
	print(sys.version)

def second_build():
	print('Passing second_build()')

def main():
	build()
	second_build()