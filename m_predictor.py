import Lol as lol
import numpy as np
import pandas as pd
import time
import model


nick_main = ""


def main(summoner_id):

    spectacor = lol.Spectacor(summoner_id)  # Create Spectacor class object
    c_match = spectacor.current_match()  # Getting information about current game
    players = c_match["participants"]  # Getting informations about current game's players
    one = np.zeros(4)
    two = np.zeros(4)

    for i in players:
        nick = i["summonerName"]  # Getting current player nick
        print(nick)
        if nick == nick_main:
            player_team_id = i["teamId"]
        summoner2 = lol.Summoner(lol.check_nick(nick))  # Create Summoner's class object
        summoner_stats2  = summoner2.get_summoner_by_name() # Getting information about current player's account
        account_id2 = summoner2.get_stats("accountId", summoner_stats2) # Getting accountId
        match2 = lol.Match(account_id2) # Create Match class object
        match_list2 = match2.return_match_list("420", "11")  # Getting current player's match list
        if len(match_list2) > 10:
            match_list2 = match_list2[:10]
        statystyki = np.zeros((4,10))
        iterator = 0
        for j in match_list2:
            match_stats2 = match2.return_match_stats(j["gameId"])
            participants = match2.get_stats(match_stats2, "participantIdentities")
            participants_stats = match2.get_stats(match_stats2, "participants")
            game_duration = match2.get_stats(match_stats2, "gameDuration") / 60


            for participant, participant_stats in zip(participants, participants_stats): # Here, we get each statistics from match
                if participant["player"]["summonerName"] == nick:
                    stats = participant_stats["stats"]
                    statystyki[0][iterator] = stats["kills"] / game_duration
                    statystyki[1][iterator] = stats["deaths"] / game_duration
                    statystyki[2][iterator] = stats["assists"] / game_duration
                    statystyki[3][iterator] = stats["totalMinionsKilled"] / game_duration
                    break
            time.sleep(1)
            iterator += 1
        if i["teamId"] == 100:
            for s in range(len(one)) :
                one[s] += statystyki[s].sum() / 10
        else:
            for s in range(len(two)):
                two[s] += statystyki[s].sum() / 10
        print(nick)
        print("Średnie zabojstwa / min: ", statystyki[0].sum() / 10)
        print("Średnie śmiercii / min: ", statystyki[1].sum() / 10)
        print("Średnie asysyt / min: ", statystyki[2].sum() / 10)
        print("Średnie farma / min: ", statystyki[3].sum() / 10, "\n")

    one = one / 5
    two = two /5

    print('PODSUMOWANIE')
    print("Gracz ", nick_main, " jest w drużynie o ID ", player_team_id)
    print("Średnia różnica w statystykach drużyny o ID 100 i drużyny o ID 200 (T1 - T2) to: ")
    print("Średnie zabójstwa / min", one[0] - two[0])
    print("Średnie śmierci / min", one[1] - two[1])
    print("Średnie asysty / min", one[2] - two[2])
    print("Średnia farma / min", one[3] - two[3])
    return one - two


if __name__ == "__main__":
    nick_main = input("Wprowadź nazwe gracza: ")
    summoner = lol.Summoner(nick_main)
    summoner_stats = summoner.get_summoner_by_name()
    summoner_id_main = summoner.get_stats("id", summoner_stats)
    account_id = summoner.get_stats("accountId", summoner_stats)
    try:
        x2 = main(summoner_id_main)
        dane = pd.read_csv("learn_data.data", header=None, sep=" ")
        x = dane.iloc[0: dane.shape[0], 0: dane.shape[1] - 1].values
        y = dane.iloc[: dane.shape[0], dane.shape[1] - 1].values
        y = np.where(y, 1, -1)
        start_sec = time.gmtime().tm_sec
        start_min = time.gmtime().tm_min
        Model = model.Perceptron(0.00015, 30)
        Model.fit(x, y)
        end_sec = time.gmtime().tm_sec
        end_min = time.gmtime().tm_min
        print((end_min * 60 + end_sec) - start_min * 60 - start_sec )

        print("Wygra drużyna 100:", Model.predict(x2))
    except Exception as error:
        print(error)


