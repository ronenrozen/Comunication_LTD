from comunication_ltd import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False, ssl_context=('cert.pem', 'key.pem'))
