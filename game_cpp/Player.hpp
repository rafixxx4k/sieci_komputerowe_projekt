#ifndef PLAYER_HPP
#define PLAYER_HPP

#include <string>

class Player
{
public:
    std::string name;
    int cards_on_hand;
    int cards_on_table;
    int card_face_up;
    int socket_fd;
    int id;

    Player()
    {
        name = "";
        cards_on_hand = 0;
        cards_on_table = 0;
        card_face_up = 0;
        socket_fd = 0;
        id = 0;
    }

    Player(std::string n, int hand, int table, int face_up, int fd, int id)
        : name(n), cards_on_hand(hand), cards_on_table(table), card_face_up(face_up), socket_fd(fd), id(id) {}
};

#endif // PLAYER_H
