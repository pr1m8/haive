.. title:: Chess - Strategic Board Game
.. _chess-game:

♟️ Chess Game Documentation
===========================

.. raw:: html

   <div class="agent-hero-section">
      <div class="hero-content">
         <h2>♟️ Advanced Chess Engine & AI</h2>
         <p class="hero-description">
            A complete chess implementation with sophisticated AI opponents, opening book, endgame tables, 
            and position analysis. Test your agents against various difficulty levels.
         </p>
      </div>
   </div>

Overview
--------

The Chess game in Haive provides a full-featured chess environment with:

- **Complete Rule Implementation**: All chess rules including castling, en passant, and promotion
- **Advanced AI**: Multiple difficulty levels with different playing styles
- **Analysis Tools**: Position evaluation, best move suggestions, and game analysis
- **Opening Library**: Extensive opening book with common variations
- **Endgame Tables**: Perfect play in endgame positions
- **Interactive Visualization**: Beautiful board rendering and move animations

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>🎯 Game Features</h2>
      </div>
      <div class="api-grid">
         <div class="api-section">
            <h4>🎮 Gameplay</h4>
            <ul>
               <li>Standard chess rules</li>
               <li>Time controls</li>
               <li>Move validation</li>
               <li>Game history</li>
               <li>Position import/export</li>
            </ul>
         </div>
         
         <div class="api-section">
            <h4>🤖 AI Features</h4>
            <ul>
               <li>Minimax with alpha-beta</li>
               <li>Iterative deepening</li>
               <li>Transposition tables</li>
               <li>Move ordering</li>
               <li>Quiescence search</li>
            </ul>
         </div>
         
         <div class="api-section">
            <h4>📊 Analysis</h4>
            <ul>
               <li>Position evaluation</li>
               <li>Best move calculation</li>
               <li>Threat detection</li>
               <li>Opening identification</li>
               <li>Endgame classification</li>
            </ul>
         </div>
      </div>
   </div>

Quick Start
-----------

.. raw:: html

   <div class="code-example-section">
      <h4>🚀 Basic Chess Game</h4>

.. code-block:: python

   from haive.games.chess import ChessGame, ChessAgent
   from haive.core.engine.aug_llm import AugLLMConfig
   import asyncio

   async def play_chess():
       # Create chess game
       game = ChessGame()
       
       # Create AI agents with different strengths
       white_agent = ChessAgent(
           name="Magnus",
           color="white",
           engine=AugLLMConfig(temperature=0.1),
           skill_level=8,  # 1-10 scale
           style="aggressive"  # "aggressive", "positional", "defensive"
       )
       
       black_agent = ChessAgent(
           name="Stockfish",
           color="black",
           engine=AugLLMConfig(temperature=0.1),
           skill_level=6,
           style="positional"
       )
       
       # Play the game
       print("Starting chess game...")
       game.display_board()
       
       while not game.is_game_over():
           current_player = "white" if game.current_turn == "w" else "black"
           agent = white_agent if current_player == "white" else black_agent
           
           # Get agent's move
           move = await agent.get_move(game.get_board_state())
           
           # Make the move
           success = game.make_move(move)
           if success:
               print(f"\n{agent.name} plays: {move}")
               game.display_board()
               
               # Show evaluation
               eval_score = game.evaluate_position()
               print(f"Position evaluation: {eval_score:+.2f}")
       
       # Game over
       result = game.get_result()
       print(f"\nGame Over! Result: {result}")
       
       # Get game analysis
       analysis = game.analyze_game()
       print(f"\nGame Analysis:")
       print(f"Total moves: {analysis['move_count']}")
       print(f"Opening: {analysis['opening']}")
       print(f"Critical moments: {analysis['critical_positions']}")

   # Run the game
   asyncio.run(play_chess())

.. raw:: html

   </div>

Game Mechanics
--------------

.. raw:: html

   <div class="custom-section">
      <h3>♟️ Chess Rules Implementation</h3>

.. code-block:: python

   from haive.games.chess import ChessGame, Move, Piece
   from haive.games.chess.rules import (
       is_valid_move,
       is_check,
       is_checkmate,
       is_stalemate,
       get_legal_moves
   )

   # Create and manipulate game state
   game = ChessGame()

   # Make moves using different notations
   game.make_move("e4")      # Pawn to e4
   game.make_move("e7e5")    # Pawn e7 to e5
   game.make_move("Nf3")     # Knight to f3
   game.make_move("Nc6")     # Knight to c6

   # Advanced moves
   game.make_move("O-O")     # Castle kingside
   game.make_move("O-O-O")   # Castle queenside
   game.make_move("exd5")    # Pawn captures on d5
   game.make_move("e8=Q")    # Pawn promotion to Queen

   # Check game state
   if game.is_check():
       print("King is in check!")
       
       # Get all moves that escape check
       legal_moves = game.get_legal_moves()
       escape_moves = [
           move for move in legal_moves
           if game.would_escape_check(move)
       ]
       print(f"Escape moves: {escape_moves}")

   # Position analysis
   position_info = game.analyze_position()
   print(f"Material balance: {position_info['material_balance']}")
   print(f"King safety: {position_info['king_safety']}")
   print(f"Center control: {position_info['center_control']}")
   print(f"Development: {position_info['development']}")

   # Threefold repetition and 50-move rule
   if game.is_threefold_repetition():
       print("Draw by repetition available")
   
   if game.halfmove_clock >= 100:  # 50 moves = 100 half-moves
       print("Draw by 50-move rule available")

   # Export/Import positions
   fen = game.to_fen()  # Export as FEN
   pgn = game.to_pgn()  # Export as PGN

   # Load a specific position
   game.load_fen("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")

