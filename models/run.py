import datetime
import sys
import tensorflow.keras
import numpy

import data
import model
import schedule

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
yscore = numpy.empty((len(games),2))
for i in range(len(games)):
    g = games[i]
    (year, week, date) = g.game_time()
    (road_team_id,home_team_id) = g.teams()
    m.set_input_data(year, week, date, road_team_id, home_team_id, x, i)
    ywin[i,0] = g.target_data_win()
    yscore[i,0] = g.score()[0]
    yscore[i,1] = g.score()[1]
    pass

nruns = 30

xpredict = numpy.empty((1,m.input_dim()))
win = numpy.empty((len(games),nruns))
score = numpy.empty((len(games),2,nruns))

for i in range(nruns):
    modelwin = tensorflow.keras.models.Sequential()
    modelwin.add(tensorflow.keras.layers.BatchNormalization(input_shape=(m.input_dim(),)))
    modelwin.add(tensorflow.keras.layers.Dense(m.neurons()[0], activation='relu', kernel_initializer='random_uniform'))
    modelwin.add(tensorflow.keras.layers.Dense(1, activation='sigmoid', kernel_initializer='random_uniform'))
    modelwin.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['binary_accuracy'])

    modelscore = tensorflow.keras.models.Sequential()
    modelscore.add(tensorflow.keras.layers.BatchNormalization(input_shape=(m.input_dim(),)))
    modelscore.add(tensorflow.keras.layers.Dense(m.neurons()[1], activation='relu', kernel_initializer='random_uniform'))
    modelscore.add(tensorflow.keras.layers.Dense(2, activation='linear', kernel_initializer='random_uniform'))
    modelscore.compile(optimizer='nadam', loss='mean_squared_error')

    modelwin.fit(x, ywin, epochs=m.epochs()[0], batch_size=1024, verbose=0)
    modelscore.fit(x, yscore, epochs=m.epochs()[1], batch_size=1024, verbose=0)

    for j in range(len(schedule.games)):
        (date,road_team_id,home_team_id) = schedule.games[j]
        m.set_input_data(schedule.year, schedule.week, date, road_team_id, home_team_id, xpredict, 0)
        win[j,i] = modelwin.predict(xpredict)
        score[j,:,i] = modelscore.predict(xpredict)
        pass

    del modelwin
    del modelscore
    pass
pass

for j in range(len(schedule.games)):
    (date,road_team_id,home_team_id) = schedule.games[j]
    w = numpy.average(win[j,:])
    if w >= 0.6:
        home_team_id = home_team_id.upper()
        pass
    elif w < 0.4:
        road_team_id = road_team_id.upper()
        pass
    road_score = numpy.average(score[j,0,:])
    home_score = numpy.average(score[j,1,:])
    print(road_team_id,max(0,int(round(road_score))),home_team_id,max(0,int(round(home_score))),str(round(100*w))+"%")
    pass
