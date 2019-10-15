import datetime
import tensorflow.keras.models
import numpy

import data
import model2 as model

db = data.Db("../data/db")
m = model.Model(db)

year = 2019
week = 7
games = [(datetime.date(2019,10,17),'kan','den'),
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

modelwin = tensorflow.keras.models.load_model(m.name()+".win.h5")
modeltotal = tensorflow.keras.models.load_model(m.name()+".total.h5")
modeldiff = tensorflow.keras.models.load_model(m.name()+".diff.h5")

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
    print(road_team_id,max(0,round(float((total[0]+diff[0])/2))),home_team_id,max(0,round(float((total[0]-diff[0])/2))))
    pass
