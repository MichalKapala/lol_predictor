import Lol as lol
import numpy as np
import pandas as pd
import time
import model



class MainPredictor():
    def __init__(self):
        self.public_team_stats = None
        self.stats_collected = False
        self.player_team_id = 100
        self.public_current_stats = []
        self.error = ""
        self.terminate = False

    def stats(self, nick_main):
        try:
            iterator_global1 = 0
            iterator_global2 = 0
            summoner = lol.Summoner(nick_main)
            summoner_stats = summoner.get_summoner_by_name()
            summoner_id = summoner.get_stats("id", summoner_stats)
            account_id = summoner.get_stats("accountId", summoner_stats)
            spectacor = lol.Spectacor(summoner_id)  # Create Spectacor class object
            c_match = spectacor.current_match()  # Getting information about current game
            players = c_match["participants"]  # Getting informations about current game's players
            players = [players[0],players[5], players[1], players[6], players[2], players[7], players[3], players[8], players[4], players[9]]
            self.one = np.zeros(4)
            self.two = np.zeros(4)
            self.public_stats1 = np.zeros(4)
            self.public_stats2 = np.zeros(4)
            self.iterator_one = 0
            self.iterator_two = 0
            self.c_nick1 = ""
            self.c_nick2 = ""
            for i in players:
                if not self.terminate:
                    nick = i["summonerName"]  # Getting current player nick
                    if nick == nick_main:
                        self.player_team_id = i["teamId"]
                    summoner2 = lol.Summoner(nick)  # Create Summoner's object
                    summoner_stats2 = summoner2.get_summoner_by_name()  # Getting information about current player's account
                    account_id2 = summoner2.get_stats("accountId", summoner_stats2)  # Getting accountId
                    match2 = lol.Match(account_id2)  # Create Match object
                    match_list2 = match2.return_match_list("420", "11")  # Getting current player's match list
                    if len(match_list2) > 10:
                        match_list2 = match_list2[:10]
                    iterator = 0
                    for j in match_list2:
                        if not self.terminate:
                            statystyki = np.zeros(4)
                            self.public_current_stats1 = []
                            self.public_current_stats2 = []
                            match_stats2 = match2.return_match_stats(j["gameId"])
                            participants = match2.get_stats(match_stats2, "participantIdentities")
                            participants_stats = match2.get_stats(match_stats2, "participants")
                            game_duration = match2.get_stats(match_stats2, "gameDuration") / 60
                            for participant, participant_stats in zip(participants,
                                                                      participants_stats):  # Here, we get each statistics from match
                                if not self.terminate:
                                    if participant["player"]["summonerName"] == nick:
                                        stats = participant_stats["stats"]
                                        statystyki[0] += stats["kills"] / game_duration
                                        statystyki[1] += stats["deaths"] / game_duration
                                        statystyki[2] += stats["assists"] / game_duration
                                        statystyki[3] += stats["totalMinionsKilled"] / game_duration
                                        break
                            time.sleep(1)
                            iterator += 1
                            if i["teamId"] == 100:
                                iterator_global1 += 1
                                self.c_nick1 = nick
                                for s in range(len(self.one)):
                                    self.one[s] += statystyki[s]
                            else:
                                iterator_global2 += 1
                                self.c_nick2 = nick
                                for s in range(len(self.two)):
                                    self.two[s] += statystyki[s]

                            if iterator_global1 > 0:
                                self.public_stats1 = self.one / iterator_global1
                            if iterator_global2 > 0:
                                self.public_stats2 = self.two / iterator_global2

                if i["teamId"] == 100:
                    self.iterator_one += 1
                else:
                    self.iterator_two += 1

            self.stats_collected = True
            self.terminate = False
        except Exception as er:
            self.error = str(er)
            print(self.error)



    def predicttion(self, stats):
        try:
            x2 = stats
            dane = pd.read_csv("Data/learnt_data7.data", header=None, sep=" ")
            x = dane.iloc[0: dane.shape[0], 0: dane.shape[1] - 1].values
            y = dane.iloc[: dane.shape[0], dane.shape[1] - 1].values
            y = np.where(y, 1, -1)

            Model = model.Perceptron(0.00015, 30, True)
            Model.fit(x, y)
            return Model.predict(x2)

        except Exception as error:
            return error


