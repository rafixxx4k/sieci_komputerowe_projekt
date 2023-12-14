#ifndef GAMESTATE_HPP
#define GAMESTATE_HPP

#include "Player.hpp"
#include <vector>

class GameState
{
public:
    int winner;
    int number_of_players;
    int who_to_move;
    std::vector<Player> players;

    GameState()
        : winner(0), number_of_players(0), who_to_move(1), players() {}

    GameState(int w, int num, int move, int hand, std::vector<Player> p)
        : winner(w), number_of_players(num), who_to_move(move), players(p) {}
};

#endif // GAMESTATE_H
