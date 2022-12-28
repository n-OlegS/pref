import json


class Score:
    def __init__(self, ui, state=None):
        self.ui = ui
        self.path_exists = bool(state is not None)
        self.path = state

        self.refer_dict = {
            "01": 3,
            "02": 2,
            "10": 2,
            "12": 3,
            "21": 2,
            "20": 3
        }

        if state is None:
            pnames = self.ui.request_names()[1]
            cap = self.ui.request_cap()[1]
            pscores = [[0, 0, 0, 0] for _ in range(3)]
            cost = self.ui.request_cost()[1]

            self.pnames = pnames
            self.pscores = pscores
            self.cost = cost
            self.bullet_cap = cap

        else:
            state_d = json.load(open(state, 'r'))

            self.pnames = state_d["names"]
            self.pscores = state_d["scores"]
            self.cost = state_d["cost"]
            self.bullet_cap = state_d["cap"]

            self.ui.set_namedict(self.pnames)
            self.ui.playernames = self.pnames.copy()

    def __str__(self):
        return "Method should be called with UI!"

    def save(self, path):
        # Form dict

        state = {
            "names": self.pnames,
            "scores": self.pscores,
            "cost": self.cost,
            "cap": self.bullet_cap
        }

        json.dump(state, open(path, 'w'))

        return 0

    def get_scores(self):
        return self.pscores.copy()

    def set_scores(self, scores):
        self.pscores = scores.copy()

    def calculate_final_score(self):
        assert list(set([self.pscores[x][1] for x in range(3)])) == [self.bullet_cap]

        # Subtract min heap

        scores = self.get_scores()
        min_heap = min([self.pscores[x][0] for x in range(3)])
        for player in range(3):
            scores[player][0] -= min_heap

        # Convert heap to whists

        for player in range(3):
            x = scores[player][0] % 3

            to_add = 10 * (added := ((3 - x) % 3))

            scores[player][0] += added
            scores[player][2] += to_add
            scores[player][3] += to_add

            scores[player][0] /= 3
            scores[player][0] *= 10

            for i in range(3):
                if i == player: continue
                scores[i][self.refer_dict[str(i) + str(player)]] += scores[player][0]

        finals = []
        for _ in range(3): finals.append([0, 0])

        for i in range(3):
            right = i + 1
            left = i - 1
            if left < 0: left += 3
            if right > 2: right -= 3

            finals[i][0] = scores[i][2] - scores[left][3]
            finals[i][1] = scores[i][3] - scores[right][2]

        return finals

    def bullet_write(self, player, amount):
        score = self.get_scores()

        if self.pscores[player][1] + amount <= self.bullet_cap:
            score[player][1] += amount
            self.set_scores(score)
        else:
            score[player][1] = self.bullet_cap
            amount -= (self.bullet_cap - self.pscores[player][1])
            bullets = [(x, score[x][1]) for x in range(3) if x != player]
            bullets.sort(key=lambda x: x[1])
            min_bullet = bullets[0]

            if self.pscores[min_bullet[0]][1] + amount <= self.bullet_cap:
                score[min_bullet[0]][1] += amount
                return 0

            amount -= (self.bullet_cap - self.pscores[min_bullet[0]][1])
            score[min_bullet[0]][1] = self.bullet_cap

            if self.pscores[bullets[1][0]][1] + amount <= self.bullet_cap:
                score[bullets[1][0]] += amount
                return 0

            amount -= (self.bullet_cap - self.pscores[bullets[1][0]][1])
            score[bullets[1][0]][2] += amount * 10
            score[bullets[1][0]][3] += amount * 10

            self.set_scores(score)

        score = self.get_scores()
        if len([1 for x in range(3) if score[x][1] == self.bullet_cap]) == 3:
            finals = self.calculate_final_score()
            self.ui.display_endgame(finals)

        return 0
