from src.app import create_app

if __name__ == '__main__':
    app = create_app()
    create_app().run(debug=False, port=7890)
