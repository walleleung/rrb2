from app import create_app

app = create_app('default')

if __name__ == '__main__':
    # manager.run()
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run()