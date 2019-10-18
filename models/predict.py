import tensorflow.keras.models
import numpy

import data
import schedule
import model2 as model

db = data.Db("../data/db")
m = model.Model(db)

modelwin = tensorflow.keras.models.load_model(m.name()+".win.h5")
modeltotal = tensorflow.keras.models.load_model(m.name()+".total.h5")
modeldiff = tensorflow.keras.models.load_model(m.name()+".diff.h5")

x = numpy.empty((1,m.input_dim()))
for (date,road_team_id,home_team_id) in schedule.games:
    m.set_input_data(schedule.year, schedule.week, date, road_team_id, home_team_id, x, 0)
    win = modelwin.predict(x)
    total = modeltotal.predict(x)
    diff = modeldiff.predict(x)
    if win[0] > 0.5:
        home_team_id = home_team_id.upper()
        pass
    else:
        road_team_id = road_team_id.upper()
        pass
    print(road_team_id,max(0,round(float((total[0]+diff[0])/2))),home_team_id,max(0,round(float((total[0]-diff[0])/2))))
    pass
