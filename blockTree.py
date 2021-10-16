from _typeshed import Self
import sys
import ledger
import collections
from hashing import Hashing
from anytree import Node

class BlockTree:
    def __init__(self, high_qc, high_commit_qc, f, ledger):
        self.pending_block_tree = PendingBlockTree()
        self.pending_votes = collections.defaultdict(set)
        self.high_qc = high_qc
        self.high_commit_qc = high_commit_qc
        self.f = f
        self.ledger = ledger
    
    def process_qc(self, qc):
        if qc.ledger_commit_info.commit_state_id is not None:
            self.ledger.commit(qc.vote_info.parent_id)
            self.pending_block_tree.prune(qc.vote_info.parent_id)
            if(qc.vote_info.round > self.high_commit_qc.vote_info.round):
                self.high_commit_qc = qc
        if(qc.vote_info.round > self.high_qc.vote_info.round):
            self.high_qc = qc
        return 

    def execute_and_insert(self, b):
        self.ledger.speculate(b.qc.block_id, b.id, b.payload)
        self.pending_block_tree.add(b)
        return 

    def process_vote(self, v):
        self.process_qc(v.high_commit_qc)
        vote_idx = Hashing.hash(v.ledger_commit_info)
        self.pending_votes[vote_idx] =   self.pending_votes[vote_idx].add(v.sign)
        if len(self.pending_votes) >= 2*self.f+1:
            return QC(vote_info= v.vote_info, state_id= v.state_id, signatures= self.pending_votes[vote_idx])
        return None

    def generate_block(self, txns, current_round):
        # Have to set author
        block = Block(author=1 , round = current_round, payload = txns, qc = self.high_qc)
        block.id = Hashing.hash(block.author, block.round, block.payload, self.high_qc.vote_info.id, self.high_qc.signatures)
        return block

class VoteInfo:
    def __init__(self, id, round, parent_id, parent_round, exec_state_id):
        self.id = id
        self.round = round
        self.parent_id = parent_id
        self.parent_round = parent_round
        self.exec_state_id = exec_state_id

class LedgerCommitInfo:
    def __init__(self, commit_state_id, vote_info_hash):
        self.commit_state_id = commit_state_id
        self.vote_info_hash = vote_info_hash
        
class VoteMsg:
    def __init__(self, vote_info, ledger_commit_info, high_commit_qc, state_id):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.high_commit_qc = high_commit_qc
        self.state_id = state_id

class QC:
    def __init__(self, vote_info, ledger_commit_info, signatures, state_id):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures = signatures
        self.state_id = state_id

class Block:
    def __init__(self, author, round, payload, qc, id = None, childBlocks = list()):
        self.author = author
        self.round = round
        self.payload = payload
        self.qc = qc
        self.id = id
        self.childBlocks = childBlocks

class TimeoutInfo:
    def __init__(self, round, high_qc):
        self.round = round
        self.high_qc = high_qc
        # sender <- u
        # signature <- sign(round, high_qc.round)

class TC:
    def __init__(self, round, tmo_high_qc_rounds, tmo_signatures):
        self.round = round
        self.tmo_high_qc_rounds = tmo_high_qc_rounds
        self.tmo_signatures = tmo_signatures

class TimeoutMsg:
    def __init__(self, tmo_info, last_round_tc, high_commit_tc):
        self.tmo_info = tmo_info
        self.last_round_tc = last_round_tc
        self.high_commit_tc = high_commit_tc

class ProposalMsg:
    def __init__(self, block, last_round_tc, high_commit_tc):
        self.block = block
        self.last_round_tc = last_round_tc
        self.high_commit_tc = high_commit_tc
        # signature <- sign(block_id)

class PendingBlockTree:
    def __init__(self):
        self.genesis_block = Block(author= 'genesis', round=0, payload = None , qc = None, id = None, childBlocks=list())
    def add(self, b):
        parent_block = self.find(self.genesis_block,b.qc.vote_info.parent_id)
        parent_block.childBlocks.append(b)
        return
    # Find the block with id
    def find(self, root, id):
        for i in range(0, len(root.childBlocks)):
            block = root.childBlocks[i]
            if block.id == id :
                return block
            else:
                root = block
                return self.find(root, id)
        return 

    def prune(self,parent_id):
        self.genesis_block = self.find(parent_id)
        return
