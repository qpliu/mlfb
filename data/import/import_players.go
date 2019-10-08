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
		panic("Usage: import_players db_file < data")
	}
	db, err := sql.Open("sqlite3", os.Args[1])
	if err != nil {
		panic(err)
	}

	if err := importPlayers(db, os.Stdin); err != nil {
		panic(err)
	}
}

func importPlayers(db *sql.DB, r io.Reader) error {
	in := csv.NewReader(r)
	for {
		row, err := in.Read()
		if err == io.EOF {
			return nil
		} else if err != nil {
			return err
		}
		if len(row) != 7 {
			return fmt.Errorf("Wrong number of fields:%d", len(row))
		}
		var height sql.NullInt64
		var weight sql.NullInt64
		var dob sql.NullString
		var draftPos sql.NullInt64
		ft := 0
		in := 0
		if _, err := fmt.Sscanf(row[3], "%d-%d", &ft, &in); err != nil {
		} else {
			height.Valid = true
			height.Int64 = int64(ft*12 + in)
		}
		if _, err := fmt.Sscanf(row[4], "%dlb", &weight.Int64); err != nil {
		} else {
			weight.Valid = true
		}
		if row[5] != "" {
			dob.Valid = true
			dob.String = row[5]
		}
		if _, err := fmt.Sscanf(row[6], "%d", &draftPos.Int64); err != nil {
		} else {
			draftPos.Valid = true
		}
		if err := func() error {
			tx, err := db.Begin()
			if err != nil {
				return err
			}
			defer tx.Rollback()

			if _, err := tx.Exec("INSERT INTO players (player_id, name, pos, height, weight, dob, draft_pos) VALUES (?,?,?,?,?,?,?)", row[0], row[1], row[2], height, weight, dob, draftPos); err != nil {
				if e, ok := err.(sqlite3.Error); ok && e.Code == sqlite3.ErrConstraint {
					return nil
				}
				return err
			}
			if err := tx.Commit(); err != nil {
				return err
			}
			return nil
		}(); err != nil {
			return err
		}
	}
}
