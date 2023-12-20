#ifndef SERVER_HPP
#define SERVER_HPP

#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <thread>
#include <random>
#include <netinet/in.h>
#include <unistd.h>
#include <unordered_map>
#include <sstream>
#include <iomanip>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "Player.hpp"
#include "GameState.hpp"

class Server
{
public:
    Server(int port);
    void start();

private:
    int server_socket;
    int port;
    const int NUMBER_OF_CARDS = 19;
    const int STARTING_CARDS = 12;
    std::unordered_map<int, GameState> game_rooms;

    void handle_client(int client_socket);

    std::pair<int, Player> handle_login(const char *data, int client_socket);
    bool handle_room(int room_number, Player &player);

    void take_totem(GameState &game_state, int player_id);

    std::string convert_game_state_to_bytes(const GameState &game_state);
    void broadcast_game_state(GameState &game_state);

    int who_to_move(GameState &game_state);

    void put_new_card(GameState &game_state, int player_id);
    void new_card(GameState &game_state, Player &player);
};

#endif // SERVER_HPP
