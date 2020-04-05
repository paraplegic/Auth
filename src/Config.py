import os
from yaml import load, dump

try:
  from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
  from yaml import Loader, Dumper

class Config():

	def __init__( self, path ):
		if path:
			self.path = path
		else:
			self.path = None
		self.parse()
		self.name = os.path.basename( self.path ).split('.')[0]

	def parse(self):
		try:
			with open(self.path,'r') as cfg:
			 self.config = load(cfg, Loader=Loader)

		except Exception as e:
			print(e)

	def describes(self, config):
		for t in self.objects():
			if t == config:
				return self.config[t]
		return None

	def dump(self):
		print(dump(self.config))

	def objects(self):
		return self.config.keys()

	def object(self, object):
		return self.config[object]

	def attrs(self, obj):
		return self.config[obj].keys()

	def attr(self, obj, att ):
		return self.config[obj][att]


if __name__ == '__main__':

	import sys
	if len(sys.argv) > 1:
		cfg = Config(sys.argv[1])
	else:
		print( 'no argument' )
		exit(1)

	print(cfg.name)
	print(cfg.config.keys())
	## cfg.dump()
