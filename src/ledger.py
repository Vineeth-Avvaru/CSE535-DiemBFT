import sys
import collections
from logging_file import LogStuff

class SpeculatedBlock(object):
    def __init__(self, prev = None, txns = "", block_id = 0):

        if prev is not None:
            self.state_id = prev.state_id +  "#" +txns
        else:
            self.state_id = txns
        self.block_id = block_id
        self.txns = txns
        self.prev = prev
        self.next = None

    def __str__(self):
        s = "\n"
        s += "BlockID = "+ str(self.block_id) + "\n"
        s += "Txns: "+str(self.txns)+ "\n"
        s += "StateID: "+ str(self.state_id)+ "\n"
        if self.prev is not None:
            s+= "Prev Block ID: " + str(self.prev.block_id)+ "\n"
        if self.next is not None:
            s+= "Next Block ID: " + str(self.next.block_id)+ "\n"
        s+="-----------------------------------------------"
        return s



class Ledger:

    def __init__(self, file_path):
        """Mapping block id to the block object"""
        self.pending_block_map = collections.defaultdict(SpeculatedBlock)
        self.ledger_file_path = file_path
        self.commit_blocks = collections.deque()
        

    def speculate(self,prev_block_id, block_id, txns):
        
        if prev_block_id not in self.pending_block_map:
            newBlock = SpeculatedBlock(block_id = block_id, txns = txns)
            self.pending_block_map[block_id] = newBlock

        else:
            prev_block = self.pending_block_map[prev_block_id]
            newBlock = SpeculatedBlock(prev = prev_block, txns = txns, block_id = block_id)
            prev_block.next = newBlock
            self.pending_block_map[block_id] = newBlock

        return

    def pending_state(self, block_id):
        pending_state_block = self.pending_block_map[block_id]
        if not pending_state_block:
            return None
        return pending_state_block.state_id

    def commit(self, block_id, node_id):

        if block_id not in self.pending_block_map:
            return
        block = self.pending_block_map[block_id]

        if block.prev is not None:
            self.commit(block.prev.block_id, node_id)

        if block.txns:
            try:
                ledger_file = open(self.ledger_file_path + str(node_id) + ".txt", "a")
            except OSError:
                return
            LogStuff.log_to_file_param("Comitting Block to ledger with BlockID", block_id)
            self.committed_block(block_id)
            ledger_file.write(str(block))
        del self.pending_block_map[block_id]
        return

    def committed_block(self, block_id):
        self.commit_blocks.append(block_id)
        return

    def print_map(self):
        print(self.commit_blocks)
        return


    