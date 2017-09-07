#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import os
import re
class Git(object):
	def __init__(self,git_binary,ctx):
		self.git_binary=git_binary
		self.ctx=ctx
	def cmd_and_log(self,*args,**kwargs):
		args=[self.git_binary]+list(args)
		return cmd_and_log(args,**kwargs)
	def version(self):
		args=[self.git_binary,'version']
		output=self.ctx.cmd_and_log(args).strip()
		int_list=[int(s)for s in re.findall('\\d+',output)]
		return tuple(int_list)
	def current_commit(self,cwd):
		args=[self.git_binary,'rev-parse','HEAD']
		output=self.ctx.cmd_and_log(args,cwd=cwd).strip()
		return output
	def clone(self,repository,directory,cwd):
		args=[self.git_binary,'clone',repository,directory]
		self.ctx.cmd_and_log(args,cwd=cwd)
	def pull(self,cwd):
		args=[self.git_binary,'pull']
		self.ctx.cmd_and_log(args,cwd=cwd)
	def branch(self,cwd):
		args=[self.git_binary,'branch']
		o=self.ctx.cmd_and_log(args,cwd=cwd)
		branch=o.split('\n')
		branch=[b for b in branch if b!='']
		current=''
		others=[]
		for b in branch:
			if b.startswith('*'):
				current=b[1:].strip()
			else:
				others.append(b)
		if current=='':
			self.ctx.fatal('Failed to locate current branch')
		return current,others
	def current_branch(self,cwd):
		current,_=self.branch(cwd=cwd)
		return current
	def is_detached_head(self,cwd):
		current,_=self.branch(cwd=cwd)
		return current.startswith('(')and current.endswith(')')
	def checkout(self,branch,cwd):
		args=[self.git_binary,'checkout',branch]
		self.ctx.cmd_and_log(args,cwd=cwd)
	def has_submodules(ctx,cwd):
		return os.path.isfile(os.path.join(cwd,'.gitmodules'))
	def sync_submodules(self,cwd):
		args=[self.git_binary,'submodule','sync']
		self.ctx.cmd_and_log(args,cwd=cwd)
	def init_submodules(self,cwd):
		args=[self.git_binary,'submodule','init']
		self.ctx.cmd_and_log(args,cwd=cwd)
	def update_submodules(self,cwd):
		args=[self.git_binary,'submodule','update']
		self.ctx.cmd_and_log(args,cwd=cwd)
	def pull_submodules(self,cwd):
		if self.has_submodules(cwd=cwd):
			self.sync_submodules(cwd=cwd)
			self.init_submodules(cwd=cwd)
			self.update_submodules(cwd=cwd)
	def tags(self,cwd):
		args=[self.git_binary,'tag','-l']
		output=self.ctx.cmd_and_log(args,cwd=cwd)
		tags=output.split('\n')
		return[t for t in tags if t!='']
	def remote_origin_url(self,cwd):
		args=[self.git_binary,'config','--get','remote.origin.url']
		output=self.ctx.cmd_and_log(args,cwd=cwd)
		return output.strip()
