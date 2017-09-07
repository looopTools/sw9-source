#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
import json
class ExistingTagResolver(object):
	def __init__(self,ctx,dependency,semver_selector,tag_database,resolver,cwd):
		self.ctx=ctx
		self.dependency=dependency
		self.semver_selector=semver_selector
		self.tag_database=tag_database
		self.resolver=resolver
		self.cwd=cwd
	def resolve(self):
		tags=self.__load_tag_file()
		path=self.__resolve_path(tags=tags)
		if path:
			return path
		path=self.resolver.resolve()
		if not path:
			return None
		assert os.path.isdir(path)
		if'git_tag'in self.dependency:
			tags[self.dependency.git_tag]=path
		else:
			raise DependencyError(msg="No git tag available",dependency=dependency)
		self.__store_tag_file(tags=tags)
		return path
	def __load_tag_file(self):
		tag_path=os.path.join(self.cwd,self.dependency.name+'.tags.json')
		if not os.path.isfile(tag_path):
			return{}
		with open(tag_path,'r')as tag_file:
			return json.load(tag_file)
	def __store_tag_file(self,tags):
		tag_path=os.path.join(self.cwd,self.dependency.name+'.tags.json')
		with open(tag_path,'w')as tag_file:
			return json.dump(tags,tag_file,indent=4)
	def __resolve_path(self,tags):
		project_tags=self.tag_database.project_tags(self.dependency.name)
		if not project_tags:
			return None
		most_recent=self.semver_selector.select_tag(self.dependency.major,project_tags)
		if most_recent not in tags:
			return None
		path=tags[most_recent]
		if not os.path.isdir(path):
			self.ctx.to_log("resolve: {} {} contained invalid path {} for tag {}""- removing it".format(self.dependency.name,tags,path,most_recent))
			del tags[most_recent]
			return None
		else:
			self.ctx.to_log('resolve: ExistingTagResolver name {} -> {}'.format(self.dependency.name,path))
			return path
	def __repr__(self):
		return"%s(%r)"%(self.__class__.__name__,self.__dict__)
