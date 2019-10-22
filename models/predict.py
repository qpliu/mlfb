import tensorflow.keras.models
import numpy

import data
import schedule
import model

db = data.Db("../data/db")
m = model.Model(db)

modelwin = tensorflow.keras.models.load_model(m.name()+".win.h5")
modelscore = tensorflow.keras.models.load_model(m.name()+".score.h5")

x = numpy.empty((1,m.input_dim()))
for (date,road_team_id,home_team_id) in schedule.games:
    m.set_input_data(schedule.year, schedule.week, date, road_team_id, home_team_id, x, 0)
    win = modelwin.predict(x)
    score = modelscore.predict(x)
    if win[0] > 0.5:
        home_team_id = home_team_id.upper()
        pass
    else:
        road_team_id = road_team_id.upper()
        pass
    print(road_team_id,max(0,int(round(score[0,0]))),home_team_id,max(0,int(round(score[0,1]))))
    pass
