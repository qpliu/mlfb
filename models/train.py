import tensorflow.keras
import numpy

import data
import model2 as model

db = data.Db('../data/db')
m = model.Model(db)
games = db.games(with_snap_counts=m.need_snap_counts(),with_week_1=m.with_week_1())
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
model.add(tensorflow.keras.layers.BatchNormalization(input_shape=(m.input_dim(),)))
model.add(tensorflow.keras.layers.Dense(m.neurons()[0], activation='relu'))
model.add(tensorflow.keras.layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['binary_accuracy'])
model.fit(x, ywin, epochs=m.epochs()[0], batch_size=1024)
model.save(m.name()+".win.h5")
del model

model = tensorflow.keras.models.Sequential()
model.add(tensorflow.keras.layers.BatchNormalization(input_shape=(m.input_dim(),)))
model.add(tensorflow.keras.layers.Dense(m.neurons()[1], activation='relu'))
model.add(tensorflow.keras.layers.Dense(1, activation='linear'))
model.compile(optimizer='nadam', loss='mean_squared_error')
model.fit(x, ytotal, epochs=m.epochs()[2], batch_size=1024)
model.save(m.name()+".total.h5")
del model

model = tensorflow.keras.models.Sequential()
model.add(tensorflow.keras.layers.BatchNormalization(input_shape=(m.input_dim(),)))
model.add(tensorflow.keras.layers.Dense(m.neurons()[2], activation='relu'))
model.add(tensorflow.keras.layers.Dense(1, activation='linear'))
model.compile(optimizer='nadam', loss='mean_squared_error')
model.fit(x, ydiff, epochs=m.epochs()[1], batch_size=1024)
model.save(m.name()+".diff.h5")
del model
