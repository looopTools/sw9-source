#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
import shutil
import hashlib
from.error import DependencyError
class GitSemverResolver(object):
	def __init__(self,git,git_resolver,ctx,semver_selector,dependency,cwd):
		self.git=git
		self.git_resolver=git_resolver
		self.ctx=ctx
		self.semver_selector=semver_selector
		self.dependency=dependency
		self.cwd=cwd
	def resolve(self):
		path=self.git_resolver.resolve()
		assert os.path.isdir(path)
		tags=self.git.tags(cwd=path)
		tag=self.semver_selector.select_tag(major=self.dependency.major,tags=tags)
		if not tag:
			raise DependencyError(msg="No tag found for major version {}, candidates ""were {}".format(self.dependency.major,tags),dependency=self.dependency)
		repo_hash=hashlib.sha1(path.encode('utf-8')).hexdigest()[:6]
		folder_name=tag+'-'+repo_hash
		tag_path=os.path.join(self.cwd,folder_name)
		self.ctx.to_log('wurf: GitSemverResolver name {} -> {}'.format(self.dependency.name,tag_path))
		if not os.path.isdir(tag_path):
			shutil.copytree(src=path,dst=tag_path,symlinks=True)
			self.git.checkout(branch=tag,cwd=tag_path)
		self.git.pull_submodules(cwd=tag_path)
		self.dependency.git_commit=self.git.current_commit(cwd=tag_path)
		self.dependency.git_tag=tag
		return tag_path
	def __repr__(self):
		return"%s(%r)"%(self.__class__.__name__,self.__dict__)
