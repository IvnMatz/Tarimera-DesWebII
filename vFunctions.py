def processor(text):
    text.strip()
    processedT = ""
    for letter in text:
        if letter == "+":
            processedT += " "
        elif letter == " ":
            processedT += "+"
        else:
            processedT += letter
    
    return processedT

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS