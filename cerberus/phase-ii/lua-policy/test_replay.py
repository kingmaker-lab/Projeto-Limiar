import os
from pathlib import Path
import random
import subprocess
import unittest


def replay(trace):
    return subprocess.run([os.environ.get("LUA", "lua5.4"), "replay.lua"],
                          cwd=Path(__file__).resolve().parent, input=trace,
                          text=True, capture_output=True, timeout=8)


class LuaReplay(unittest.TestCase):
    def test_hot_policy_change_preserves_existing_sessions(self):
        run = replay("publish 0 off 1\nadmit a\nadmit a\nadmit b\n"
                     "publish 0 on 1\npublish 1 on 1\nrelease a\nadmit b\n"
                     "publish 2 off 1\nadmit b")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout.splitlines(), [
            "1\t0\tpublished", "1\t1\taccepted", "1\t1\tduplicate", "1\t1\tcapacity",
            "1\t1\tstale", "2\t1\tpublished", "2\t0\treleased", "2\t0\tmaintenance",
            "3\t0\tpublished", "3\t1\taccepted",
        ])

    def test_invalid_inputs_and_bounded_lines(self):
        run = replay("publish 0 off 0\npublish 1.0 off 2\npublish 0 x 2\n"
                     "publish 9223372036854775808 off 2\nadmit a/b\n"
                     "admit " + "x" * 65 + "\n")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout.splitlines(), ["0\t0\tinvalid"] * 6)
        run = replay("admit " + "x" * 251 + "\nadmit valid\n")
        self.assertEqual(run.returncode, 64)
        self.assertEqual(run.stdout, "")

    def test_differential_replay(self):
        rng = random.Random(2206)
        events = []
        expected = []
        occupied = set()
        state = (0, False, 100)
        for _ in range(500):
            generation, maintenance, limit = state
            action = rng.choice(("publish", "admit", "admit", "release"))
            session = f"s{rng.randrange(12)}"
            if action == "publish":
                base = generation + rng.choice((0, 0, 1))
                proposed = rng.choice((True, False))
                capacity = rng.randrange(1, 8)
                events.append(f"publish {base} {'on' if proposed else 'off'} {capacity}")
                if base != generation:
                    verdict = "stale"
                else:
                    state = (generation + 1, proposed, capacity)
                    verdict = "published"
            else:
                events.append(f"{action} {session}")
                if action == "release":
                    verdict = "released" if session in occupied else "absent"
                    occupied.discard(session)
                else:
                    verdict = next((reason for reject, reason in [
                        (session in occupied, "duplicate"),
                        (maintenance, "maintenance"),
                        (len(occupied) >= limit, "capacity"),
                    ] if reject), "accepted")
                    if verdict == "accepted":
                        occupied.add(session)
            expected.append(f"{state[0]}\t{len(occupied)}\t{verdict}")

        trace = "\n".join(events) + "\n"
        run = replay(trace)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout.splitlines(), expected)
        self.assertEqual(replay(trace).stdout, run.stdout)
