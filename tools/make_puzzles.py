#!/usr/bin/env python3
"""Make original chess puzzles from real games, checked with Stockfish for a single best answer.

Source games: Lichess standard games database (CC0): https://database.lichess.org/
Engine: Stockfish (GPL-3.0), run as a local tool. python-chess (GPL-3.0) as a local tool.
Neither is shipped in the app by this script; the output is a plain JSON list of positions + moves.

Usage:
  python make_puzzles.py --pgn lichess_db_standard_rated_2013-01.pgn.zst --engine ./stockfish \
      --out content/puzzles.json --count 200 [--min-elo 1500] [--nodes 400000] [--seed 7]

Uniqueness rule (every player move in the line):
  best move wins clearly  : eval >= +WIN cp (default 250) or a forced mate for the player
  second-best is far worse: second <= +100 cp AND best - second >= GAP cp (default 200)
  a mate-in-one step is kept only if exactly one legal move mates.
Every kept puzzle is re-checked at --verify-nodes (default 4x --nodes); any step that is no longer unique is dropped.
Opponent replies are Stockfish's best move. Lines are 1-3 player moves.
"""
import argparse, io, json, random, sys
import chess, chess.pgn, chess.engine

def open_pgn(path):
    if path.endswith('.zst'):
        import zstandard
        return io.TextIOWrapper(zstandard.ZstdDecompressor().stream_reader(open(path, 'rb')), encoding='utf-8', errors='replace')
    return open(path, encoding='utf-8', errors='replace')

def cp(score):  # score from side-to-move's view, mates mapped to big numbers
    return score.score(mate_score=100000)

def unique_best(engine, board, nodes, win, gap):
    infos = engine.analyse(board, chess.engine.Limit(nodes=nodes), multipv=2)
    if len(infos) < 2 or 'pv' not in infos[0]:
        return None
    b, s = cp(infos[0]['score'].relative), cp(infos[1]['score'].relative)
    move = infos[0]['pv'][0]
    board.push(move); mates_now = board.is_checkmate(); board.pop()
    if mates_now:
        mates = 0
        for m in board.legal_moves:
            board.push(m); mates += board.is_checkmate(); board.pop()
        return (move, b, True) if mates == 1 else None   # single best answer: exactly one mating move
    if b >= win and s <= 100 and b - s >= gap and not infos[1]['score'].relative.is_mate():
        return move, b, False
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pgn', required=True); ap.add_argument('--engine', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--count', type=int, default=100)
    ap.add_argument('--min-elo', type=int, default=1500); ap.add_argument('--nodes', type=int, default=400000)
    ap.add_argument('--win', type=int, default=250); ap.add_argument('--gap', type=int, default=200)
    ap.add_argument('--max-games', type=int, default=20000); ap.add_argument('--verify-nodes', type=int, default=0); ap.add_argument('--seed', type=int, default=7)
    a = ap.parse_args(); rng = random.Random(a.seed)
    eng = chess.engine.SimpleEngine.popen_uci(a.engine)
    out, seen, games = [], set(), 0
    f = open_pgn(a.pgn)
    while len(out) < a.count and games < a.max_games:
        g = chess.pgn.read_game(f)
        if g is None: break
        games += 1
        h = g.headers
        try:
            if min(int(h.get('WhiteElo', 0)), int(h.get('BlackElo', 0))) < a.min_elo: continue
        except ValueError: continue
        moves = list(g.mainline_moves())
        if len(moves) < 24: continue
        ply = rng.randrange(16, len(moves) - 4)
        board = g.board()
        for m in moves[:ply]: board.push(m)
        # quick pre-filter: side to move must not already be totally winning before the tactic
        first = unique_best(eng, board, a.nodes, a.win, a.gap)
        if not first: continue
        fen = board.fen()
        if fen in seen: continue
        line, any_mate_last, b = [], False, board.copy()
        res = first
        for _ in range(3):
            mv, score, mate_now = res
            line.append(mv.uci()); b.push(mv)
            if mate_now or b.is_game_over():
                any_mate_last = mate_now; break
            reply = eng.play(b, chess.engine.Limit(nodes=a.nodes)).move
            if reply is None: break
            line.append(reply.uci()); b.push(reply)
            nxt = unique_best(eng, b, a.nodes, a.win, a.gap)
            if not nxt:
                line.pop(); b.pop(); break     # end the puzzle after the player's last unique move
            res = nxt
        # deeper re-check of every player move
        vn = a.verify_nodes or a.nodes * 4
        vb, good = chess.Board(fen), True
        for i, u in enumerate(line):
            if i % 2 == 0:
                r = unique_best(eng, vb, vn, a.win, a.gap)
                if not r or r[0].uci() != u:
                    if i == 0: good = False
                    else: line = line[:i - 1]
                    break
            vb.push_uci(u)
        if not good or not line: continue
        seen.add(fen)
        out.append({
            'id': f'bm{len(out)+1:05d}', 'fen': fen, 'moves': line,
            'evalCp': first[1],
            'sourceGame': h.get('Site', ''), 'madeBy': 'Made by your bot from a Lichess game (CC0); checked with Stockfish for a single best answer',
        })
        print(f'{len(out)}/{a.count} from {games} games', file=sys.stderr)
    eng.quit()
    json.dump(out, open(a.out, 'w'), indent=1)
    print(f'wrote {len(out)} puzzles to {a.out} (scanned {games} games)')

if __name__ == '__main__':
    main()
