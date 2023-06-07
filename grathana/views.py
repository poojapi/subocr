from flask import Blueprint, send_file, request, render_template
import logging
import os
from doc_curation import pdf
#from google.oauth2 import service_account
#import googleapiclient.discovery 
#from google.oauth2 import service_account  # type: ignore

bp = Blueprint("site", __name__)

directory = '/Users/poojaprakash/Downloads/subocr/'

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger() 

fileList = []

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/bijavapa")
def setup_ocr():	
    return render_template("setup-ocr.html")

@bp.route("/grathana")
def grathana():
    return render_template("grathana.html")

@bp.route("/bijavapa-result")
def setup_result():	
    acct = create_service_account('subhixa-ocr','subhixa-ocr', 'subhixa-ocr-service'  )
    return render_template("do-ocr.html")

@bp.route("/do_ocr", methods = ['GET', 'POST', 'DELETE'])
def do_ocr():	
    #upload file 
    if request.method == 'POST':
        """modify/update the information for <user_id>"""
        # you can use <user_id>, which is a str but could
        # changed to be int or whatever you want, along
        # with your lxml knowledge to make the required
        # changes
        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        logger.info(file)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # filename = secure_filename(file.filename)
            file.save(os.path.join(directory+"files", file.filename))
            fileList.append(file.filename)
            
            return 'Done' 
    
@bp.route("/ocr")
def ocr():
    file = request.args.to_dict().get('file')
    #change directory of service-account-key accordingly
    key="/Users/poojaprakash/Downloads/subhixa-ocr-bccca51b3dcc.json"
    print(file)
    p=directory+str(file)
    
    pdf.split_and_ocr_on_drive(p,key,small_pdf_pages=20)
    
    return send_file(os.path.join(directory, str(file) + '.txt' ))  

def create_service_account(project_id: str, name: str, display_name: str) -> dict:
    """Creates a service account."""

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    my_service_account = service.projects().serviceAccounts().create(
        name='projects/' + project_id,
        body={
            'accountId': name,
            'serviceAccount': {
                'displayName': display_name
            }
        }).execute()

    print('Created service account: ' + my_service_account['email'])
    return my_service_account
 

