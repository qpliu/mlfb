import datetime
import tensorflow.keras.models
import numpy

import data
import model1

db = data.Db("../data/db")
m = model1.Model1(db)

year = 2019
week = 6
games = [(datetime.date(2019,10,10),'nyg','nwe'),
         (datetime.date(2019,10,13),'car','tam'),
         (datetime.date(2019,10,13),'sea','cle'),
         (datetime.date(2019,10,13),'cin','rav'),
         (datetime.date(2019,10,13),'phi','min'),
         (datetime.date(2019,10,13),'was','mia'),
         (datetime.date(2019,10,13),'htx','kan'),
         (datetime.date(2019,10,13),'nor','jax'),
         (datetime.date(2019,10,13),'atl','crd'),
         (datetime.date(2019,10,13),'sfo','ram'),
         (datetime.date(2019,10,13),'oti','den'),
         (datetime.date(2019,10,13),'dal','nyj'),
         (datetime.date(2019,10,13),'pit','sdg'),
         (datetime.date(2019,10,14),'det','gnb')]

modelwin = tensorflow.keras.models.load_model("model1.win.h5")
modeltotal = tensorflow.keras.models.load_model("model1.total.h5")
modeldiff = tensorflow.keras.models.load_model("model1.diff.h5")

x = numpy.empty((1,m.input_dim()))
for (date,road_team_id,home_team_id) in games:
    m.set_input_data(year, week, date, road_team_id, home_team_id, x, 0)
    win = modelwin.predict(x)
    total = modeltotal.predict(x)
    diff = modeldiff.predict(x)
    if win[0] > 0.5:
        home_team_id = home_team_id.upper()
        pass
    else:
        road_team_id = road_team_id.upper()
        pass
    print(road_team_id,max(0,round(float((total[0]+diff[0])/2))),home_team_id,max(0,round(float((total[0]-diff[0])/2))),modelwin.predict(x),modeltotal.predict(x),modeldiff.predict(x))
    pass
