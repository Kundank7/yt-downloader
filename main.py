from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

# Create a download directory if it doesn't exist
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        resolution = request.form.get("resolution")
        unique_id = str(uuid.uuid4())
        output_path = os.path.join(DOWNLOAD_DIR, f"{unique_id}.mp4")

        ydl_opts = {
            'format': f'bestvideo[height<={resolution}]+bestaudio/best',
            'outtmpl': output_path,
            'merge_output_format': 'mp4'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return f"<h3>Error: {e}</h3>"

    return render_template("index.html")

# Add this block to support Render dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
