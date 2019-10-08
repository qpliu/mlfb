package main

import (
	"database/sql"
	"os"

	_ "github.com/mattn/go-sqlite3"
)

func main() {
	if len(os.Args) != 2 {
		panic("Usage: create_db db_file < data")
	}
	db, err := sql.Open("sqlite3", os.Args[1])
	if err != nil {
		panic(err)
	}

	if err := createSchema(db); err != nil {
		panic(err)
	}
}

func createSchema(db *sql.DB) error {
	tx, err := db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	for _, stmt := range []string{
		`CREATE TABLE players (
                    player_id VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(256),
                    pos VARCHAR(10),
                    height INTEGER,
                    weight INTEGER,
                    dob DATE,
                    draft_pos INTEGER
                    )`,
		`CREATE TABLE teams (team_id VARCHAR(3) PRIMARY KEY)`,
		`CREATE TABLE games (
                    game_id VARCHAR(12) PRIMARY KEY,
                    year INTEGER,
                    week INTEGER,
                    date DATE,
                    road_team_id VARCHAR(3),
                    road_team_name VARCHAR(64),
                    road_team_score INTEGER,
                    home_team_id VARCHAR(3),
                    home_team_name VARCHAR(64),
                    home_team_score INTEGER,
                    FOREIGN KEY (road_team_id) REFERENCES teams(team_id),
                    FOREIGN KEY (home_team_id) REFERENCES teams(team_id)
                    )`,
		`CREATE INDEX games_year_week ON games(year,week)`,
		`CREATE TABLE game_team_stats (
                    game_id VARCHAR(12),
                    team_id VARCHAR(3),
                    stat_name VARCHAR(32),
                    stat_value VARCHAR(32),
                    PRIMARY KEY (game_id,team_id,stat_name),
                    FOREIGN KEY (game_id) REFERENCES games(game_id),
                    FOREIGN KEY (team_id) REFERENCES teams(team_id)
                    )`,
		`CREATE INDEX game_team_stats_game ON game_team_stats(game_id)`,
		`CREATE TABLE game_player_pos (
                    game_id VARCHAR(12),
                    player_id VARCHAR(10),
                    pos VARCHAR(5),
                    team_id VARCHAR(3),
                    PRIMARY KEY (game_id,player_id),
                    FOREIGN KEY (game_id) REFERENCES games(game_id),
                    FOREIGN KEY (player_id) REFERENCES players(player_id),
                    FOREIGN KEY (team_id) REFERENCES teams(team_id)
                    )`,
		`CREATE INDEX game_player_pos_game ON game_player_pos(game_id)`,
		`CREATE INDEX game_player_pos_game_team ON game_player_pos(game_id,team_id)`,
		`CREATE TABLE game_player_stats (
                    game_id VARCHAR(12),
                    player_id VARCHAR(10),
                    stat_name VARCHAR(32),
                    stat_value REAL,
                    team_id VARCHAR(3),
                    PRIMARY KEY (game_id,player_id,stat_name),
                    FOREIGN KEY (game_id) REFERENCES games(game_id),
                    FOREIGN KEY (player_id) REFERENCES players(player_id),
                    FOREIGN KEY (team_id) REFERENCES teams(team_id)
                    )`,
		`CREATE INDEX game_player_stats_game ON game_player_stats(game_id)`,
		`CREATE INDEX game_player_stats_game_team ON game_player_stats(game_id,team_id)`,
	} {
		if _, err := tx.Exec(stmt); err != nil {
			return err
		}
	}

	if err := tx.Commit(); err != nil {
		return err
	}

	return nil
}
