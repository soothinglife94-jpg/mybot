from flask import Flask, request, redirect
import bot  # shares visited_users with bot.py

app = Flask(__name__)

AD_URL = "https://omg10.com/4/11066405"  # your real ad link here

@app.route("/visit")
def visit():
    user_id = request.args.get("user_id")
    if user_id:
        bot.visited_users.add(int(user_id))
    return redirect(AD_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)