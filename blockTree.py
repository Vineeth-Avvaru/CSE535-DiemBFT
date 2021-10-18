# from _typeshed import Self
import sys
import ledger
import collections
from hashing import Hashing
from logging_file import LogStuff

class BlockTree:
    def __init__(self, high_qc, high_commit_qc, f, ledger, mempool, node_id):
        self.high_qc=QC(VoteInfo("genesis_id",-1,"genesis_id",-2,"genesis_state", -1),LedgerCommitInfo(None,""),["genesis"], node_id, None)
        self.high_commit_qc=QC(VoteInfo("genesis_id",-2,"genesis_id",-3,"genesis_state", -1),LedgerCommitInfo(None,""),["genesis"], node_id, None)
        genesis_block = Block(node_id, 0, ["genesis_txn"], self.high_qc, "genesis_id",[])
        self.pending_block_tree = PendingBlockTree(genesis_block)
        self.pending_votes = collections.defaultdict(set)
        self.f = f
        self.ledger = ledger
        self.mempool = mempool
    
    def process_qc(self, qc, node_id):
        # LogStuff.log_to_file("***********Processing QC***************", node_id)
        if qc.ledger_commit_info.commit_state_id is not None:
            self.ledger.commit(qc.vote_info.parent_id, node_id)
            self.mempool.update_state(qc.vote_info.id.split('#')[2], "COMMIT")
            self.pending_block_tree.prune(qc.vote_info.id, node_id)
            if(qc.vote_info.round > self.high_commit_qc.vote_info.round):
                self.high_commit_qc = qc
        if(qc.vote_info.round > self.high_qc.vote_info.round):
            self.high_qc = qc
        return 

    def execute_and_insert(self, b):
        self.ledger.speculate(b.qc.vote_info.id, b.id, b.payload)
        self.mempool.update_state(b.payload, "PENDING")
        self.pending_block_tree.add(b)
        return 

    def process_vote(self, v, node_id, signature):
        LogStuff.log_to_file_node("***********Processing Vote***************", node_id)
        self.process_qc(v.high_commit_qc, node_id)
        vote_idx = Hashing.hashObj(v.ledger_commit_info)
        self.pending_votes[vote_idx].add(v.sign)
        if len(self.pending_votes[vote_idx]) == 2*self.f+1:
            
            return QC(vote_info= v.vote_info,ledger_commit_info = v.ledger_commit_info, signatures= self.pending_votes[vote_idx], author= node_id, signature= signature)
        return None

    def generate_block(self, txns, current_round):
        # Have to set author
        block = Block(author=1 , round = current_round, payload = txns, qc = self.high_qc, childBlocks=[])
        block.id = Hashing.hash(block.author, block.round, block.payload, self.high_qc.vote_info.id)
        return block

class SignatureInfo:
    def __init__(self, node_id, signature):
        self.node_id = node_id
        self.signature = signature

class VoteInfo:
    def __init__(self, id, round, parent_id, parent_round, exec_state_id, tid):
        self.id = id
        self.round = round
        self.parent_id = parent_id
        self.parent_round = parent_round
        self.exec_state_id = exec_state_id
        self.tid = tid

class LedgerCommitInfo:
    def __init__(self, commit_state_id, vote_info_hash):
        self.commit_state_id = commit_state_id
        self.vote_info_hash = vote_info_hash
        
class VoteMsg:
    def __init__(self, vote_info, ledger_commit_info, high_commit_qc, sender, signature):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.high_commit_qc = high_commit_qc
        self.sender = sender
        self.sign = signature

class QC:
    def __init__(self, vote_info, ledger_commit_info, signatures, author, signature):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures = signatures
        self.author = author
        self.sign = signature

class Block:
    def __init__(self, author, round, payload, qc, id = None, childBlocks = list()):
        self.author = author
        self.round = round
        self.payload = payload
        self.qc = qc
        self.id = id
        self.childBlocks = childBlocks

class TimeoutInfo:
    def __init__(self, round, high_qc, sender, signature):
        self.round = round
        self.high_qc = high_qc
        self.sender = sender
        self.signature = signature

class TC:
    def __init__(self, round, tmo_high_qc_rounds, tmo_signatures):
        self.round = round
        self.tmo_high_qc_rounds = tmo_high_qc_rounds
        self.tmo_signatures = tmo_signatures

class TimeoutMsg:
    def __init__(self, tmo_info, last_round_tc, high_commit_qc):
        self.tmo_info = tmo_info
        self.last_round_tc = last_round_tc
        self.high_commit_qc = high_commit_qc

class ProposalMsg:
    def __init__(self, block, last_round_tc, high_commit_qc, sender):
        self.block = block
        self.last_round_tc = last_round_tc
        self.high_commit_qc = high_commit_qc
        self.sender = sender
        # signature <- sign(block_id)

class PendingBlockTree:
    def __init__(self, genesis_block):
        self.genesis_block = genesis_block

    def add(self, b):
        parent_block = self.find(self.genesis_block, b.qc.vote_info.id)

        parent_block.childBlocks.append(b)
        return

    # Find the block with id
    def find(self, root, id):
        res = None
        if root is not None:
            if id == root.id:
                return root
            else:
                
                for i in range(0, len(root.childBlocks)):
                    block = root.childBlocks[i]
                    node_found = self.find(block, id)
                    if node_found:
                        res = node_found
                return res
        return res

    def prune(self, parent_id, node_id):
        pruned_node = self.find(self.genesis_block,parent_id)
        if pruned_node:
            self.genesis_block = pruned_node
        return
