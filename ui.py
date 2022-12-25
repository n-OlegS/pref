class UI:
    def __init__(self):
        self.namedict = {}
        self.suits = 'pbkc'
        self.score = None
        self.playernames = None

    def request_game(self, code):
        if len(code) not in [1, 2, 6]:
            print("Invalid code.")
            return [1]

        if len(code) == 1:
            return [0, 2]
        elif len(code) == 2:
            if code[1] not in self.namedict:
                print("Invalid user")
                return [1]
            return [0, 3, self.namedict[code[1]]]
        else:
            player = self.namedict[code[1]]
            num = code[2]
            if num == "a": num = 10
            num = int(num)
            suit = self.suits.index(code[3])
            whist_1 = bool(code[4] == "w")
            whist_2 = bool(code[5] == "w")
            return [0, 1, [player, num, suit, whist_1, whist_2]]

    def request_save(self):
        if self.score.path_exists:
            self.score.save(self.score.path)
        else:
            try:
                self.score.save(input("Enter save path: "))
            except Exception:
                print("Invalid path...")
                self.request_save()

    def request_names(self):
        names = input("Enter names, separated by a space: ").split()
        self.playernames = names
        for i in range(3):
            self.namedict[names[i][0]] = i
        return 0, names

    def set_namedict(self, names):
        for i in range(3):
            self.namedict[names[i][0]] = i

        return 0

    @staticmethod
    def request_cost():
        cost = int(input("Enter the cost of one whist: "))
        return 0, cost

    @staticmethod
    def request_cap():
        cap = int(input("Enter bullet cap: "))
        return 0, cap

    @staticmethod
    def request_score():
        raw = input("Enter game scores: ")
        score = []

        if len(raw) != 3:
            print("Too many characters!")
            return 1

        for letter in raw:
            if letter not in "1234567890a":
                print("Invalid score")
                return 1
            if letter == "a":
                letter = 10

            score.append(int(letter))

        return [0, score]

    @staticmethod
    def cap(inp, length):
        inp = str(inp)
        if len(inp) > length:
            raise AttributeError
        else:
            return "0" * (length - len(inp)) + inp

    def show_score(self):
        score_list = self.score.get_scores()
        # cap
        score = f"----------------------------\n|    |   |   ||   |   |    |\n|    |   |   ||   |   |    |\n|{self.cap(score_list[0][2], 4)}|   |   ||   |   |{self.cap(score_list[2][3], 4)}|\n|    |   |   ||   |   |    |\n|    |   |{self.cap(score_list[0][0], 3)}||{self.cap(score_list[2][0], 3)}|   |    |\n|    |   |   ||   |   |    |\n|    |{self.cap(score_list[0][1], 3)}|   ||   |{self.cap(score_list[2][1], 3)}|    |\n|----|   |   ||   |   |----|\n|    |   |   ||   |   |    |\n|    |   |   ||   |   |    |\n|    |   |  /  \  |   |    |\n|{self.cap(score_list[0][3], 4)}|   | /{self.cap(score_list[1][0], 4)}\ |   |{self.cap(score_list[2][2], 4)}|\n|    |   |/------\|   |    |\n|    |   /        \   |    |\n|    |  /   {self.cap(score_list[1][1], 4)}   \  |    |\n|    | /            \ |    |\n|    |/--------------\|    |\n|    /        |       \    |\n|   /         |        \   |\n|  /    {self.cap(score_list[1][2], 4)}  |  {self.cap(score_list[1][3], 4)}   \  |\n| /           |          \ |\n|/            |           \|\n----------------------------\n"
        print(score)
        return 0
