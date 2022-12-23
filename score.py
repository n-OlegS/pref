from ui import UI


class Score:
    def __init__(self, ui, state=None):
        self.ui = ui

        if state is None:
            pnames = self.ui.request_names()[1]
            cap = self.ui.request_cap()[1]
            pscores = [[0, 0, 0, 0] for _ in range(3)]
            cost = self.ui.request_cost()[1]

        else:
            pass

        self.pnames = pnames
        self.pscores = pscores
        self.cost = cost
        self.bullet_cap = cap

    def __str__(self):
        return "Method should be called with UI!"

    def get_scores(self):
        return self.pscores.copy()

    def set_scores(self, scores):
        self.pscores = scores.copy()

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
            self.ui.display_endgame()

            return 0
