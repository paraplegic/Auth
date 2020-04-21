import Model
import hashlib

class User:

	def __init__(self,id):
		pass

	def hash(self,blob):
		hash = hashlib.md5()
		hash.update(blob.encode())
		return hash.hexdigest()

	def lookup(self, key):
		pass

	def validate(self,key,pass):
		pass

