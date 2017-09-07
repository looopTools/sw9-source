#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
import sys
class CreateSymlinkResolver(object):
	def __init__(self,resolver,dependency,symlinks_path,ctx):
		self.resolver=resolver
		self.dependency=dependency
		self.symlinks_path=symlinks_path
		self.ctx=ctx
		assert os.path.isabs(self.symlinks_path)
	def resolve(self):
		path=self.resolver.resolve()
		if not path:
			return path
		link_path=os.path.join(self.symlinks_path,self.dependency.name)
		if os.path.exists(link_path):
			if os.path.realpath(link_path)==os.path.realpath(path):
				self.dependency.is_symlink=True
				self.dependency.real_path=os.path.realpath(path)
				return link_path
		os_symlink=getattr(os,"symlink",None)
		if not callable(os_symlink)and sys.platform=='win32':
			def symlink_windows(target,link_path):
				cmd='mklink /J "{}" "{}"'.format(link_path.replace('/','\\'),target.replace('/','\\'))
				self.ctx.cmd_and_log(cmd)
			os_symlink=symlink_windows
		try:
			self.ctx.to_log('wurf: CreateSymlinkResolver {} -> {}'.format(link_path,path))
			if os.path.lexists(link_path):
				if sys.platform=='win32':
					os.rmdir(link_path)
				else:
					os.unlink(link_path)
			os_symlink(path,link_path)
		except Exception as e:
			self.ctx.logger.debug("Symlink creation failed for: {}".format(self.dependency.name),exc_info=True)
			return path
		self.dependency.is_symlink=True
		self.dependency.real_path=path
		return link_path
	def __repr__(self):
		return"%s(%r)"%(self.__class__.__name__,self.__dict__)
