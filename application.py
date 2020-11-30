from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import glob
import urllib.request
import fitz

from ami import ami_extract_details
from form import extract_details
from fid import fid_extract_details
from mer import mer_extract_details
from sch import sch_extract_details
from dl import dl_extract_details
from extra import extra_dets
from checkbox import composed_model_details

app = Flask(__name__)
app.secret_key = "detectform"

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

UPLOAD_FOLDER1 = os.path.join(path, 'pdf2img')
if not os.path.isdir(UPLOAD_FOLDER1):
    os.mkdir(UPLOAD_FOLDER1)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1

def convertpdf(pdffile,page):
    p = page
    doc = fitz.open(pdffile)
    page = doc.loadPage(page-1)  # number of page
    pix = page.getPixmap(matrix=fitz.Matrix(150/72,150/72))
    output = "./pdf2img/"+str(p)+".jpg"
    pix.writePNG(output)


#MAIN APP MAKING
@app.route("/")
def home():
    return render_template('home.html')

@app.route('/predicturl', methods=['GET', 'POST'])
def predicturl():

    if request.method == 'POST':
        docs = request.form['documents']
        filedata = urllib.request.urlopen(docs)
        datatowrite = filedata.read()
        with open(r'uploads/download.pdf', 'wb') as f:
            f.write(datatowrite)

    f = []
    f1 = []
    f2 = []
    f3 = []
    f4 = []
    f5 = []
    f6 = []
    f7 = []
    f8 = []
    f9 = []
    f10 = []
    f11 = []
    f12 = []
    f13 = []
    f14 = []

    org_cbox = []
    cat_cbox = []
    selected = []
    unselected = []

    global org
    global cat
    global fname
    global mname
    global lname
    global dob
    global ssn
    global email
    global tele
    global street
    global city
    global state
    global accno
    global sex
    global det



    for file_name in glob.iglob("uploads/**/*.pdf", recursive=True):
        org, cat = extract_details(file_name)
        #det = extra_dets(file_name)
        org = org.lower()
        cat = cat.lower()

        if "ameritrade" in org and "standard account application" in cat:
            convertpdf(file_name, 1)
            convertpdf(file_name, 2)
        if "ameritrade" in org and "account transfer form" in cat:
            convertpdf(file_name, 1)

        if "merrill" in org and "client relationship agreement" in cat:
            convertpdf(file_name, 4)

        if "merrill" in org and "lma account profile form – retail/trust" in cat:
            convertpdf(file_name, 5)

        if "merrill" in org and "client account transfer form" in cat:
            convertpdf(file_name, 1)

        if "fidelity" in org and "new fidelity account®—ira" in cat:
            convertpdf(file_name, 1)

        if "fidelity" in org and "new fidelity account®—non-retirement—brokerage" in cat:
            convertpdf(file_name, 1)

        if "charles schwab" in org and "ira account application" in cat:
            convertpdf(file_name, 1)
        if "charles schwab" in org and "ira distribution form" in cat:
            convertpdf(file_name, 1)
        if "charles schwab" in org and "schwab one®account application for personal accounts" in cat:
            convertpdf(file_name, 1)

        extensions = [".jpg"]
        l = [f for f in os.listdir("pdf2img") if os.path.splitext(f)[1] in extensions]
        for k in range(len(l)):
            img_file = "pdf2img/" + l[k]
            org_cb, cat_cb, selected_cb, unselected_cb = composed_model_details(img_file)

            org_cbox.append(org_cb)
            cat_cbox.append(cat_cb)
            selected.append(selected_cb)
            unselected.append(unselected_cb)

        BASE_DIR = os.getcwd()
        dir = os.path.join(BASE_DIR, "pdf2img")
        for root, dirs, files in os.walk(dir):
            for file in files:
                path = os.path.join(dir, file)
                os.remove(path)

        if "merrill" in org:
            org, cat, fname, mname, lname, dob, ssn, email, tele, street, city, state, sex, accno = mer_extract_details(file_name)
            det = extra_dets(file_name)
        elif "ameritrade" in org:
            org, cat, fname, mname, lname, dob, ssn, email, tele, street, city, state, sex, accno = ami_extract_details(file_name)
            det = extra_dets(file_name)
        elif "fidelity" in org:
            org, cat, fname, mname, lname, dob, ssn, email, tele, street, city, state, sex, accno = fid_extract_details(file_name)
            det = extra_dets(file_name)
        elif "charles schwab" in org:
            org, cat, fname, mname, lname, dob, ssn, email, tele, street, city, state, sex, accno = sch_extract_details(file_name)
            det = extra_dets(file_name)
        elif "driving license" in org:
            org, cat, fname, mname, lname, dob, ssn, email, tele, street, city, state, sex, accno = dl_extract_details(file_name)

        f.append(org)
        f1.append(cat)
        f2.append(fname)
        f3.append(mname)
        f4.append(lname)
        f5.append(dob)
        f6.append(ssn)
        f7.append(email)
        f8.append(tele)
        f9.append(street)
        f10.append(city)
        f11.append(state)
        f12.append(sex)
        f13.append(accno)
        f14.append(det)

    os.system("cls")
    print(f)
    print(f1)
    print(f2)
    print(f3)
    print(f4)
    print(f5)
    print(f6)
    print(f7)
    print(f8)
    print(f9)
    print(f10)
    print(f11)
    print(f12)
    print(f13)
    print(f14)

    # EMPTY UPLOAD FOLDER
    BASE_DIR = os.getcwd()
    dir = os.path.join(BASE_DIR, "uploads")

    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(dir, file)
            os.remove(path)

    return render_template('predict.html', org=org, cat=cat, fname=fname, mname=mname, lname=lname, dob=dob, ssn=ssn, email=email, tele=tele, street=street,city=city, state=state, sex=sex, accno=accno, selected=selected,unselected=unselected, det=det)

