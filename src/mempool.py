from hashing import Hashing
from collections import deque
from logging_file import LogStuff

class Mempool:
	def __init__(self):
		self.transaction_list = deque()

	def insert(self, transaction_obj):
		self.transaction_list.append(transaction_obj['transaction_id'])

	def update_state(self, transaction_id, state=None):

		try:
			self.transaction_list.remove(transaction_id)
		except ValueError:
			return
		except IndexError:
			return

	def get_transactions(self):
		return self.transaction_list.popleft()