from app import create_app

app = create_app()

app.jinja_env.auto_reload = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)