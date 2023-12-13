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
    std::unordered_map<int, GameState> game_rooms;

    void handle_client(int client_socket);
    std::pair<int, Player> handle_login(const char *data, int client_socket);
    bool handle_room(int room_number, Player &player);
    std::string convert_game_state_to_bytes(const GameState &game_state);
    void broadcast_game_state(const GameState &game_state);
};

#endif // SERVER_HPP
