#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import json
class TagDatabase(object):
	def __init__(self,ctx):
		self.ctx=ctx
		self.tags=None
	def download_tags(self):
		url="http://files.steinwurf.com/registry/tags.json"
		try:
			from urllib.request import urlopen,Request
		except ImportError:
			from urllib2 import urlopen,Request
		try:
			req=Request(url)
			response=urlopen(req)
			tags_json=response.read()
			self.ctx.to_log("Tags downloaded. File size: {}\n".format(len(tags_json)))
			self.tags=json.loads(tags_json)
		except Exception as e:
			self.tags={}
			self.ctx.logger.debug("Could not fetch tags.json from: {}".format(url),exc_info=True)
	def project_tags(self,project_name):
		if self.tags is None:
			self.download_tags()
		if project_name in self.tags:
			self.ctx.to_log("Registered tags for {}:\n{}".format(project_name,self.tags[project_name]))
			return self.tags[project_name]
		else:
			self.ctx.to_log("No registered tags for {}.".format(project_name))
			return None
