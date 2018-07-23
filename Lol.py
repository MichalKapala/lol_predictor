import urllib.request as request
import urllib.parse
import json
import time
api_key = "RGAPI-4bbbb465-6338-4889-b600-62c03c387f46"
region = "eun1"


def return_response(url):
    response = request.urlopen(url)
    charset = response.headers.get_content_charset()
    response = response.read().decode(charset, "replace")
    response = response.replace("\\", "")
    response = json.loads(response)
    return response


def check_nick(nick):
    nick = urllib.parse.quote_plus(nick)
    nick = nick.replace("+", "%20")
    return nick

class Summoner():
    def __init__(self, summonerName):
        self.summonerName = summonerName

    def get_summoner_by_name(self):
        url =  "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + str(self.summonerName) + "?api_key=" + api_key
        return return_response(url)

    def get_summoner_by_summonerId(self, summonerId):
        url = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/" + str(summonerId) + "?api_key=" + api_key
        return return_response(url)

    def get_summoner_by_accountId(self, accountId):
        url = "https://" + region + "api.riotgames.com/lol/summoner/v3/summoners/by-account/" + str(accountId) + "?api_key=" + api_key
        return return_response(url)

    def get_stats(self, key, stats):
        try:
            return stats[key]
        except Exception as error:
            return error


class Match():
    def __init__ (self, accountId):
        self.accounId = accountId

    def return_match_list(self, queue, season):
        url = "https://" + region + ".api.riotgames.com/lol/match/v3/matchlists/by-account/"+ str(self.accounId) + "?queue="+ queue + "&season=" + season + "&api_key=" + api_key
        return return_response(url)["matches"]

    def return_match_stats(self, gameId, key=None):
        url = "https://" + region + ".api.riotgames.com/lol/match/v3/matches/" + str(gameId) + "?api_key=" + api_key
        return return_response(url)

    def get_stats(self, stats, key):
        try:
            return stats[key]
        except Exception as error:
            return error

    def stats(self, players_stats, key):
        team_win = 0
        team_lose = 0
        for i in players_stats:
            player = i['stats']
            if(player["win"] == True):
                team_win += player[key]
            else:
                team_lose += player[key]
        return team_win - team_lose


class Spectacor():
    def __init__(self, summonerId):
        self.summonerId = summonerId

    def current_match(self):
        url = "https://" + region +  ".api.riotgames.com/lol/spectator/v3/active-games/by-summoner/" + str(self.summonerId) + "?api_key=" + api_key
        return return_response(url)

def save_to_file(stats):
    file = open("Content2.txt", "a")
    for i in range(len(stats)):
        if i != len(stats) - 1:
            file.write(str(stats[i]) + " ")
        else:
            file.write(str(stats[i]))
    file.write("\n")
    file.close()

def read_summoners():
    file = open("Nicki2.data", "r")
    summoners = file.readlines()
    nicks = []
    for i in summoners:
        name = i.replace("league of legends player	", "")
        name = name[: len(name) - 1]
        nicks.append(name)
    return nicks


def main(nick):
    summoner = Summoner(check_nick(nick))
    summoner_id = summoner.get_stats("accountId", summoner.get_summoner_by_name())
    match = Match(str(summoner_id))
    match_list = match.return_match_list("420", "11")
    if len(match_list) > 30:
        match_list = match_list[:30]

    for i in match_list:
        dane = []
        dane2 = []
        match_id = str(i["gameId"])
        match_stats = match.return_match_stats(match_id)
        match_stats = match.get_stats(match_stats, "participants")
        game_duration = match.return_match_stats(match_id) # get game duration [minutes]
        game_duration = game_duration["gameDuration"] / 60
        dane.append(match.stats(match_stats, "kills") / game_duration)
        dane.append(match.stats(match_stats, "deaths") / game_duration)
        dane.append(match.stats(match_stats, "assists") / game_duration)
        dane.append(match.stats(match_stats, "totalMinionsKilled") / game_duration)
        dane.append(1)
        for di in dane:
            dane2.append(str(-1 * di))
        save_to_file(dane)
        save_to_file(dane2)

        print("Gra: ", match_id)
        print(dane)
        time.sleep(1)

if __name__ == "__main__":
    for nick in read_summoners():
        try:
            print(nick)
            main(nick)
            time.sleep(30)
        except Exception as error:
            print(error)