.. raw:: html

   </div>

AI Strategies
-------------

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>🧠 Chess AI Implementation</h2>
      </div>

.. code-block:: python

   from haive.games.chess import ChessAI, EvaluationFunction
   from haive.games.chess.ai import (
       MinimaxEngine,
       AlphaBetaEngine,
       MCTSEngine,
       NeuralEngine
   )

   # 1. Minimax with Alpha-Beta Pruning
   class AlphaBetaChessAI(ChessAI):
       def __init__(self, depth: int = 4):
           self.depth = depth
           self.transposition_table = {}
           self.history_table = {}  # For move ordering
       
       def get_best_move(self, board_state):
           """Find best move using alpha-beta search."""
           
           def minimax(state, depth, alpha, beta, maximizing):
               # Check transposition table
               state_hash = hash(state)
               if state_hash in self.transposition_table:
                   return self.transposition_table[state_hash]
               
               # Terminal node
               if depth == 0 or state.is_game_over():
                   eval_score = self.evaluate(state)
                   self.transposition_table[state_hash] = eval_score
                   return eval_score
               
               # Get moves ordered by history heuristic
               moves = self.order_moves(state.get_legal_moves())
               
               if maximizing:
                   max_eval = float('-inf')
                   for move in moves:
                       state.make_move(move)
                       eval_score = minimax(state, depth - 1, alpha, beta, False)
                       state.undo_move()
                       
                       max_eval = max(max_eval, eval_score)
                       alpha = max(alpha, eval_score)
                       
                       if beta <= alpha:
                           # Update history for good moves
                           self.history_table[move] = self.history_table.get(move, 0) + depth
                           break
                   
                   return max_eval
               else:
                   min_eval = float('inf')
                   for move in moves:
                       state.make_move(move)
                       eval_score = minimax(state, depth - 1, alpha, beta, True)
                       state.undo_move()
                       
                       min_eval = min(min_eval, eval_score)
                       beta = min(beta, eval_score)
                       
                       if beta <= alpha:
                           self.history_table[move] = self.history_table.get(move, 0) + depth
                           break
                   
                   return min_eval
           
           # Iterative deepening
           best_move = None
           for d in range(1, self.depth + 1):
               moves_with_scores = []
               
               for move in board_state.get_legal_moves():
                   board_state.make_move(move)
                   score = minimax(board_state, d - 1, float('-inf'), float('inf'), False)
                   board_state.undo_move()
                   moves_with_scores.append((move, score))
               
               # Sort by score
               moves_with_scores.sort(key=lambda x: x[1], reverse=True)
               best_move = moves_with_scores[0][0]
           
           return best_move
       
       def order_moves(self, moves):
           """Order moves for better pruning."""
           return sorted(
               moves,
               key=lambda m: self.history_table.get(m, 0),
               reverse=True
           )

   # 2. Position Evaluation
   class AdvancedEvaluator(EvaluationFunction):
       def __init__(self):
           # Piece values
           self.piece_values = {
               'P': 100, 'N': 320, 'B': 330,
               'R': 500, 'Q': 900, 'K': 20000
           }
           
           # Positional tables (simplified)
           self.pawn_table = [
               [0,  0,  0,  0,  0,  0,  0,  0],
               [50, 50, 50, 50, 50, 50, 50, 50],
               [10, 10, 20, 30, 30, 20, 10, 10],
               [5,  5, 10, 25, 25, 10,  5,  5],
               [0,  0,  0, 20, 20,  0,  0,  0],
               [5, -5,-10,  0,  0,-10, -5,  5],
               [5, 10, 10,-20,-20, 10, 10,  5],
               [0,  0,  0,  0,  0,  0,  0,  0]
           ]
       
       def evaluate(self, board_state) -> float:
           """Comprehensive position evaluation."""
           score = 0.0
           
           # Material count
           score += self.material_balance(board_state)
           
           # Positional factors
           score += self.piece_positioning(board_state)
           score += self.king_safety(board_state)
           score += self.pawn_structure(board_state)
           score += self.center_control(board_state)
           score += self.mobility(board_state)
           
           # Game phase adjustments
           phase = self.game_phase(board_state)
           if phase == "opening":
               score += self.opening_principles(board_state)
           elif phase == "endgame":
               score += self.endgame_principles(board_state)
           
           return score

   # 3. Opening Book
   class OpeningBook:
       def __init__(self):
           self.book = {
               "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -": [
                   ("e4", 0.45),    # King's pawn
                   ("d4", 0.40),    # Queen's pawn
                   ("Nf3", 0.10),   # Reti
                   ("c4", 0.05)     # English
               ],
               # More positions...
           }
       
       def get_book_move(self, fen: str):
           """Get move from opening book."""
           if fen in self.book:
               moves = self.book[fen]
               # Weighted random selection
               import random
               total = sum(weight for _, weight in moves)
               r = random.uniform(0, total)
               cumsum = 0
               for move, weight in moves:
                   cumsum += weight
                   if r <= cumsum:
                       return move
           return None

