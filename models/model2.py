# model2 inputs
#
# 0: road team days since last game (capped at 18 e.g. for week 1)
# 1: road team wins in last 4 games
# 2: road team yards gained in last 4 games
# 3: road team yards allowed in last 4 games
# 4: road team points scored in last 4 games
# 5: road team points allowed in last 4 games
# 6: road team qb age
# 7: road team qb height
# 8: road team qb weight
# 9: road team qb draft position
# 10: road team qb pass_cmp in last 4 games
# 11: road team qb pass_att in last 4 games
# 12: road team qb pass_yds in last 4 games
# 13: road team qb pass_td in last 4 games
# 14: road team qb pass_int in last 4 games
# 15: road team qb pass_sacked in last 4 games
# 16: road team qb pass_sacked_yds in last 4 games
# 17: road team qb pass_rating in last 4 games
# 18: road team qb rush_att in last 4 games
# 19: road team qb rush_yds in last 4 games
# 20: road team qb rush_td in last 4 games
# 21: road team rb1 rush_att in last 4 games
# 22: road team rb1 rush_yds in last 4 games
# 23: road team rb1 rush_td in last 4 games
# 24: road team rb2 rush_att in last 4 games
# 25: road team rb2 rush_yds in last 4 games
# 26: road team rb2 rush_td in last 4 games
# 27: home team days since last game (capped at 18 e.g. for week 1)
# 28: home team wins in last 4 games
# 29: home team yards gained in last 4 games
# 30: home team yards allowed in last 4 games
# 31: home team points scored in last 4 games
# 32: home team points allowed in last 4 games
# 33: home team qb age
# 34: home team qb height
# 35: home team qb weight
# 36: home team qb draft position
# 37: home team qb pass_cmp in last 4 games
# 38: home team qb pass_att in last 4 games
# 39: home team qb pass_yds in last 4 games
# 40: home team qb pass_td in last 4 games
# 41: home team qb pass_int in last 4 games
# 42: home team qb pass_sacked in last 4 games
# 43: home team qb pass_sacked_yds in last 4 games
# 44: home team qb pass_rating in last 4 games
# 45: home team qb rush_att in last 4 games
# 46: home team qb rush_yds in last 4 games
# 47: home team qb rush_td in last 4 games
# 48: home team rb1 rush_att in last 4 games
# 49: home team rb1 rush_yds in last 4 games
# 50: home team rb1 rush_td in last 4 games
# 51: home team rb2 rush_att in last 4 games
# 52: home team rb2 rush_yds in last 4 games
# 53: home team rb2 rush_td in last 4 games

