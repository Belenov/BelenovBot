from main import app


if __name__ == '__main__':
    app.start()
    app.send_message("me", "Session is created!")
    app.stop()
