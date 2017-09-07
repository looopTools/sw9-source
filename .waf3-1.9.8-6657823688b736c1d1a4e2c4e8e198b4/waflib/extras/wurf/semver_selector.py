#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! https://waf.io/book/index.html#_obtaining_the_waf_file

class SemverSelector(object):
	def __init__(self,semver):
		self.semver=semver
	def select_tag(self,major,tags):
		assert isinstance(major,int),"Major version is not an int"
		valid_tags=[]
		for tag in tags:
			try:
				t=self.semver.parse(tag)
				if t['major']!=major:
					continue
				valid_tags.append(tag)
			except ValueError:
				pass
		if len(valid_tags)==0:
			return None
		best_match=valid_tags[0]
		for t in valid_tags:
			if self.semver.match(best_match,"<"+t):
				best_match=t
		return best_match
	def __repr__(self):
		return"%s(%r)"%(self.__class__.__name__,self.__dict__)
