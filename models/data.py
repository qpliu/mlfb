import datetime
import sqlite3

class Db:
    def __init__(self, file):
        self._conn = sqlite3.connect(file, detect_types=sqlite3.PARSE_DECLTYPES)
        return

    def __del__(self):
        self._conn.close()
        return

    def cursor(self):
        return self._conn.cursor()

    def games(self, with_snap_counts=False, with_week_1=True):
        min_year = 0
        if with_snap_counts:
            min_year = 2012
            pass
        omit_week = 1
        if with_week_1:
            omit_week = 0
            pass
        c = self._conn.cursor()
        c.execute('SELECT game_id FROM games WHERE year >= ? AND week <> ? ORDER BY year ASC, week ASC', (min_year,omit_week))
        return list(map(lambda x: Game(self, x[0]), c.fetchall()))

    def last_games(self, team_id, limit=4, as_of=(9999,1)):
        c = self._conn.cursor()
        c.execute('SELECT game_id FROM games WHERE (road_team_id = ? OR home_team_id = ?) AND (year < ? OR (year = ? AND week < ?)) ORDER BY year DESC, week DESC LIMIT ?', (team_id, team_id, as_of[0], as_of[0], as_of[1], limit))
        return list(map(lambda x: Game(self, x[0]), c.fetchall()))

    pass

class Game:
    def __init__(self, db, game_id):
        self._db = db
        self._game_id = game_id
        self._loaded = False
        return

    def load(self):
        if self._loaded:
            return
        c = self._db.cursor()
        c.execute('SELECT year, week, date, road_team_id, road_team_name, road_team_score, home_team_id, home_team_name, home_team_score FROM games WHERE game_id = ?', (self._game_id,))
        row = c.fetchone()
        self._year = row[0]
        self._week = row[1]
        self._date = row[2]
        self._road_team_id = row[3]
        self._road_team_name = row[4]
        self._road_team_score = row[5]
        self._home_team_id = row[6]
        self._home_team_name = row[7]
        self._home_team_score = row[8]
        self._loaded = True
        return

    def game_id(self):
        return self._game_id

    def game_time(self):
        self.load()
        return (self._year,self._week,self._date)

    def teams(self):
        self.load()
        return (self._road_team_id,self._home_team_id)

    def team_names(self):
        self.load()
        return (self._road_team_name,self._home_team_name)

    def score(self):
        self.load()
        return (self._road_team_score,self._home_team_score)

    def home_win(self):
        self.load()
        return self._home_team_score > self._road_team_score

    def target_data_win(self):
        if self.home_win():
            return 1
        else:
            return 0
        pass

    def target_data_score_total(self):
        return self._road_team_score + self._home_team_score

    def target_data_score_diff(self):
        return self._road_team_score - self._home_team_score

    def road_players(self):
        self.load()
        c = self._db.cursor()
        c.execute('SELECT player_id FROM game_player_pos WHERE game_id = ? AND team_id = ?', (self._game_id, self._road_team_id))
        return list(map(lambda x: Player(self._db, x[0]), c.fetchall()))

    def home_players(self):
        self.load()
        c = self._db.cursor()
        c.execute('SELECT player_id FROM game_player_pos WHERE game_id = ? AND team_id = ?', (self._game_id, self._home_team_id))
        return list(map(lambda x: Player(self._db, x[0]), c.fetchall()))

    def road_team_last_games(self, limit=4):
        self.load()
        return self._db.last_games(self._road_team_id, limit=limit, as_of=(self._year, self._week))

    def home_team_last_games(self, limit=4):
        self.load()
        return self._db.last_games(self._home_team_id, limit=limit, as_of=(self._year, self._week))

    def road_team_stat(self, stat, default=None):
        self.load()
        c = self._db.cursor()
        c.execute('SELECT stat_value FROM game_team_stats WHERE game_id = ? AND team_id = ? AND stat_name = ?', (self._game_id, self._road_team_id, stat))
        row = c.fetchone()
        if row == None:
            return default
        return row[0]

    def home_team_stat(self, stat, default=None):
        self.load()
        c = self._db.cursor()
        c.execute('SELECT stat_value FROM game_team_stats WHERE game_id = ? AND team_id = ? AND stat_name = ?', (self._game_id, self._home_team_id, stat))
        row = c.fetchone()
        if row == None:
            return default
        return row[0]

    pass

class Player:
    def __init__(self, db, player_id):
        self._db = db
        self._player_id = player_id
        self._loaded = False
        return

    def load(self):
        if self._loaded:
            return
        c = self._db.cursor()
        c.execute('SELECT name, pos, height, weight, dob, draft_pos FROM players WHERE player_id = ?', (self._player_id,))
        row = c.fetchone()
        self._name = row[0]
        self._pos = row[1]
        self._height = row[2]
        self._weight = row[3]
        self._dob = row[4]
        self._draft_pos = row[5]
        self._loaded = True
        return

    def player_id(self):
        return self._player_id

    def name(self):
        self.load()
        return self._name

    def pos(self, game=None):
        self.load()
        if not game:
            return self._pos
        c = self._db.cursor()
        c.execute('SELECT pos FROM game_player_pos WHERE game_id = ? AND player_id = ?', (game.game_id(), self._player_id))
        return c.fetchone()[0]

    def height(self):
        self.load()
        return self._height

    def weight(self):
        self.load()
        return self._weight

    def dob(self):
        self.load()
        return self._dob

    def draft_pos(self, undrafted=None):
        self.load()
        if self._draft_pos == None:
            return undrafted
        return self._draft_pos

    def age(self, game=None, date=None):
        self.load()
        if date != None:
            return (date - self._dob).days
        if game != None:
            return (game.game_time()[2] - self._dob).days
        return (datetime.date.today() - self._dob).days

    def last_games(self, game, limit=4):
        self.load()
        c = self._db.cursor()
        c.execute('SELECT games.game_id FROM games, game_player_pos WHERE games.game_id = game_player_pos.game_id AND player_id = ? AND ((year = ? AND week < ?) OR (year < ?)) ORDER BY year DESC, week DESC LIMIT ?', (self._player_id, game.game_time()[0], game.game_time()[1], game.game_time()[0], limit))
        return list(map(lambda x: Game(self._db, x[0]), c.fetchall()))

    def stat(self, game, stat, default=None):
        self.load()
        c = self._db.cursor()
        c.execute('SELECT stat_value FROM game_player_stats WHERE game_id = ? AND player_id = ? AND stat_name = ?', (game.game_id(), self._player_id, stat))
        row = c.fetchone()
        if row == None:
            return default
        return row[0]

    pass
