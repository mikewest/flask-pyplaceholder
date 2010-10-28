import os, errno, re
from flask import Flask, render_template, abort, send_file
from lib.placeholder import Placeholder, PlaceholderOptionError

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

###########################################################################
#
#   App starts here.
#

app = Flask(__name__)

@app.route("/")
def index():
    return render_template( 'index.html' )

@app.route( "/placeholder.png" )
@app.route( "/<int:width>x<int:height>/placeholder.png" )
@app.route( "/<int:width>x<int:height>/<foreground>/<background>/placeholder.png" )
@app.route( "/<int:width>x<int:height>/<foreground>/<background>/<metadata>/placeholder.png" )
@app.route( "/<int:width>x<int:height>/<foreground>/<background>/<metadata>/<border>/placeholder.png" )
def placeholder( width=400, height=300, foreground="333333", background="CCCCCC", border=False, metadata=True ):
    border = False if not border or border == "noborder" else True
    metadata = False if not metadata or metadata == "nometadata" else True
    out = "./output/%dx%d/%s/%s/%s/%s.png" % ( width, height, foreground, background, 'border' if border else 'noborder', 'metadata' if metadata else 'nometadata' )

    if height > 1000 or width > 1000:
        abort( 501,  "Max size is 1000x1000.  Take pity on my poor server, please." )
    if re.search( r'[^0-9a-fA-F]', foreground ):
        abort( 501, "Please use a foreground hex value in the form `RRGGBB`: You entered `%s`" % foreground )
    if re.search( r'[^0-9a-fA-F]', background ):
        abort( 501, "Please use a background hex value in the form `RRGGBB`: You entered `%s`" % background )

    if not os.path.exists( out ):
        mkdir_p( os.path.dirname( out ) )
        p = Placeholder( width=width, height=height, foreground=foreground, background=background, border=border, out=out, metadata=metadata )
        p.write()

    return send_file( filename_or_fp=out, mimetype='image/png', cache_timeout=31556926 )

if __name__ == "__main__":
    app.run(debug=False)
