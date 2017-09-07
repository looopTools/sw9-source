#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
import hashlib
class GitResolver(object):
	def __init__(self,git,ctx,dependency,git_url_rewriter,source,cwd):
		self.git=git
		self.ctx=ctx
		self.dependency=dependency
		self.git_url_rewriter=git_url_rewriter
		self.source=source
		self.cwd=cwd
	def resolve(self):
		repo_url=self.git_url_rewriter.rewrite_url(self.source)
		self.dependency.current_source=repo_url
		repo_hash=hashlib.sha1(repo_url.encode('utf-8')).hexdigest()[:6]
		folder_name='master-'+repo_hash
		master_path=os.path.join(self.cwd,folder_name)
		if not os.path.isdir(master_path):
			self.git.clone(repository=repo_url,directory=folder_name,cwd=self.cwd)
		else:
			try:
				self.git.pull(cwd=master_path)
			except Exception as e:
				self.ctx.to_log('Exception when executing git pull:')
				self.ctx.to_log(e)
		assert os.path.isdir(master_path),"We should have a valid path here!"
		self.git.pull_submodules(cwd=master_path)
		return master_path
	def __repr__(self):
		return"%s(%r)"%(self.__class__.__name__,self.__dict__)
