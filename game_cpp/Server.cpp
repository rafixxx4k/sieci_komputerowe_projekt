#include "Server.hpp"

Server::Server(int port) : port(port), server_socket(-1) {}

void Server::start()
{
    std::srand(static_cast<unsigned int>(std::time(nullptr)));

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

        // std::cout << "Received " << bytes_received << " bytes from " << player.name << std::endl;
        // std::cout << "Received data: " << std::string(data, bytes_received) << std::endl;

        if (bytes_received <= 0)
        {
            // Client disconnected or error occurred
            std::cerr << "Client disconnected or error occurred" << std::endl;
            this->game_rooms[room_number].players[player_id - 1].card_face_up = -1;

            // if the player who disconnected was the one to move, change who to move
            // end game if all players disconnected (who_to_move returns -1)
            if (this->game_rooms[room_number].who_to_move == player_id)
            {
                std::cout << "Disconnected player had move, changing who to move" << std::endl;
                if (this->who_to_move(game_rooms[room_number]) == -1)
                {
                    std::cout << "All players disconnected. Closing room " << room_number << std::endl;
                    this->game_rooms.erase(room_number);
                    close(client_socket);
                    return;
                }
            }

            broadcast_game_state(this->game_rooms[room_number]);
            break;
        }
        if (std::string(data, 1) == "c")
        {
            std::cout << "Player " << player.name << " puts a new card" << std::endl;
            put_new_card(this->game_rooms[room_number], player_id);
            broadcast_game_state(this->game_rooms[room_number]);
        }
        else if (std::string(data, 1) == "t")
        {
            std::cout << "Player " << player.name << " takes the totem" << std::endl;
            take_totem(this->game_rooms[room_number], player_id);
            broadcast_game_state(this->game_rooms[room_number]);
        }
    }

    // Cleanup
    close(client_socket);
    return;
}

int Server::who_to_move(GameState &game_state)
{
    int disconnected = 0;
    while (true)
    {
        game_state.who_to_move = (game_state.who_to_move % game_state.number_of_players) + 1;

        if (game_state.players[game_state.who_to_move - 1].card_face_up == -1)
            disconnected++;
        else
            break;

        // if all players are disconnected
        if (disconnected == game_state.number_of_players)
            return -1;
    }

    return 0;
}

std::pair<int, Player> Server::handle_login(const char *data, int client_socket)
{
    int room_number = std::stoi(std::string(data, 4));
    std::string player_name(data + 4, 14);
    Player player(player_name, this->STARTING_CARDS, 1, std::rand() % (NUMBER_OF_CARDS + 1), client_socket, -1);

    std::cout << "Created player " << player_name << " in room " << room_number << std::endl;

    return std::make_pair(room_number, player);
}

bool Server::handle_room(int room_number, Player &player)
{
    std::cout << "Player " << player.name << " wants to join room " << room_number << std::endl;
    if (this->game_rooms.find(room_number) == game_rooms.end())
    {
        this->game_rooms[room_number] = GameState(0, 0, 1, 0, {});
    }

    std::cout << "Number of players in room " << room_number << ": " << game_rooms[room_number].number_of_players << std::endl;
    if (this->game_rooms[room_number].number_of_players >= 8)
    {
        send(player.socket_fd, "0", 1, 0); // Room is full, send 0 to the client
        return false;
    }

    this->game_rooms[room_number].number_of_players++;
    player.id = this->game_rooms[room_number].number_of_players;
    this->game_rooms[room_number].players.push_back(player);
    return true;
}

std::string Server::convert_game_state_to_bytes(const GameState &game_state)
{
    std::stringstream result_byte;

    result_byte << game_state.winner;
    result_byte << game_state.number_of_players;
    result_byte << game_state.who_to_move;

    for (const auto &player : game_state.players)
    {
        result_byte << std::left << std::setw(14) << std::setfill(' ') << player.name;
        result_byte << std::right << std::setw(2) << std::setfill('0') << player.cards_on_hand;
        result_byte << std::right << std::setw(2) << std::setfill('0') << player.cards_on_table;
        result_byte << std::right << std::setw(2) << std::setfill('0') << player.card_face_up;
        result_byte << std::right << std::setw(1) << std::setfill('0') << player.message;
    }

    // std::cout << "result_byte : " << result_byte.str() << std::endl;

    return result_byte.str();
}

void Server::broadcast_game_state(GameState &game_state)
{
    std::string game_state_bytes = convert_game_state_to_bytes(game_state);

    // std::cout << "Broadcasting game state: " << game_state_bytes << std::endl;
    std::cout << "Broadcasting game state" << std::endl;

    for (const Player &player : game_state.players)
    {
        if (player.card_face_up == -1)
            continue;
        // std::cout << "Sending to player: " << player.name << std::endl;
        send(player.socket_fd, game_state_bytes.c_str(), game_state_bytes.size(), 0);
    }

    // Set all messages to 0
    for (auto &player : game_state.players)
        player.message = 0;
}

void Server::put_new_card(GameState &game_state, int player_id)
{
    Player &current_player = game_state.players[player_id - 1];

    if (current_player.cards_on_hand != 0)
        this->new_card(game_state, current_player);

    this->who_to_move(game_state);
}

void Server::take_totem(GameState &game_state, int player_id)
{

    Player &current_player = game_state.players[player_id - 1];

    std::vector<Player *> players_with_same_card;
    for (auto &p : game_state.players)
        if (p.card_face_up != -1 && p.card_face_up / 5 == current_player.card_face_up / 5)
            players_with_same_card.push_back(&p);

    if (players_with_same_card.size() == 1)
    {

        std::cout << "Player " << current_player.name << "took the totem but shouldn't have!!!" << std::endl;
        current_player.message = 3; // not the same card

        for (auto &p : game_state.players)
        {
            if (p.card_face_up == -1)
                continue;
            current_player.cards_on_hand += p.cards_on_table;
            p.cards_on_table = 0;
            this->new_card(game_state, p);
        }
    }
    else
    {
        std::cout << "Player " << current_player.name << " took the totem!!! Distributing cards." << std::endl;
        current_player.message = 1; // took the totem (success)

        int numbers_of_cards_after_split = current_player.cards_on_table / (players_with_same_card.size() - 1);
        for (size_t i = 0; i < players_with_same_card.size(); ++i)
        {
            auto &p = *players_with_same_card[i];
            if (i != static_cast<size_t>(player_id - 1))
            {
                p.cards_on_hand += numbers_of_cards_after_split;
                p.cards_on_hand += p.cards_on_table;
                p.message = 2; // unfortunately someone took the totem, you receive cards
            }

            p.cards_on_table = 0;
            this->new_card(game_state, p);
        }
    }

    this->who_to_move(game_state);
}

void Server::new_card(GameState &game_state, Player &player)
{

    // std::cout << "Player " << player.name << "id= " << player.id << " got a new card" << std::endl;

    if (player.cards_on_hand == 0)
    {
        game_state.winner = player.id;
        std::cout << "Player " << player.name << player.id << " won the game" << std::endl;
        return;
    }

    player.cards_on_hand -= 1;
    player.cards_on_table += 1;
    player.card_face_up = std::rand() % NUMBER_OF_CARDS;
}