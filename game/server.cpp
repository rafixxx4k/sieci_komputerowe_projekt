#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <thread>
#include <random>
#include <netinet/in.h>
#include <unistd.h>
#include <unordered_map>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

// Constants
const int NUMBER_OF_CARDS = 19;

// Player class
class Player
{
public:
    std::string name;
    int cards_on_hand;
    int cards_on_table;
    int card_face_up;
    int socket_fd;

    Player()
    {
        name = "";
        cards_on_hand = 0;
        cards_on_table = 0;
        card_face_up = 0;
        socket_fd = 0;
    }

    Player(std::string n, int hand, int table, int face_up, int fd)
        : name(n), cards_on_hand(hand), cards_on_table(table), card_face_up(face_up), socket_fd(fd) {}
};

// GameState class
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

// // Dictionary to store game state for each room
// std::unordered_map<int, GameState> game_rooms;

// // Function to handle login
// std::pair<int, Player> handle_login(const char *data, int client_socket)
// {
//     int room_number = std::stoi(std::string(data, 4));
//     std::string player_name(data + 4, 14);
//     Player player(player_name, 12, 1, std::rand() % (NUMBER_OF_CARDS + 1), client_socket);
//     return std::make_pair(room_number, player);
// }

// // Function to handle player joining a room
// bool handle_room(int room_number, Player &player)
// {
//     if (game_rooms.find(room_number) == game_rooms.end())
//     {
//         game_rooms[room_number] = GameState(0, 0, 1, 0, {});
//     }

//     if (game_rooms[room_number].number_of_players >= 8)
//     {
//         send(player.socket_fd, "0", 1, 0); // Room is full, send 0 to the client
//         return false;
//     }

//     game_rooms[room_number].players.push_back(player);
//     game_rooms[room_number].number_of_players++;
//     return true;
// }

// // Function to handle client communication
// void handle_client(int client_socket)
// {
//     char data[32];
//     ssize_t bytes_received;

//     // Receive login data
//     bytes_received = recv(client_socket, data, sizeof(data), 0);
//     if (bytes_received <= 0)
//     {
//         close(client_socket);
//         return;
//     }

//     int room_number;
//     Player player;
//     std::tie(room_number, player) = handle_login(data, client_socket);

//     if (!handle_room(room_number, player))
//     {
//         close(client_socket);
//         return;
//     }

//     int player_id = game_rooms[room_number].number_of_players;
//     send(client_socket, std::to_string(player_id).c_str(), sizeof(int), 0);
//     // Broadcast game state
//     // broadcast_game_state(game_rooms[room_number]);

//     while (true)
//     {
//         bytes_received = recv(client_socket, data, sizeof(data), 0);
//         if (bytes_received <= 0)
//         {
//             close(client_socket);
//             return;
//         }

//         if (std::string(data, 1) == "c")
//         {
//             // new_card(game_rooms[room_number], player);
//         }
//         else if (std::string(data, 1) == "t")
//         {
//             // take_totem(game_rooms[room_number], player, player_id - 1);
//         }
//     }
// }

// Function to start the server
void start_server()
{
    int server_socket, client_socket;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len = sizeof(client_addr);
    std::srand(static_cast<unsigned int>(std::time(nullptr)));

    // Create socket
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1)
    {
        std::cerr << "Error creating server socket" << std::endl;
        exit(1);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(1100);

    // Bind socket
    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1)
    {
        std::cerr << "Error binding server socket" << std::endl;
        close(server_socket);
        exit(1);
    }

    // Listen for incoming connections
    if (listen(server_socket, 5) == -1)
    {
        std::cerr << "Error listening for connections" << std::endl;
        close(server_socket);
        exit(1);
    }

    std::cout << "Server listening on port 1100" << std::endl;

    while (true)
    {
        client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_addr_len);
        if (client_socket == -1)
        {
            std::cerr << "Error accepting client connection" << std::endl;
            continue;
        }

        std::cout << "Accepted connection from " << inet_ntoa(client_addr.sin_addr) << std::endl;

        // // Start a new thread to handle the client
        // std::thread client_thread(handle_client, client_socket);
        // client_thread.detach(); // Detach the thread to run independently
    }
}

int main()
{
    start_server();
    return 0;
}
