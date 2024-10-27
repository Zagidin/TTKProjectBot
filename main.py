from handlers import dp
from web_app import app
from bot.start_bot import start_bot


__all__ = ["dp"]


if __name__ == '__main__':
    # app.run(debug=True)
    start_bot()
