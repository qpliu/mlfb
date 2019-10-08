package main

import (
	"database/sql"
	"encoding/csv"
	"fmt"
	"io"
	"os"

	"github.com/mattn/go-sqlite3"
)

func main() {
	if len(os.Args) != 2 {
		panic("Usage: import_game db_file < data")
	}
	db, err := sql.Open("sqlite3", os.Args[1])
	if err != nil {
		panic(err)
	}

	if err := importGame(db, os.Stdin); err != nil {
		panic(err)
	}
}

func importGame(db *sql.DB, r io.Reader) error {
	tx, err := db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	in := csv.NewReader(r)
	for {
		row, err := in.Read()
		if err == io.EOF {
			break
		} else if err != nil {
			return err
		}
		if len(row) == 0 {
			continue
		} else if len(row) != 11 {
			return fmt.Errorf("Wrong number of fields:%d", len(row))
		}
		if row[0] == "game" {
			if _, err := tx.Exec("INSERT INTO teams (team_id) VALUES (?)", row[5]); err != nil {
				if e, ok := err.(sqlite3.Error); !ok || e.Code != sqlite3.ErrConstraint {
					return err
				}
			}
			if _, err := tx.Exec("INSERT INTO teams (team_id) VALUES (?)", row[8]); err != nil {
				if e, ok := err.(sqlite3.Error); !ok || e.Code != sqlite3.ErrConstraint {
					return err
				}
			}

			var year int
			if _, err := fmt.Sscanf(row[1], "%d", &year); err != nil {
				return err
			}
			var week int
			if _, err := fmt.Sscanf(row[2], "%d", &week); err != nil {
				return err
			}
			if len(row[3]) != 8 {
				return fmt.Errorf("Unrecognized date:%s", row[3])
			}
			date := row[3][0:4] + "-" + row[3][4:6] + "-" + row[3][6:]
			var roadTeamScore int
			if _, err := fmt.Sscanf(row[7], "%d", &roadTeamScore); err != nil {
				return err
			}
			var homeTeamScore int
			if _, err := fmt.Sscanf(row[10], "%d", &homeTeamScore); err != nil {
				return err
			}

			if _, err := tx.Exec("INSERT INTO games (game_id, year, week, date, road_team_id, road_team_name, road_team_score, home_team_id, home_team_name, home_team_score) VALUES (?,?,?,?,?,?,?,?,?,?)", row[4], year, week, date, row[5], row[6], roadTeamScore, row[8], row[9], homeTeamScore); err != nil {
				if e, ok := err.(sqlite3.Error); !ok || e.Code != sqlite3.ErrConstraint {
					return err
				}
			}
		} else if row[0] == "team" {
			if _, err := tx.Exec("INSERT INTO game_team_stats (game_id, team_id, stat_name, stat_value) VALUES (?,?,?,?)", row[1], row[2], row[3], row[4]); err != nil {
				if e, ok := err.(sqlite3.Error); !ok || e.Code != sqlite3.ErrConstraint {
					return err
				}
			}
		} else if row[0] == "player" && row[4] == "pos" {
			if _, err := tx.Exec("INSERT INTO game_player_pos (game_id, player_id, pos, team_id) VALUES (?,?,?,?)", row[1], row[3], row[5], row[2]); err != nil {
				if e, ok := err.(sqlite3.Error); !ok || e.Code != sqlite3.ErrConstraint {
					return err
				}
			}
		} else if row[0] == "player" {
			if row[5] == "" {
				continue
			}
			var statValue float64
			if _, err := fmt.Sscanf(row[5], "%f%%", &statValue); err != nil {
				if _, err := fmt.Sscanf(row[5], "%f", &statValue); err != nil {
					println(row[1], row[2], row[3], row[4], row[5])
					return err
				}
			}
			if _, err := tx.Exec("INSERT INTO game_player_stats (game_id, player_id, stat_name, stat_value, team_id) VALUES (?,?,?,?,?)", row[1], row[3], row[4], statValue, row[2]); err != nil {
				if e, ok := err.(sqlite3.Error); !ok || e.Code != sqlite3.ErrConstraint {
					return err
				}
			}
		} else {
			return fmt.Errorf("Unrecognized row: %s", row[0])
		}
	}

	if err := tx.Commit(); err != nil {
		return err
	}
	return nil
}
