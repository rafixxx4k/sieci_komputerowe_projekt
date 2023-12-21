import random


class Messages:
    answers = {
        0: [" "],
        1: [
            "Wziąłeś totem",
            "Udało ci się wyrwać totem",
            "Po prostu wziąłeś totem",
            "Wziąłeś totem, ale nie wiem czy to humanitarne zagranie",
            "W elegancki sposób, popijając herbatkę chwyciłeś totem",
            "Wszyscy rzucili się na totem, ale ty byłeś najszybszy",
            "Zagadałeś wszystkich i wziąłeś totem",
            "Totem po prostu wpadł ci w ręce",
            "Dzwoń po ambulans, ale nie dlamnie tylko dla przeciwników, bo wziąłem totem",
        ],
        2: [
            "Ktoś wyrwał ci totem",
            "Po prostu zaspałeś",
            "Jak ninja twój przeciwnik wyskoczył z cienia i zabrał totem",
            "Przeciwnik zabrał ci totem",
            "Przeciwnik zabrał ci totem, ale nie wiem czy to humanitarne zagranie",
            "Po co wstawałeś, i tak nie miałeś szans",
            "Nie tym razem, ale nie mart się to tylko gra",
        ],
        3: [
            "Niestety to nie te same karty",
            "Coś chyba zaburza twoją percepcję rzeczywistości",
            "Brawo, byłeś pierwszy w kolejce po więcej kart",
            "W tej grze trzeba być szybkim i spostrzegawczym, a tobie tego drugiego brakuje",
        ],
    }

    @staticmethod
    def get(message):
        return random.choice(Messages.answers[message])
