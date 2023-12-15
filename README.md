# Take totem and win game
This repository store all the necessary files to run **Take totem and win** game (based on Jungle Speed). 

Steps to launch the game:
* `git clone https://github.com/rafixxx4k/sieci_komputerowe_projekt.git`
* `cd sieci-komputerowe-projekt`
* `g++ game_cpp/*.cpp -o server`
* `./server`, now the server is listening and waiting for clients
* open a new terminal for each player and run: `cd game_python && python main.py`
