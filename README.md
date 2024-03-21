# Chess
A Python-based Chess GUI and Engine developed as a final project for CS40S. This project allows users to play a friend, play a bot, or visualize a battle between bots. It's built using the pygame library in python.

## Todo Engine
- Add better Move Ordering with value of taken_piece - attacking_piece, replace capture boolean in Move
- Move Generation with only legal moves
- Convert Board back to 64 lenth array
- Precalculate all moves in 64 length array (including pawn moves this time)
- Add better search
- Add end-game piece value tables
- Better pattern to checkmate (force king to edge)
- Stop bot from stale-mating

## Todo GUI
- Add buttons (back, quit, sound, home)
- Add menu
- Add different gamemodes (play a friend, play engine, visualize battle)