@app.route('/predictfile', methods=['GET', 'POST'])
def predictfile():
    if request.method == 'POST' and 'doc' in request.files:
        for f in request.files.getlist('doc'):
            file = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
    f = []
    f1 = []
    f2 = []
    f3 = []
    f4 = []
    f5 = []
    f6 = []
    f7 = []
    f8 = []
    f9 = []
    f10 = []
    f11 = []
    f12 = []
    f13 = []
    f14 = []

    org_cbox = []
    cat_cbox = []
    selected = []
    unselected = []

    global org
    global cat
    global fname
    global mname
    global lname
    global dob
    global ssn
    global email
    global tele
    global street
    global city
    global state
    global accno
    global sex
    global det

    for file_name in glob.iglob("uploads/**/*.pdf", recursive=True):
        org, cat = extract_details(file_name)
        # det = extra_dets(file_name)
        org = org.lower()
        cat = cat.lower()

        if "ameritrade" in org and "standard account application" in cat:
            convertpdf(file_name, pages="1-2")
        if "ameritrade" in org and "account transfer form" in cat:
            convertpdf(file_name, pages="1")

        if "merrill" in org and "client relationship agreement" in cat:
            convertpdf(file_name, pages=4)

        if "merrill" in org and "lma account profile form – retail/trust" in cat:
            convertpdf(file_name, pages=5)

        if "merrill" in org and "client account transfer form" in cat:
            convertpdf(file_name, pages=1)

        if "fidelity" in org and "new fidelity account®—ira" in cat:
            convertpdf(file_name, pages=1)

        if "fidelity" in org and "new fidelity account®—non-retirement—brokerage" in cat:
            convertpdf(file_name, pages=1)

        if "charles schwab" in org and "ira account application" in cat:
            convertpdf(file_name, pages=1)
        if "charles schwab" in org and "ira distribution form" in cat:
            convertpdf(file_name, pages=1)
        if "charles schwab" in org and "schwab one®account application for personal accounts" in cat:
            convertpdf(file_name, pages=1)

        extensions = [".jpg"]
        l = [f for f in os.listdir("pdf2img") if os.path.splitext(f)[1] in extensions]
        for k in range(len(l)):
            img_file = "pdf2img/" + l[k]
            org_cb, cat_cb, selected_cb, unselected_cb = composed_model_details(img_file)

            org_cbox.append(org_cb)
            cat_cbox.append(cat_cb)
            selected.append(selected_cb)
            unselected.append(unselected_cb)

        BASE_DIR = os.getcwd()
        dir = os.path.join(BASE_DIR, "pdf2img")
        for root, dirs, files in os.walk(dir):
            for file in files:
                path = os.path.join(dir, file)
                os.remove(path)

        if "merrill" in org:
            org, cat, fname, mname, lname, dob, ssn, email, tele, street, city, state, sex, accno = mer_extract_details(
                file_name)
            det = extra_dets(file_name)
        elif "ameritrade" in org:
            org, cat, fname, mname, lname, dob, ssn, email, tele, street, city, state, sex, accno = ami_extract_details(
                file_name)
            det = extra_dets(file_name)
        elif "fidelity" in org:
            org, cat, fname, mname, lname, dob, ssn, email, tele, street, city, state, sex, accno = fid_extract_details(
                file_name)
            det = extra_dets(file_name)
        elif "charles schwab" in org:
            org, cat, fname, mname, lname, dob, ssn, email, tele, street, city, state, sex, accno = sch_extract_details(
                file_name)
            det = extra_dets(file_name)
        elif "driving license" in org:
            org, cat, fname, mname, lname, dob, ssn, email, tele, street, city, state, sex, accno = dl_extract_details(
                file_name)

        f.append(org)
        f1.append(cat)
        f2.append(fname)
        f3.append(mname)
        f4.append(lname)
        f5.append(dob)
        f6.append(ssn)
        f7.append(email)
        f8.append(tele)
        f9.append(street)
        f10.append(city)
        f11.append(state)
        f12.append(sex)
        f13.append(accno)
        f14.append(det)

    os.system("cls")
    print(f)
    print(f1)
    print(f2)
    print(f3)
    print(f4)
    print(f5)
    print(f6)
    print(f7)
    print(f8)
    print(f9)
    print(f10)
    print(f11)
    print(f12)
    print(f13)
    print(f14)

    # EMPTY UPLOAD FOLDER
    BASE_DIR = os.getcwd()
    dir = os.path.join(BASE_DIR, "uploads")

    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(dir, file)
            os.remove(path)

    return render_template('predict.html', org=org, cat=cat, fname=fname, mname=mname, lname=lname, dob=dob, ssn=ssn,
                           email=email, tele=tele, street=street, city=city, state=state, sex=sex, accno=accno,
                           selected=selected, unselected=unselected, det=det)


if __name__ == "__main__":
    app.run(debug=True)
