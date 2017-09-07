#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

import hashlib
import json
import collections
import pprint
class Dependency(object):
	def __init__(self,**kwargs):
		assert"sha1"not in kwargs
		if'recurse'not in kwargs:
			kwargs['recurse']=True
		if'optional'not in kwargs:
			kwargs['optional']=False
		if'internal'not in kwargs:
			kwargs['internal']=False
		hash_attributes=kwargs.copy()
		hash_attributes.pop('optional',None)
		hash_attributes.pop('internal',None)
		s=json.dumps(hash_attributes,sort_keys=True)
		sha1=hashlib.sha1(s.encode('utf-8')).hexdigest()
		object.__setattr__(self,'info',kwargs)
		self.info['sha1']=sha1
		self.info['hash']=None
		object.__setattr__(self,'read_write',dict())
		object.__setattr__(self,'audit',list())
		self.error_messages=[]
	def rewrite(self,attribute,value,reason):
		if value==None:
			self.__delete(attribute=attribute,reason=reason)
		elif attribute not in self.info:
			self.__create(attribute=attribute,value=value,reason=reason)
		else:
			self.__modify(attribute=attribute,value=value,reason=reason)
	def __delete(self,attribute,reason):
		if attribute not in self.info:
			raise AttributeError("Cannot delete non existing attribute {}".format(attribute))
		audit='Deleting "{}". Reason: {}'.format(attribute,reason)
		del self.info[attribute]
		self.audit.append(audit)
	def __create(self,attribute,value,reason):
		audit='Creating "{}" value "{}". Reason: {}'.format(attribute,value,reason)
		self.audit.append(audit)
		self.info[attribute]=value
	def __modify(self,attribute,value,reason):
		audit='Modifying "{}" from "{}" to "{}". Reason: {}'.format(attribute,self.info[attribute],value,reason)
		self.audit.append(audit)
		self.info[attribute]=value
	def __getattr__(self,attribute):
		if attribute in self.info:
			return self.info[attribute]
		elif attribute in self.read_write:
			return self.read_write[attribute]
		else:
			return None
	def __setattr__(self,attribute,value):
		if attribute in self.info:
			raise AttributeError("Attribute {} read-only.".format(attribute))
		else:
			self.read_write[attribute]=value
	def __contains__(self,attribute):
		return(attribute in self.info)or(attribute in self.read_write)
	def __str__(self):
		return"Dependency info:\n{}\nread_write: {}\naudit: {}".format(pprint.pformat(self.info,indent=2),pprint.pformat(self.read_write,indent=2),pprint.pformat(self.audit,indent=2))
	def __hash__(self):
		if not self.info['hash']:
			self.info['hash']=hash(self.info['sha1'])
		return self.info['hash']
