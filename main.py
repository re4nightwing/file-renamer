import sys, os
if sys.executable.endswith('pythonw.exe'):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.path.join(os.getenv('TEMP'), 'stderr-{}'.format(os.path.basename(sys.argv[0]))), "w")
    
from flask import Flask, render_template, jsonify, request
from flaskwebgui import FlaskUI
from uuid import uuid4
import json, re, string, requests, urllib.request, socket, platform


app = Flask(__name__)
app.debug = False #change this on GUI

USERNAME = 're4nightwing'
REPO_NAME = 'file-renamer'
CURRENT_VERSION = 'v0.1.1'
URL = f"https://api.github.com/repos/{USERNAME}/{REPO_NAME}/releases/latest"
PLATFORM = 'Windows'

if(platform.uname()[0] == 'Linux'):
  PLATFORM = 'Linux'
else:
  from ctypes import windll


def check_internet_connection():
  try:
    urllib.request.urlopen('https://www.google.com', timeout=1)
    return True
  except urllib.request.URLError:
    pass
  try:
    socket.gethostbyname('www.google.com')
    return True
  except socket.gaierror:
    pass
  return False

def check_version(url:str, current_version:str):
  if check_internet_connection():
    response = requests.get(url)
    data = json.loads(response.content)
    latest_version = data["tag_name"]
    if latest_version != current_version:
      return latest_version
    else:
      return True
  else:
    return False

def saybye():
  print("Thank you for using, bye!")

def start_flask(**server_kwargs):
  app = server_kwargs.pop("app", None)
  server_kwargs.pop("debug", None)
  try:
    import waitress
    waitress.serve(app, **server_kwargs)
  except:
    app.run(**server_kwargs)

def get_drives():
  drives = []
  if(PLATFORM == 'Linux'):
    for dir in os.listdir(os.path.expanduser("~")):
      if not dir.startswith('.'):
        drives.append(f'~/{dir}/')
  else:
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
      if bitmask & 1:
        drives.append(f'{letter}:\\')
      bitmask >>= 1
  return drives

def get_file_ext(filename):
  parts = filename.split(".")
  extension = "." + parts[-1]
  return(extension)

def sanitize_filename(filename_list):
  sanitized_filename_list = []
  pattern = r'[<>:"/\\|?*]'
  for name in filename_list:
    sanitized_filename_list.append(re.sub(pattern, '-', name))
  return sanitized_filename_list

def make_file_name_list(no_of_files, filename_style):
  if no_of_files != 0:
    matches = re.findall(r'<.*?>', filename_style)
    name_list = []
    if(len(matches) != 0):
      for i in range(no_of_files):
        new_string = re.sub(r'<.*?>', '{:02d}'.format(i+1), filename_style)
        name_list.append(new_string)
    else:
      for i in range(no_of_files):
        new_string = filename_style + '{:02d}'.format(i+1)
        name_list.append(new_string)
    return sanitize_filename(name_list)
  else:
    return False


@app.route('/', methods=['GET', 'POST'])
def index_page():
  context = {
    'drives': get_drives(),
    'current_version': CURRENT_VERSION
  }
  version_check = check_version(URL, CURRENT_VERSION)
  if isinstance(version_check, str):
    context['new_version'] = version_check
  return render_template('home.html', context=context)

@app.route('/get_dir_tree', methods=['POST'])
def get_dir_tree():
  context = {}
  dir_list = {}
  req_path = request.form['directory']
  if PLATFORM == 'Linux':
    req_path = os.path.expanduser(req_path)
  filenames = os.listdir(req_path)
  directories = [d for d in filenames if os.path.isdir(os.path.join(req_path, d))]
  directories.sort()
  for dir in directories:
    dir_list[dir] = f'{req_path}/{dir}'
  context['dir_list'] = dir_list
  return jsonify(context), 200

@app.route('/scan_dir', methods=['POST'])
def scan_directory():
  dir_path = request.form['directory']
  if PLATFORM == 'Linux':
    dir_path = os.path.expanduser(dir_path)
  context = {'path' : dir_path}
  if os.path.exists(dir_path) and os.path.isdir(dir_path):
    filenames = os.listdir(dir_path)
    files = [f for f in filenames if os.path.isfile(os.path.join(dir_path, f))]
    files.sort()
    file_list = {}
    for file in files:
      file_list[str(uuid4())] = file
    #add recursion to for folders inside the directory.
    #directories = [d for d in filenames if os.path.isdir(os.path.join(dir_path, d))]
    #context['directory_list'] = directories
    #print(file_list)
    context['file_list'] = file_list
  else:
      context['err'] = 'Invalid directory path'
      print('Invalid directory path')
      return jsonify(context), 400
  return jsonify(context), 200

@app.route('/rename_dir', methods=['POST'])
def rename_directory():
  dir_path = request.form['directory']
  file_list = request.form['file_list']
  rename_style = request.form['style']
  data = json.loads(file_list)
  name_list = make_file_name_list(len(data), rename_style)
  if name_list:
    #print(name_list)
    for file in data:
      if os.path.isfile(os.path.join(dir_path, file['filename'])):
        os.rename(os.path.join(dir_path, file['filename']), os.path.join(dir_path, file['id'] + get_file_ext(file['filename'])))
      #add didn't find file to the response.
    for index, file in enumerate(data):
      if os.path.isfile(os.path.join(dir_path, file['id'] + get_file_ext(file['filename']))):
        os.rename(os.path.join(dir_path, file['id'] + get_file_ext(file['filename'])), os.path.join(dir_path, str(name_list[index]) + get_file_ext(file['filename'])))
  else:
    return jsonify({"msg": "No files found"}), 400
  #return new files names to update the table after done.
  return jsonify('context'), 200

@app.route('/about', methods=['GET', 'POST'])
def about_page():
  return render_template('about.html')

if __name__ == "__main__":
  #app.run() #development
  FlaskUI(
    server=start_flask,
    server_kwargs={
      "app": app,
      "port": 3000,
      "threaded": True,
    },
    width=850,
    height=600,
    on_shutdown=saybye).run()


  #### pyvan main.py -nc --icon .\static\file_icon.ico
  #### pyinstaller --noconfirm --onefile --console --icon "D:/Python/File-Renamer/app/static/file_icon.ico" --add-data "D:/Python/File-Renamer/app/templates;templates/" --add-data "D:/Python/File-Renamer/app/static;static/"  "D:/Python/File-Renamer/app/main.py"