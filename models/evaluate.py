import datetime
import random
import sys
import tensorflow.keras
import numpy

import data
import model

db = data.Db('../data/db')

for history_size in range(1,13):
    m = model.Model(db)
    m.set_history_size(history_size)
    label = 'history_size='+str(history_size)

    games = db.games(with_snap_counts=m.need_snap_counts(),with_week_1=m.with_week_1())
    for i in range(len(games)):
        if games[i].game_time()[1] > m.need_history_size():
            games = games[i:]
            break
        pass
    random.shuffle(games)

    ntrain = int(0.9*len(games))
    nvalidate = len(games) - ntrain

    xtrain = numpy.empty((ntrain,m.input_dim()))
    ywintrain = numpy.empty((ntrain,1))
    yscoretrain = numpy.empty((ntrain,2))
    for i in range(ntrain):
        g = games[i]
        (year, week, date) = g.game_time()
        (road_team_id,home_team_id) = g.teams()
        m.set_input_data(year, week, date, road_team_id, home_team_id, xtrain, i)
        ywintrain[i,0] = g.target_data_win()
        yscoretrain[i,0] = g.score()[0]
        yscoretrain[i,1] = g.score()[1]
        pass

    xvalidate = numpy.empty((nvalidate,m.input_dim()))
    ywinvalidate = numpy.empty((nvalidate,1))
    yscorevalidate = numpy.empty((nvalidate,2))
    for i in range(nvalidate):
        g = games[i+ntrain]
        (year, week, date) = g.game_time()
        (road_team_id,home_team_id) = g.teams()
        m.set_input_data(year, week, date, road_team_id, home_team_id, xvalidate, i)
        ywinvalidate[i,0] = g.target_data_win()
        yscorevalidate[i,0] = g.score()[0]
        yscorevalidate[i,1] = g.score()[1]
        pass

    modelwin = tensorflow.keras.models.Sequential()
    modelwin.add(tensorflow.keras.layers.BatchNormalization(input_shape=(m.input_dim(),)))
    modelwin.add(tensorflow.keras.layers.Dense(m.neurons()[0], activation='relu', kernel_initializer='random_uniform'))
    modelwin.add(tensorflow.keras.layers.Dense(1, activation='sigmoid', kernel_initializer='random_uniform'))
    modelwin.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['binary_accuracy'])

    modelscore = tensorflow.keras.models.Sequential()
    modelscore.add(tensorflow.keras.layers.BatchNormalization(input_shape=(m.input_dim(),)))
    modelscore.add(tensorflow.keras.layers.Dense(m.neurons()[1], activation='relu', kernel_initializer='random_uniform'))
    modelscore.add(tensorflow.keras.layers.Dense(2, activation='linear', kernel_initializer='random_uniform'))
    modelscore.compile(optimizer='nadam', loss='mean_squared_error', metrics=['accuracy'])

    modelwin.fit(xtrain, ywintrain, epochs=m.epochs()[0], batch_size=1024, verbose=0)
    modelscore.fit(xtrain, yscoretrain, epochs=m.epochs()[1], batch_size=1024, verbose=0)

    evalwin = modelwin.evaluate(x=xvalidate, y=ywinvalidate, verbose=0)
    for i in range(len(evalwin)):
        print('evalwin', label, modelwin.metrics_names[i], evalwin[i])
        pass

    evalscore = modelscore.evaluate(x=xvalidate, y=yscorevalidate, verbose=0)
    for i in range(len(evalscore)):
        print('evalscore', label, modelscore.metrics_names[i], evalscore[i])
        pass

    del modelwin
    del modelscore
    pass
