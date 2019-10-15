import datetime
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

modelwin = tensorflow.keras.models.Sequential()
modelwin.add(tensorflow.keras.layers.Dense(64, activation='relu', input_dim=m.input_dim()))
modelwin.add(tensorflow.keras.layers.Dense(1, activation='sigmoid'))
modelwin.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['binary_accuracy'])

modeltotal = tensorflow.keras.models.Sequential()
modeltotal.add(tensorflow.keras.layers.Dense(64, activation='relu', input_dim=m.input_dim()))
modeltotal.add(tensorflow.keras.layers.Dense(1, activation='linear'))
modeltotal.compile(optimizer='nadam', loss='mean_squared_error', metrics=['mean_squared_error'])

modeldiff = tensorflow.keras.models.Sequential()
modeldiff.add(tensorflow.keras.layers.Dense(64, activation='relu', input_dim=m.input_dim()))
modeldiff.add(tensorflow.keras.layers.Dense(1, activation='linear'))
modeldiff.compile(optimizer='nadam', loss='mean_squared_error', metrics=['mean_squared_error'])

year = 2019
week = 7
schedule = [(datetime.date(2019,10,17),'kan','den'),
            (datetime.date(2019,10,20),'mia','buf'),
            (datetime.date(2019,10,20),'ram','atl'),
            (datetime.date(2019,10,20),'sfo','was'),
            (datetime.date(2019,10,20),'crd','nyg'),
            (datetime.date(2019,10,20),'rai','gnb'),
            (datetime.date(2019,10,20),'min','det'),
            (datetime.date(2019,10,20),'htx','clt'),
            (datetime.date(2019,10,20),'jax','cin'),
            (datetime.date(2019,10,20),'sdg','oti'),
            (datetime.date(2019,10,20),'nor','chi'),
            (datetime.date(2019,10,20),'rav','sea'),
            (datetime.date(2019,10,20),'phi','dal'),
            (datetime.date(2019,10,21),'nwe','nyj')]
n = 300
nwarmup = 500

xpredict = numpy.empty((1,m.input_dim()))
win = numpy.empty((len(games),n))
total = numpy.empty((len(games),n))
diff = numpy.empty((len(games),n))

for i in range(n+nwarmup):
    modelwin.fit(x, ywin, epochs=20, batch_size=1024)
    modeltotal.fit(x, ytotal, epochs=200, batch_size=1024)
    modeldiff.fit(x, ydiff, epochs=200, batch_size=1024)
    if i >= nwarmup:
        for j in range(len(schedule)):
            (date,road_team_id,home_team_id) = schedule[j]
            m.set_input_data(year, week, date, road_team_id, home_team_id, xpredict, 0)
            win[(j,i-nwarmup)] = modelwin.predict(xpredict)
            total[(j,i-nwarmup)] = modeltotal.predict(xpredict)
            diff[(j,i-nwarmup)] = modeldiff.predict(xpredict)
            pass
        pass
    pass
pass

for j in range(len(schedule)):
    (date,road_team_id,home_team_id) = schedule[j]
    print(road_team_id,home_team_id,numpy.average(win[j,:]),numpy.average(total[j,:]),numpy.std(total[j,:]),numpy.average(diff[j,:]),numpy.std(diff[j,:]))
    pass

for j in range(len(schedule)):
    (date,road_team_id,home_team_id) = schedule[j]
    print(road_team_id,home_team_id,win[j,-1],total[j,-1],diff[j,-1])
    pass

for j in range(len(schedule)):
    (date,road_team_id,home_team_id) = schedule[j]
    w = numpy.average(win[j,:])
    if w >= 0.5:
        home_team_id = home_team_id.upper()
        pass
    else:
        road_team_id = road_team_id.upper()
        pass
    t = numpy.average(total[j,:])
    d = numpy.average(diff[j,:])
    print(road_team_id,max(0,round(float((t+d)/2))),home_team_id,max(0,round(float((t-d)/2))))
    pass
