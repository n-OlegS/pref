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

    """def game(self, pars, scores):
        self.pass_round = 1
        score = self.score.get_scores()
        # [player, num, suit, whist_1, whist_2]

        if not (pars[3] or pars[4]):
            score.bullet_write(pars[0], self.cost_dict[pars[1]])
            return

        success = False
        if scores[pars[0]] >= pars[1]: success = True

        ind = 2
        reserve = 0
        to_add = {0: 0, 1: 0, 2: 0}
        whister = -1

        for i in [pars[0] - 1, pars[0] - 2]:
            ind += 1
            k = i
            if k < 0: k += 3

            if not pars[ind]:
                if whister == -1:
                    reserve += scores[k]
                else:
                    to_add[whister] += scores[k]
                continue

            whister = k

            print("add to", k)

            to_add[k] += scores[k] + reserve

        for player_to_add in list(to_add.keys()):
            if to_add[player_to_add] == 0: continue
            score[player_to_add][self.refer_dict[str(player_to_add) + str(pars[0])]] += (to_add[player_to_add]) * self.cost_dict[pars[1]]

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
                print(f"Whisters: {players}")

                print(pars)

                if pars[3]:
                    p = p1
                else:
                    p = p2

                print(p)

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
    """

    def game(self, pars, scores):
        packed = self.pack(pars, scores)

        print(f'Packed: {packed}')

        self.process_game(packed)

        return 0

    def pack(self, pars, scores):
        # Input: [player, num, suit, whist_1, whist_2], [0, 7, 2] - scores
        # Output: [whisters: x, data: dict]
        output = {'whisters': 0, 'data': {}}

        if not (pars[3] or pars[4]):
            output['data'] = {'score_p': pars[1], 'player': pars[0]}
            return output

        elif not (pars[3] and pars[4]):
            output['whisters'] = 1
            data = {}
            data['req_p'] = pars[1]
            data['player_id'] = pars[0]

            ind = 2
            for i in [pars[0] - 1, pars[0] - 2]:
                ind += 1
                k = i
                if k < 0: k += 3

                if pars[ind]:
                    data['whister_id'] = k
                    break

            data['score_0'] = 0
            for i in [x for x in range(3) if x != pars[0]]:
                data['score_0'] += scores[i]

            data['score_p'] = scores[pars[0]]
            data['req_w'] = self.full_whist[pars[1]]

            output['data'] = data
            return output

        else:
            assert pars[3] and pars[4]
            output['whisters'] = 2
            data = {'req_p': pars[1]}

            whister_ids = []
            for i in [pars[0] - 1, pars[0] - 2]:
                k = i
                if k < 0: k += 3

                whister_ids.append(k)

            single_whist = (pars[1] in [8, 9])
            if single_whist: single_whister = whister_ids[-1]

            data['score_0'] = -1
            data['score_p'] = scores[pars[0]]
            data['score_1'] = scores[whister_ids[0]]
            data['score_2'] = scores[whister_ids[1]]
            if single_whist: data['score_0'] = sum([scores[x] for x in whister_ids])
            if single_whist: output['whisters'] = 1

            data['req_1'] = self.half_whist[pars[1]]
            data['req_2'] = self.half_whist[pars[1]]
            data['req_0'] = self.full_whist[pars[1]]

            data['single_whist'] = single_whist
            data['whister_ids'] = whister_ids

            output['data'] = data

            return output

    def process_game(self, packed):
        # Input: [whisters: x, data: dict]
        data = packed['data']

        if packed['whisters'] == 0:
            player = data['player']
            game = data['score_p']
            update = self.score.get_score_template()

            update[player][1] = self.cost_dict[game]

            self.score.receive_update(update)

            return 0

        elif packed['whisters'] == 1:
            if data['req_p'] == data['score_p']:
                update = self.score.get_score_template()
                player = data['player_id']
                whister = data['whister_id']

                update[player][1] = self.cost_dict[data['score_p']]
                update[whister][self.refer_dict[str(whister) + str(player)]] = self.full_whist(data['score_p']) * \
                                                                               self.cost_dict[data['score_p']]

                self.score.receive_update(update)

            elif data['score_p'] < data['req_p']:
                consolation = data['req_p'] - data['score_p']
                whister = data['whister_id']
                player = data['player_id']
                passer = [i for i in range(3) if i not in [whister, player]][0]

                update = self.score.get_score_template()
                update[passer][self.refer_dict[str(passer) + str(player)]] += self.cost_dict[
                                                                                  data['req_p']] * consolation
                update[whister][self.refer_dict[str(whister) + str(player)]] += self.cost_dict[data['req_p']] * (
                            consolation + data['score_0'])
                update[player][0] += self.cost_dict[data['req_p']] * consolation

                self.score.receive_update(update)

            else:
                assert data['score_p'] > data['req_p']

                update = self.score.get_score_template()
                player = data['player_id']
                whister = data['whister_id']

                update[player][1] += self.cost_dict[data['req_p']]
                update[whister][0] += self.cost_dict[data['req_p']] * (data['req_w'] - data['score_0'])
                update[whister][self.refer_dict[str(whister) + str(player)]] += self.cost_dict[data['req_p']] * data[
                    'score_0']

                self.score.receive_update(update)

        else:
            if data['score_p'] <= data['req_p']:
                consolation = data['req_p'] - data['score_p'] * self.cost_dict[data['req_p']]
                update = self.score.get_score_template()

                for w in data['whister_ids']: update[w][
                    self.refer_dict[str(w) + str(data['player_id'])]] += consolation + self.cost_dict[data['req_p']] * \
                                                                         data[f'score_{w + 1}']
                update[data['player_id']][0] += consolation

                self.score.receive_update(update)

            else:
                update = self.score.get_score_template()
                update[data['player_id']][1] += self.cost_dict[data['req_p']]

                for w in data['whister_ids']: update[w][self.refer_dict[str(w) + str(data['player_id'])]] += \
                self.cost_dict[data['req_p']] * data[f'score_{w + 1}']

                if data['single_whist']:
                    update[data['single_whister']][0] += self.cost_dict[data['req_p']] * (
                                data['req_0'] - data['score_0'])
                else:
                    for w in data['whister_ids']:
                        update[w][0] += (self.half_whist[data['req_p']] - data[f'score_{w + 1}']) * self.cost_dict[
                            data['req_p']]

                self.score.receive_update(update)

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