class Model:
    def __init__(self, db):
        self._db = db
        self._n = 4
        pass

    def name(self):
        return "model2"

    def need_snap_counts(self):
        return True

    def with_week_1(self):
        return True

    def need_history_size(self):
        return self._n

    def input_dim(self):
        return 54

    def neurons(self):
        return (120,64,64)

    def epochs(self):
        return (500,10000,10000)

    def _set_input_data(self, year, week, date, team_id, input_data, row_index, column_offset):
        games = self._db.last_games(team_id, limit=self._n, as_of=(year,week))
        input_data[row_index, column_offset] = min((date - games[0].game_time()[2]).days, 18)
        input_data[row_index, column_offset+1] = 0
        input_data[row_index, column_offset+2] = 0
        input_data[row_index, column_offset+3] = 0
        input_data[row_index, column_offset+4] = 0
        input_data[row_index, column_offset+5] = 0
        input_data[row_index, column_offset+6] = 0
        input_data[row_index, column_offset+7] = 0
        input_data[row_index, column_offset+8] = 0
        input_data[row_index, column_offset+9] = 0
        input_data[row_index, column_offset+10] = 0
        input_data[row_index, column_offset+11] = 0
        input_data[row_index, column_offset+12] = 0
        input_data[row_index, column_offset+13] = 0
        input_data[row_index, column_offset+14] = 0
        input_data[row_index, column_offset+15] = 0
        input_data[row_index, column_offset+16] = 0
        input_data[row_index, column_offset+17] = 0
        input_data[row_index, column_offset+18] = 0
        input_data[row_index, column_offset+19] = 0
        input_data[row_index, column_offset+20] = 0
        input_data[row_index, column_offset+21] = 0
        input_data[row_index, column_offset+22] = 0
        input_data[row_index, column_offset+23] = 0
        input_data[row_index, column_offset+24] = 0
        input_data[row_index, column_offset+25] = 0
        input_data[row_index, column_offset+26] = 0

        qb = None
        rb1 = None
        rb2 = None
        if games[0].teams()[0] == team_id:
            players = games[0].road_players()
            pass
        else:
            players = games[0].home_players()
            pass
        for p in players:
            pos = p.pos(games[0])
            if pos == 'QB':
                if qb == None or qb.stat(games[0], 'offense') < p.stat(games[0], 'offense'):
                    qb = p
                pass
            elif pos == 'RB':
                if rb1 == None or rb1.stat(games[0], 'offense') < p.stat(games[0], 'offense'):
                    rb2 = rb1
                    rb1 = p
                    pass
                elif rb2 == None or rb2.stat(games[0], 'offense') < p.stat(games[0], 'offense'):
                    rb2 = p
                    pass
                pass
            pass

        if qb != None:
            input_data[row_index, column_offset+6] = int(qb.age(date=date)/365.25)
            input_data[row_index, column_offset+7] = qb.height()
            input_data[row_index, column_offset+8] = round(qb.weight(),-1)
            input_data[row_index, column_offset+9] = qb.draft_pos(undrafted=400)
            pass

        for g in games:
            (road_team_id,home_team_id) = g.teams()
            (road_team_score,home_team_score) = g.score()
            road_team_yards = int(g.road_team_stat("Total Yards"))
            home_team_yards = int(g.home_team_stat("Total Yards"))
            if team_id == home_team_id:
                if home_team_score > road_team_score:
                    input_data[row_index, column_offset+1] += 1
                    pass
                input_data[row_index, column_offset+2] += home_team_yards
                input_data[row_index, column_offset+3] += road_team_yards
                input_data[row_index, column_offset+4] += home_team_score
                input_data[row_index, column_offset+5] += road_team_score
                pass
            else:
                if road_team_score > home_team_score:
                    input_data[row_index, column_offset+1] += 1
                    pass
                input_data[row_index, column_offset+2] += road_team_yards
                input_data[row_index, column_offset+3] += home_team_yards
                input_data[row_index, column_offset+4] += road_team_score
                input_data[row_index, column_offset+5] += home_team_score
                pass
            if qb != None:
                input_data[row_index, column_offset+10] += qb.stat(g, 'pass_cmp', default=0)
                input_data[row_index, column_offset+11] += qb.stat(g, 'pass_att', default=0)
                input_data[row_index, column_offset+12] += qb.stat(g, 'pass_yds', default=0)
                input_data[row_index, column_offset+13] += qb.stat(g, 'pass_td', default=0)
                input_data[row_index, column_offset+14] += qb.stat(g, 'pass_int', default=0)
                input_data[row_index, column_offset+15] += qb.stat(g, 'pass_sacked', default=0)
                input_data[row_index, column_offset+16] += qb.stat(g, 'pass_sacked_yds', default=0)
                input_data[row_index, column_offset+17] += qb.stat(g, 'pass_rating', default=0)
                input_data[row_index, column_offset+18] += qb.stat(g, 'rush_att', default=0)
                input_data[row_index, column_offset+19] += qb.stat(g, 'rush_yds', default=0)
                input_data[row_index, column_offset+20] += qb.stat(g, 'rush_td', default=0)
                pass
            if rb1 != None:
                input_data[row_index, column_offset+21] += rb1.stat(g, 'rush_att', default=0)
                input_data[row_index, column_offset+22] += rb1.stat(g, 'rush_yds', default=0)
                input_data[row_index, column_offset+23] += rb1.stat(g, 'rush_td', default=0)
                pass
            if rb2 != None:
                input_data[row_index, column_offset+24] += rb2.stat(g, 'rush_att', default=0)
                input_data[row_index, column_offset+25] += rb2.stat(g, 'rush_yds', default=0)
                input_data[row_index, column_offset+26] += rb2.stat(g, 'rush_td', default=0)
                pass
            pass
        input_data[row_index, column_offset+2] //= 50
        input_data[row_index, column_offset+3] //= 50
        input_data[row_index, column_offset+12] //= 50
        input_data[row_index, column_offset+22] //= 10
        input_data[row_index, column_offset+25] //= 10
        pass

    def set_input_data(self, year, week, date, road_team_id, home_team_id, input_data, row_index):
        self._set_input_data(year, week, date, road_team_id, input_data, row_index, 0)
        self._set_input_data(year, week, date, home_team_id, input_data, row_index, 27)
        pass
