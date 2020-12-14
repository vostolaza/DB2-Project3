from search import knnRTree
from flask import Flask,jsonify,render_template, request, session, Response, redirect
from flask import send_from_directory
# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder= "")
app._static_folder = "static/web"

@app.route('/')
def index():
    return render_template("static/web/html/index.html")



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




# @app.route('/', methods=['GET', 'POST'])
# def upload_image():
#     # Check if a valid image file was uploaded
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return redirect(request.url)

#         file = request.files['file']

#         if file.filename == '':
#             return redirect(request.url)

#         if file and allowed_file(file.filename):
#             # The image file seems valid! Detect faces and return the result.
#             return find_closest_match(file, 8, 200)

#     # If no valid image file was uploaded, show the file upload form:
#     return '''
#     <!doctype html>
#     <title>Proyecto 3</title>
#     <h1>Ingrese una imagen y mostraremos las 8 caras mas parecidas</h1>
#     <form method="POST" enctype="multipart/form-data">
#       <input type="file" name="file">
#       <input type="submit" value="Cargar">
#     </form>
#     '''


def find_closest_match(file_stream, k, size):
    pictures = knnRTree(size, k, file_stream)

    if not len(pictures):
        return f'''
        <!doctype html>
        <title>Proyecto 3</title>
        <h1>No se encontraron caras en la imagen ingresada<h1>
        '''

    html = ""
    for picture in pictures:
        print(picture)
        html += f'<img src="{picture}">'

    return f'''
    <!doctype html>
    <title>Proyecto 3</title>
    {html}
    '''
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=False)
