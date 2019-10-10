import tensorflow.keras
import numpy

import data
import model1

db = data.Db('../data/db')
m = model1.Model1(db)
games = db.games(with_snap_counts=m.need_snap_counts())
for i in range(len(games)):
    if games[i].game_time()[1] > m.need_history_size():
        games = games[i:]
        break
    pass

x = numpy.empty((len(games),m.input_dim()))
ywin = numpy.empty((len(games),1))
ytotal = numpy.empty((len(games),1))
ydiff = numpy.empty((len(games),1))
for i in range(len(games)):
    g = games[i]
    (year, week, date) = g.game_time()
    (road_team_id,home_team_id) = g.teams()
    m.set_input_data(year, week, date, road_team_id, home_team_id, x, i)
    ywin[i,0] = g.target_data_win()
    ytotal[i,0] = g.target_data_score_total()
    ydiff[i,0] = g.target_data_score_diff()
    pass

model = tensorflow.keras.models.Sequential()
model.add(tensorflow.keras.layers.Dense(32, activation='relu', input_dim=m.input_dim()))
model.add(tensorflow.keras.layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['binary_accuracy'])
model.fit(x, ywin, epochs=20, batch_size=1024)
model.save("model1.win.h5")
del model

model = tensorflow.keras.models.Sequential()
model.add(tensorflow.keras.layers.Dense(32, activation='relu', input_dim=m.input_dim()))
model.add(tensorflow.keras.layers.Dense(1, activation='linear'))
model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_squared_error'])
model.fit(x, ytotal, epochs=50, batch_size=1024)
model.save("model1.total.h5")
del model

model = tensorflow.keras.models.Sequential()
model.add(tensorflow.keras.layers.Dense(32, activation='relu', input_dim=m.input_dim()))
model.add(tensorflow.keras.layers.Dense(1, activation='linear'))
model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_squared_error'])
model.fit(x, ydiff, epochs=50, batch_size=1024)
model.save("model1.diff.h5")
del model
