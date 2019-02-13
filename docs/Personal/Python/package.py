#! /usr/bin/python
"""
title				:	package.py
description 		:	This file will be the to be responsible
						in getting the file from artifactory/svn going to the webservers
author				:	release management team
						DL.IT.CDRelease@bayviewtechnology.com
python version		:	2.7 / 3.5

(c) 2018, Glen Garing
"""
import argsparse
import os
import logging

svn_url = ""
artifactory_url = ""
svn_user = ""
artifactory_user = ""
artifactory_password = ""
package_version = ""
local_dir = '/var/www/html'

class PackageError(Exception):
	"""
	Package is not present
	"""
	pass


class deployment_package:

	def __init__(self, svn_url=none, artifactory_url=none, svn_user=none, svn_password=none,
		artifactory_user=none, artifactory_password=none, package_version):
		self.svn_url = svn_url
		self.artifactory_url = artifactory_url
		self.svn_user = svn_user
		self.svn_password = svn_password
		self.artifactory_user = artifactory_user
		self.artifactory_password = artifactory_password
		self.package_version = package_version
		self.local_dir = local_dir

	def _if_present(self):
		try:
			if os.path.join(self.local_dir, self.package_version):
				msg = 'Version {0} is existing in {1}'.format(self.package_version, self.local_dir)
				logger.debug(msg)
		except:
			msg = 'Version {0} is not existing in {1}'.format(self.local_dir, self.package_version)
			logger.fatal

class import_package:

	 def check_package:
	 	

	def __init__(self, )

	@classmethod
	def change_dir(cls, pkg_dir)
	deployment_package.pkg_dir = pkg_dir