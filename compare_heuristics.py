"""
Compares Ultimate Tic Tac Toe game tree heuristics.
"""

import random
import time
import argparse

from engine.GameTree import GameTree
from UTTTState import UTTTState
from UTTTSpace import UTTTSpace
from heuristic import heuristic_A, heuristic_B

TRACE = False
DICTATE = False

def always_choose_random_state(node):
    """
    Makes a random move.
    """
    return random.randint(0, len(node.successors()) - 1)


def trace(*args):
    if TRACE:
        print(*args)

"""
Entry point for Ultimate Tic Tac Toe game tree demo.
"""
def main():
    """
    Collects win and runtime stats on each heuristic at differing depths.
    """
    trials = 5
    depth = [1, 2, 3]
    heuristics = { 'A': heuristic_A, 'B': heuristic_B }

    # Testing for standard UTTT board.

    for hName, hFunc in sorted(heuristics.items()):
        trace("[Heuristic {}]".format(hName))

        all_time = 0
        all_wins = 0

        for d in depth:
            trace("[Heuristic {}; Depth: {}]".format(hName, d))

            all_order_time = 0
            all_order_wins = 0

            for opponent_first in [True, False]:
                player_zero = ("Opponent" if opponent_first else "AI")

                trace("[Heuristic {}; Depth: {}; Player Zero: {}]".format(hName, d, player_zero))

                # Force AI to be Player with id 0 always.
                initial_state = UTTTState(1 if opponent_first else 0, None, None, UTTTSpace(None, 3, 3))

                i_time = 0
                i_wins = 0

                for t in range(trials):
                    trace("[Heuristic {}; Depth: {}; Player Zero: {}; Trial: {}]".format(hName, d, player_zero, t))

                    # Instantiate the game tree.
                    game = GameTree(initial_state, opponent_first, d)

                    # Test against random.
                    game.attach_turn_handler(always_choose_random_state)

                    game.DICTATE = DICTATE

                    start = time.time()
                    win = game.play(hFunc)
                    i_time += time.time() - start
                    i_wins += 1 if win else 0

                avg_time = i_time / trials
                percent_win = i_wins / trials

                print("Trials: {}\tHeuristic: {}\tDepth: {}\tAvg Runtime: {}\tWin Percent: {}\tPlayer 0: {}".format(trials, hName, d, avg_time, percent_win, player_zero))

                all_order_time += avg_time
                all_order_wins += percent_win

            # Average over opponent starting vs. AI starting.
            avg_time = all_order_time / 2
            percent_win = all_order_wins / 2

            print("Trials: {}\tHeuristic: {}\tDepth: {}\tAvg Runtime: {}\tWin Percent: {}".format(trials * 2, hName, d, avg_time, percent_win))

            all_time += avg_time
            all_wins += percent_win

        # Average over opponent starting vs. AI starting.
        avg_time = all_time / (len(depth) + 1)
        percent_win = all_wins / (len(depth) + 1)

        print("Trials: {}\tHeuristic: {}\tAvg Runtime: {}\tWin Percent: {}".format(trials * 2 * (range(depth) + 1), hName, avg_time, percent_win))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compares heuristics.')
    parser.add_argument('--trace', dest='TRACE', action='store_true', help='Enables minimal tracing.')
    parser.add_argument('--dictate', dest='DICTATE', action='store_true', help='Enables move dictation.')
    args = parser.parse_args()

    TRACE = args.TRACE
    DICTATE = args.DICTATE

    main()
