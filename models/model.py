import sys
import model1
import model2

def Model(db):
    if len(sys.argv) > 1 and sys.argv[1] == 'model1':
        return model1.Model(db)
    elif len(sys.argv) > 1 and sys.argv[1] == 'model2':
        return model2.Model(db)
    else:
        return model2.Model(db)
