from blockTree import BlockTree, TC

class Pacemaker:
    def __init__(self, block_tree, config):

        # instance variables
        self.current_round = 0
        self.last_round_tc = None
        self.pending_timeouts = {}
        # block_tree object
        self.block_tree = block_tree

        self.config = config


    def get_round_timer(self, round = 0):
        return 4 * self.config['delta']

    