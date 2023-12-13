#include "Server.hpp"

Server::Server(int port) : port(port), server_socket(-1) {}

void Server::start()
{
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len = sizeof(client_addr);

    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1)
    {
        std::cerr << "Error creating server socket" << std::endl;
        exit(1);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1)
    {
        std::cerr << "Error binding server socket" << std::endl;
        close(server_socket);
        exit(1);
    }

    if (listen(server_socket, 5) == -1)
    {
        std::cerr << "Error listening for connections" << std::endl;
        close(server_socket);
        exit(1);
    }

    std::cout << "Server listening on port " << port << std::endl;

    while (true)
    {
        std::cout << "Waiting for incoming connections..." << std::endl;

        int client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_addr_len);
        if (client_socket == -1)
        {
            std::cerr << "Error accepting client connection" << std::endl;
            continue;
        }

        std::cout << "Accepted connection from " << inet_ntoa(client_addr.sin_addr) << std::endl;

        // Start a new thread to handle the client
        std::thread client_thread(&Server::handle_client, this, client_socket);
        client_thread.detach(); // Detach the thread to run independently
    }
}

void Server::handle_client(int client_socket)
{
    char data[32];
    ssize_t bytes_received;

    // Receive login data
    bytes_received = recv(client_socket, data, sizeof(data), 0);
    if (bytes_received <= 0)
    {
        close(client_socket);
        return;
    }

    int room_number;
    Player player;
    std::tie(room_number, player) = handle_login(data, client_socket);

    if (!handle_room(room_number, player))
    {
        close(client_socket);
        return;
    }
    std::cout << "Player " << player.name << " joined room " << room_number << std::endl;

    int player_id = game_rooms[room_number].number_of_players;
    send(client_socket, std::to_string(player_id).c_str(), sizeof(int), 0);

    // Broadcast game state
    broadcast_game_state(game_rooms[room_number]);

    while (true)
    {
        bytes_received = recv(client_socket, data, sizeof(data), 0);

        std::cout << "Received " << bytes_received << " bytes" << std::endl;

        if (bytes_received <= 0)
        {
            // Client disconnected or error occurred
            std::cerr << "Client disconnected or error occurred" << std::endl;
            break;
        }
        if (std::string(data, 1) == "c")
        {
            // new_card(game_rooms[room_number], player);
        }
        else if (std::string(data, 1) == "t")
        {
            // take_totem(game_rooms[room_number], player, player_id - 1);
        }
    }

    // Cleanup
    close(client_socket);
    return;
}

std::pair<int, Player> Server::handle_login(const char *data, int client_socket)
{
    int room_number = std::stoi(std::string(data, 4));
    std::string player_name(data + 4, 14);
    Player player(player_name, 12, 1, std::rand() % (NUMBER_OF_CARDS + 1), client_socket);

    std::cout << "Created player " << player_name << " in room " << room_number << std::endl;

    return std::make_pair(room_number, player);
}

bool Server::handle_room(int room_number, Player &player)
{
    std::cout << "Player " << player.name << " joining room " << room_number << std::endl;
    if (game_rooms.find(room_number) == game_rooms.end())
    {
        game_rooms[room_number] = GameState(0, 0, 1, 0, {});
    }

    std::cout << "Number of players in room " << room_number << ": " << game_rooms[room_number].number_of_players << std::endl;
    if (game_rooms[room_number].number_of_players >= 8)
    {
        send(player.socket_fd, "0", 1, 0); // Room is full, send 0 to the client
        return false;
    }

    game_rooms[room_number].players.push_back(player);
    game_rooms[room_number].number_of_players++;
    return true;
}

std::string Server::convert_game_state_to_bytes(const GameState &game_state)
{
    std::stringstream result_byte;

    result_byte << game_state.winner;
    result_byte << game_state.number_of_players;
    result_byte << game_state.who_to_move;
    result_byte << '0';

    for (const auto &player : game_state.players)
    {
        result_byte << std::left << std::setw(14) << std::setfill(' ') << player.name;
        result_byte << std::right << std::setw(2) << std::setfill('0') << player.cards_on_hand;
        result_byte << std::right << std::setw(2) << std::setfill('0') << player.cards_on_table;
        result_byte << std::right << std::setw(2) << std::setfill('0') << player.card_face_up;
    }

    std::cout << "result_byte : " << result_byte.str() << std::endl;

    return result_byte.str();
}

void Server::broadcast_game_state(const GameState &game_state)
{
    std::string game_state_bytes = convert_game_state_to_bytes(game_state);

    std::cout << "Broadcasting game state: " << game_state_bytes << std::endl;

    for (const Player &player : game_state.players)
    {
        std::cout << "Sending to player: " << player.name << std::endl;
        send(player.socket_fd, game_state_bytes.c_str(), game_state_bytes.size(), 0);
    }
}