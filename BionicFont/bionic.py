import os.path
import PySimpleGUI as sg
import PyPDF2
import http.client
import webbrowser

#funtion to create and run gui
def gui():
    layout = [
        [sg.Text('Select a PDF file to translate:')],
        [sg.Input(key='file'), sg.FileBrowse()],
        [sg.Button('OK'), sg.Button('Cancel')]
    ]

    # Create the window
    window = sg.Window('PDF Input', layout)

    # Event loop to process events
    while True:
        event, values = window.read()

        # If the OK button is clicked
        if event == 'OK':
            # Get the file path from the input field
            file_path = values['file']
            # Open the PDF file and do something with it
            with open(file_path, 'rb') as file:
                #call translation file to work with pdf
                FileHandling(file)
                pass

        # If the Cancel button is clicked or the window is closed
        if event in (None, 'Cancel'):
            break

    # Close the window
    window.close()

#function to handle the translation of the pdf
def FileHandling(file):
    pdf = PyPDF2.PdfFileReader(file)
    num_pages = pdf.getNumPages()
    text = ""

    for page_num in range(num_pages):
        page = pdf.getPage(page_num)
        text += page.extractText() 

    Translation(text)    



def Translation(text):
    conn = http.client.HTTPSConnection("bionic-reading1.p.rapidapi.com")
    payload = "content={}&response_type=html&request_type=html&fixation=1&saccade=10".format(text)

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'X-RapidAPI-Key': "b5f9086debmsh9729b86df5f7197p19256djsn4d6bb5e2634c",
        'X-RapidAPI-Host': "bionic-reading1.p.rapidapi.com"
        }

    conn.request("POST", "/convert", payload.encode("utf-8"), headers)

    res = conn.getresponse()
    data = res.read()

    output(data)


def output(data):
    with open("bionic.html", "w") as f:
        f.write(data.decode("utf-8"))

    webbrowser.open("bionic.html")

gui()