.. raw:: html

   </div>

Training Chess Agents
---------------------

.. raw:: html

   <div class="custom-section">
      <h3>🎓 Training and Improvement</h3>

.. code-block:: python

   from haive.games.chess import ChessTrainer, ChessAgent
   from haive.games.chess.training import (
       SelfPlayTrainer,
       OpeningTrainer,
       EndgameTrainer,
       TacticsTrainer
   )
   import asyncio

   # Self-play training
   async def train_through_self_play():
       trainer = SelfPlayTrainer(
           base_agent=ChessAgent(
               name="learner",
               engine=AugLLMConfig(),
               skill_level=5
           ),
           games_per_iteration=100,
           learning_rate=0.01
       )
       
       # Train for multiple iterations
       for iteration in range(10):
           print(f"\nTraining iteration {iteration + 1}")
           
           # Play games
           results = await trainer.play_training_games()
           
           # Analyze games
           improvements = trainer.analyze_games(results)
           
           # Update agent
           trainer.update_agent(improvements)
           
           # Test against benchmark
           win_rate = await trainer.test_against_benchmark()
           print(f"Win rate vs benchmark: {win_rate:.1%}")

   # Opening repertoire training
   class OpeningTrainer:
       def __init__(self, target_openings: List[str]):
           self.target_openings = target_openings
           self.opening_database = self.load_opening_database()
       
       async def train_opening(self, agent: ChessAgent, opening_name: str):
           """Train specific opening."""
           
           # Get opening moves
           opening_lines = self.opening_database[opening_name]
           
           for line in opening_lines:
               # Set up position
               game = ChessGame()
               for move in line['moves']:
                   game.make_move(move)
               
               # Train from this position
               training_positions = self.generate_training_positions(game)
               
               for position in training_positions:
                   # Get agent's move
                   agent_move = await agent.get_move(position)
                   
                   # Compare with book move
                   book_move = line['best_moves'].get(position.fen())
                   
                   if agent_move != book_move:
                       # Provide feedback
                       await agent.learn_from_mistake(
                           position,
                           agent_move,
                           book_move,
                           line['explanation']
                       )

   # Tactics training
   class TacticsTrainer:
       def __init__(self, puzzle_database):
           self.puzzles = puzzle_database
       
       async def train_tactics(self, agent: ChessAgent, difficulty: str):
           """Train tactical patterns."""
           
           puzzles = self.get_puzzles_by_difficulty(difficulty)
           correct = 0
           
           for puzzle in puzzles:
               # Show position
               game = ChessGame()
               game.load_fen(puzzle['fen'])
               
               # Get agent's solution
               solution = await agent.solve_puzzle(
                   game,
                   hint=puzzle.get('hint')
               )
               
               # Check solution
               if self.is_correct_solution(solution, puzzle['solution']):
                   correct += 1
                   print(f"✓ Solved: {puzzle['theme']}")
               else:
                   print(f"✗ Failed: {puzzle['theme']}")
                   # Show correct solution
                   await self.explain_solution(agent, puzzle)
           
           accuracy = correct / len(puzzles)
           print(f"\nTactics accuracy: {accuracy:.1%}")
           
           return accuracy

.. raw:: html

   </div>

Analysis and Visualization
---------------------------

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>📊 Game Analysis Tools</h2>
      </div>

