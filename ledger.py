import sys
import collections

class SpeculatedBlock(object):
    def __init__(self, prev = None, txns = "", block_id = 0):
        #TODO: fix state_id based on hash function
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
        

    def speculate(self,prev_block_id, block_id, txns):
        print("Speculate: " , prev_block_id , block_id , txns)
        
        if prev_block_id not in self.pending_block_map:
            #TODO: Ask the TA about commited state block
            # commited_state_block = self.committed_block(prev_block_id)
            # if not commited_state_block:
                # return
            print("No prev block")
            newBlock = SpeculatedBlock(block_id = block_id, txns = txns)
            self.pending_block_map[block_id] = newBlock

        else:
            prev_block = self.pending_block_map[prev_block_id]
            print("prev block is there")
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

        #TODO: Prune neglected branches, ask TA how to commit blocks

        if block_id not in self.pending_block_map:
            print("Block id not found in pending ledger state")
            return
        block = self.pending_block_map[block_id]
        if block.prev is not None:
            self.commit(block.prev.block_id, node_id)
        try:
            ledger_file = open(self.ledger_file_path + str(node_id) + ".txt", "a")
        except OSError:
            print("Error in reading file: ", self.ledger_file_path + str(node_id) + ".txt")
            print(OSError)
            return
        ledger_file.write(str(block))
        del self.pending_block_map[block_id]
        return

    def committed_block(self, block_id):
        return

    def print_map(self):
        for k,v in self.pending_block_map.items():
            print(k, v)

        return

def main():

    # block1 = SpeculatedBlock()
    # file_path = "./ledger_map.txt"
    # ledger1 = Ledger(file_path=file_path)
    # ledger1.speculate(0, 1, txns = "transaction_1")
    # ledger1.speculate(1, 2,txns =  "transaction_2")
    # ledger1.speculate(1, 3, txns = "transaction_3")
    # print("*************************")
    # ledger1.print_map()
    # ledger1.commit(2, node_id)
    # print("*************************")
    # ledger1.print_map()

if __name__ == '__main__':
    main()


    