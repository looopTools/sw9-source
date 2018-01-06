#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import hashlib
import os
import shutil
class GitCheckoutResolver(object):
	def __init__(self,git,git_resolver,ctx,dependency,checkout,cwd):
		self.git=git
		self.git_resolver=git_resolver
		self.ctx=ctx
		self.dependency=dependency
		self.checkout=checkout
		self.cwd=cwd
	def resolve(self):
		path=self.git_resolver.resolve()
		assert os.path.isdir(path)
		if self.git.current_branch(cwd=path)==self.checkout:
			return path
		if self.git.current_commit(cwd=path)==self.checkout:
			return path
		repo_hash=hashlib.sha1(path.encode('utf-8')).hexdigest()[:6]
		folder_name=self.checkout+'-'+repo_hash
		checkout_path=os.path.join(self.cwd,folder_name)
		self.ctx.to_log('wurf: GitCheckoutResolver name {} -> {}'.format(self.dependency.name,checkout_path))
		if not os.path.isdir(checkout_path):
			try:
				shutil.copytree(src=path,dst=checkout_path,symlinks=True)
				self.git.checkout(branch=self.checkout,cwd=checkout_path)
			except:
				def onerror(func,path,exc_info):
					import stat
					if not os.access(path,os.W_OK):
						os.chmod(path,stat.S_IWUSR)
						func(path)
					else:
						raise
				shutil.rmtree(checkout_path,onerror=onerror)
				raise
		else:
			if not self.git.is_detached_head(cwd=checkout_path):
				self.git.pull(cwd=checkout_path)
		self.git.pull_submodules(cwd=checkout_path)
		self.dependency.git_commit=self.git.current_commit(cwd=checkout_path)
		return checkout_path
	def __repr__(self):
		return"%s(%r)"%(self.__class__.__name__,self.__dict__)
