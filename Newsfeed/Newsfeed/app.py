from flask import Flask , render_template, request
import google_news
app = Flask(__name__)

outFile = ''

@app.route("/")
def main():
     print "Welcome!"
     return render_template('index.html')

@app.route('/uploadFile', methods=['POST'])
def upload():
    global outputFile
    filedata = request.files['upload']
    filename = filedata.filename
    print 'filename:' + filename
    inputFile = 'input/' + filename
    outputFile = 'output/' + filename + '_output'
    outputPath = 'templates/' + outputFile
    filedata.save(inputFile)
    print "Input Saved"

    print "processing starts" 
    
    google_news.news(inputFile,outputPath)

    print "processing success"
#processing

    return "success"

@app.route('/download')
def download():
    print 'download'
    print outputFile
    return render_template(outputFile)

if __name__ == "__main__":
    app.run()

