# download_index.py
import os, requests, zipfile, io, sys

INDEX_URL = os.environ.get("INDEX_URL")  # set this in Render dashboard env vars
TARGET_DIR = "index"

def download_and_extract(url, outdir):
    if os.path.exists(outdir):
        print("Index folder already exists:", outdir)
        return
    if not url:
        print("INDEX_URL not set. Exiting.")
        sys.exit(1)
    print("Downloading index from:", url)
    r = requests.get(url, stream=True, timeout=600)
    r.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(outdir)
    print("Index extracted to:", outdir)

if __name__ == "__main__":
    download_and_extract(INDEX_URL, TARGET_DIR)
