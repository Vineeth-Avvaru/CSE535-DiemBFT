#import BLOCK_TREE

class Pacemaker:
    def __init__(self, current_round, last_round_tc, pending_timouts, block_tree):
        pass

    def get_round_timer(self, round):
        pass

    def start_timer(self, new_round):
        pass
    
    def local_timeout_round(self):
        pass

    def process_remote_timeout(self, timeout):
        pass

    def advance_round_tc(self, tc):
        pass

    def advance_round_qc(self, qc):
        pass