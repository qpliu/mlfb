# model1 inputs
#
# 0: road team days since last game (capped at 18 e.g. for week 1)
# 1: road team wins in last 4 games
# 2: road team yards gained in last 4 games
# 3: road team yards allowed in last 4 games
# 4: road team points scored in last 4 games
# 5: road team points allowed in last 4 games
# 6: home team days since last game (capped at 18 e.g. for week 1)
# 7: home team wins in last 4 games
# 8: home team yards gained in last 4 games
# 9: home team yards allowed in last 4 games
# 10: home team points scored in last 4 games
# 11: home team points allowed in last 4 games

class Model:
    def __init__(self, db):
        self._db = db
        self._n = 4
        pass

    def name(self):
        return "model1"

    def need_snap_counts(self):
        return False

    def with_week_1(self):
        return True

    def need_history_size(self):
        return self._n

    def input_dim(self):
        return 12

    def neurons(self):
        return (120,64,64)

    def epochs(self):
        return (5000,1000)

    def _set_input_data(self, year, week, date, team_id, input_data, row_index, column_offset):
        games = self._db.last_games(team_id, limit=self._n, as_of=(year,week))
        input_data[row_index, column_offset] = min((date - games[0].game_time()[2]).days, 18)
        input_data[row_index, column_offset+1] = 0
        input_data[row_index, column_offset+2] = 0
        input_data[row_index, column_offset+3] = 0
        input_data[row_index, column_offset+4] = 0
        input_data[row_index, column_offset+5] = 0
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
            pass
        pass

    def set_input_data(self, year, week, date, road_team_id, home_team_id, input_data, row_index):
        self._set_input_data(year, week, date, road_team_id, input_data, row_index, 0)
        self._set_input_data(year, week, date, home_team_id, input_data, row_index, 6)
        pass
