class Manager:
    def __init__(self, ui, score):
        self.ui = ui
        self.score = score
        self.pass_round = 1
        self.update = None

        self.cost_dict = {
            6: 2,
            7: 4,
            8: 6,
            9: 8,
            10: 10,
        }

        self.refer_dict = {
            "01": 3,
            "02": 2,
            "10": 2,
            "12": 3,
            "21": 2,
            "20": 3
        }

        self.half_whist = {
            6: 2,
            7: 1,
            8: 1,
            9: 1
        }

        self.full_whist = {
            6: 4,
            7: 2,
            8: 1,
            9: 1
        }

        """
        CODES:
            0 - IDLE
            1 - GAME
            2 - PASS
            3 - MISERE
        """

        self.state = 0

    def idle(self, command):
        self.state = 0
        game = self.ui.request_game(command)
        if game[0] == 1: return 1

        scores = self.ui.request_score()[1]

        if game[1] == 1:
            code = self.game(game[2], scores)
        elif game[1] == 2:
            code = self.game_pass(scores)
        else:
            code = self.game_misere(game[2], scores)

        if code:
            return 1
        return 0

    def game(self, pars, scores):
        self.pass_round = 1
        score = self.score.get_scores()
        # [player, num, suit, whist_1, whist_2]

        if not (pars[3] or pars[4]):
            score.bullet_write(pars[0], self.cost_dict[pars[1]])
            return

        success = False
        if scores[pars[0]] >= pars[1]: success = True

        ind = 3
        for i in [pars[0] - 1, pars[0] - 2]:
            k = i
            if k < 0: k += 3
            if not pars[ind]: continue

            score[k][self.refer_dict[str(i) + str(pars[0])]] += scores[i] * self.cost_dict[pars[1]]
            ind += 1

        self.score.set_scores(score)

        if success:
            self.score.bullet_write(pars[0], self.cost_dict[pars[1]])
            p1, p2 = [x for x in range(3) if x != pars[0]]
            completed = False

            if scores[p1] + scores[p2] >= self.full_whist[pars[1]]: completed = True

            if completed: return 0

            if pars[3] and pars[4]:
                for p in [p1, p2]:
                    if scores[p] < self.half_whist[pars[1]]:
                        score = self.score.get_scores()
                        score[p][0] += (self.half_whist[pars[1]] - scores[p]) * self.cost_dict[pars[1]]
                        self.score.set_scores(score)

            else:
                players = []
                i = pars[0] - 1

                for _ in range(2):
                    if i < 0: i = 2
                    players.append(i)
                    i -= 1

                p1, p2 = players

                if pars[3]:
                    p = p2
                else:
                    p = p1

                score = self.score.get_scores()
                score[p][0] += (self.full_whist[pars[1]] - scores[p]) * self.cost_dict[pars[1]]

            return 0

        else:
            # fine
            score = self.score.get_scores()
            score[pars[0]][0] += self.cost_dict[pars[1]] * (missed := (pars[1] - scores[pars[0]]))

            # consolation
            for i in range(3):
                if i != pars[0]:
                    score[i][self.refer_dict[str(i) + str(pars[0])]] += missed * self.cost_dict[pars[1]]

            self.score.set_scores(score)

            return 0

    def game_pass(self, scores):
        score = self.score.get_scores().copy()

        for i in range(3):
            score[i][0] += self.pass_round * scores[i]

        self.score.set_scores(score.copy())
        self.pass_round += 1

    def game_misere(self, pars, scores):
        self.pass_round = 1
        score = self.score.get_scores()
        played = False

        if scores[pars] == 0:
            played = True

        if played:
            self.score.bullet_write(pars, 10)
        else:
            score[pars][0] += 10 * scores[pars]