.. code-block:: python

   from haive.games.chess import ChessAnalyzer
   from haive.games.chess.visualization import BoardRenderer, GameReplay
   import matplotlib.pyplot as plt

   # Analyze completed game
   analyzer = ChessAnalyzer()

   # Load game from PGN
   game = analyzer.load_pgn("""
   [Event "Test Game"]
   [White "Agent1"]
   [Black "Agent2"]
   
   1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6
   5. O-O Be7 6. Re1 b5 7. Bb3 O-O 8. c3 d5
   """)

   # Full game analysis
   analysis = analyzer.analyze_game(game)

   print("Game Analysis Report")
   print("===================\n")

   # Opening analysis
   print(f"Opening: {analysis['opening']['name']}")
   print(f"ECO Code: {analysis['opening']['eco']}")
   print(f"Theory deviation: Move {analysis['opening']['theory_end']}\n")

   # Critical moments
   print("Critical Positions:")
   for moment in analysis['critical_moments']:
       print(f"Move {moment['move_number']}: {moment['description']}")
       print(f"  Best: {moment['best_move']} ({moment['best_eval']:+.2f})")
       print(f"  Played: {moment['played_move']} ({moment['played_eval']:+.2f})")
       print(f"  Mistake severity: {moment['severity']}\n")

   # Evaluation graph
   plt.figure(figsize=(12, 6))
   moves = range(len(analysis['evaluations']))
   evals = analysis['evaluations']
   
   plt.plot(moves, evals, 'b-', linewidth=2)
   plt.axhline(y=0, color='gray', linestyle='--')
   plt.fill_between(moves, 0, evals, alpha=0.3)
   
   # Mark critical moments
   for moment in analysis['critical_moments']:
       move_num = moment['move_number'] * 2 - (2 if moment['color'] == 'white' else 1)
       plt.axvline(x=move_num, color='red', alpha=0.5)
   
   plt.xlabel('Move Number')
   plt.ylabel('Evaluation (pawns)')
   plt.title('Game Evaluation Over Time')
   plt.grid(True, alpha=0.3)
   plt.show()

   # Move quality distribution
   move_quality = analysis['move_quality']
   
   plt.figure(figsize=(10, 6))
   categories = ['Brilliant', 'Best', 'Good', 'Inaccuracy', 'Mistake', 'Blunder']
   white_counts = [move_quality['white'][cat] for cat in categories]
   black_counts = [move_quality['black'][cat] for cat in categories]
   
   x = range(len(categories))
   width = 0.35
   
   plt.bar([i - width/2 for i in x], white_counts, width, label='White', color='lightgray')
   plt.bar([i + width/2 for i in x], black_counts, width, label='Black', color='darkgray')
   
   plt.xlabel('Move Quality')
   plt.ylabel('Count')
   plt.title('Move Quality Distribution')
   plt.xticks(x, categories, rotation=45)
   plt.legend()
   plt.tight_layout()
   plt.show()

   # Interactive board visualization
   renderer = BoardRenderer()
   
   # Show specific position
   renderer.show_position(
       game.get_position_at_move(20),
       highlights={
           'e4': 'green',  # Good square
           'd5': 'red',    # Weak square
           'f7': 'yellow'  # Target square
       },
       arrows=[
           ('e1', 'e8', 'blue'),  # Attack
           ('g1', 'f3', 'green')  # Defense
       ]
   )

.. raw:: html

   </div>

API Reference
-------------

.. automodule:: haive.games.chess
   :members:
   :show-inheritance:

.. autoclass:: haive.games.chess.ChessGame
   :members:
   :show-inheritance:

.. autoclass:: haive.games.chess.ChessAgent
   :members:
   :show-inheritance:

.. autoclass:: haive.games.chess.ChessAI
   :members:
   :show-inheritance:

Next Steps
----------

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>🚀 Explore More Games</h2>
      </div>
      <div class="agent-showcase">
         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">🎯</div>
               <div>
                  <h3 class="agent-title">Other Board Games</h3>
                  <p class="agent-subtitle">More strategic challenges</p>
               </div>
            </div>
            <p class="agent-description">
               Try other board games like Go, Checkers, and Connect Four with similar AI capabilities.
            </p>
            <a href="../index.html" class="agent-link">Browse Games</a>
         </div>

         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">🏆</div>
               <div>
                  <h3 class="agent-title">Chess Tournaments</h3>
                  <p class="agent-subtitle">Competitive play</p>
               </div>
            </div>
            <p class="agent-description">
               Organize tournaments between multiple agents with different strategies and skill levels.
            </p>
            <a href="../../guides/game_tournaments.html" class="agent-link">Tournament Guide</a>
         </div>

         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">🤖</div>
               <div>
                  <h3 class="agent-title">Custom Chess Agents</h3>
                  <p class="agent-subtitle">Build your own AI</p>
               </div>
            </div>
            <p class="agent-description">
               Create custom chess agents with unique evaluation functions and playing styles.
            </p>
            <a href="../../guides/custom_game_agents.html" class="agent-link">Agent Guide</a>
         </div>
      </div>
   </div>

.. seealso::

   - :doc:`../../agents/index` - Agents that can play chess
   - :doc:`../../guides/game_ai` - Building game AI
   - :doc:`../index` - Back to games overview