from lib.imagize import Imagize
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    print "index"
    return 'Hello there!'

@app.route('/imagize')
def imagize():
    return (Imagize()).generate("")

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)

    I = Imagize()
    print I.generate("As they rounded a bend in the path that ran beside the river, Lara recognized the "
                     "silhouette of a fig tree atop a nearby hill. The weather was hot and the days were "
                     "long. The fig tree was in full leaf, but not yet bearing fruit. Soon Lara spotted other "
                     "landmarks - an outcropping of limestone beside the path that had a silhouette like a man's "
                     "face, a marshy spot beside the river where the waterfowl were easily startled, a tall tree")