import datetime
import sys
import tensorflow.keras
import numpy

import data
import schedule
import model1
import model2

db = data.Db('../data/db')
if len(sys.argv) > 1 and sys.argv[1] == 'model1':
    m = model1.Model(db)
    pass
elif len(sys.argv) > 1 and sys.argv[1] == 'model2':
    m = model2.Model(db)
    pass
else:
    m = model2.Model(db)
    pass
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

nruns = 20

xpredict = numpy.empty((1,m.input_dim()))
win = numpy.empty((len(games),nruns))
total = numpy.empty((len(games),nruns))
diff = numpy.empty((len(games),nruns))

for i in range(nruns):
    modelwin = tensorflow.keras.models.Sequential()
    modelwin.add(tensorflow.keras.layers.BatchNormalization(input_shape=(m.input_dim(),)))
    modelwin.add(tensorflow.keras.layers.Dense(m.neurons()[0], activation='relu', kernel_initializer='random_uniform'))
    modelwin.add(tensorflow.keras.layers.Dense(1, activation='sigmoid', kernel_initializer='random_uniform'))
    modelwin.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['binary_accuracy'])

    modeltotal = tensorflow.keras.models.Sequential()
    modeltotal.add(tensorflow.keras.layers.BatchNormalization(input_shape=(m.input_dim(),)))
    modeltotal.add(tensorflow.keras.layers.Dense(m.neurons()[1], activation='relu', kernel_initializer='random_uniform'))
    modeltotal.add(tensorflow.keras.layers.Dense(1, activation='linear', kernel_initializer='random_uniform'))
    modeltotal.compile(optimizer='nadam', loss='mean_squared_error')

    modeldiff = tensorflow.keras.models.Sequential()
    modeldiff.add(tensorflow.keras.layers.BatchNormalization(input_shape=(m.input_dim(),)))
    modeldiff.add(tensorflow.keras.layers.Dense(m.neurons()[2], activation='relu', kernel_initializer='random_uniform'))
    modeldiff.add(tensorflow.keras.layers.Dense(1, activation='linear', kernel_initializer='random_uniform'))
    modeldiff.compile(optimizer='nadam', loss='mean_squared_error')

    modelwin.fit(x, ywin, epochs=m.epochs()[0], batch_size=1024)
    modeltotal.fit(x, ytotal, epochs=m.epochs()[1], batch_size=1024)
    modeldiff.fit(x, ydiff, epochs=m.epochs()[2], batch_size=1024)

    for j in range(len(schedule.games)):
        (date,road_team_id,home_team_id) = schedule.games[j]
        m.set_input_data(schedule.year, schedule.week, date, road_team_id, home_team_id, xpredict, 0)
        win[(j,i)] = modelwin.predict(xpredict)
        total[(j,i)] = modeltotal.predict(xpredict)
        diff[(j,i)] = modeldiff.predict(xpredict)
        pass

    del modelwin
    del modeltotal
    del modeldiff
    pass
pass

for j in range(len(schedule.games)):
    (date,road_team_id,home_team_id) = schedule.games[j]
    print(road_team_id,home_team_id,numpy.average(win[j,:]),numpy.average(total[j,:]),numpy.std(total[j,:]),numpy.average(diff[j,:]),numpy.std(diff[j,:]))
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
    t = numpy.average(total[j,:])
    d = numpy.average(diff[j,:])
    print(road_team_id,max(0,round(float((t+d)/2))),home_team_id,max(0,round(float((t-d)/2))),str(round(100*w))+"%")
    pass
