import requests

API_BASE = "https://personne2-task-functions-gxayfpbkgyfwcedg.belgiumcentral-01.azurewebsites.net/api"
API_KEY  = "g3xvSGpj6sQ52Xb9GoY8jA8mDAtZpyLC2aiFhRK2ju8tAzFuDp4pbA=="


def upload_file(file, filename):
    response = requests.post(
        f"{API_BASE}/files/upload",
        params={"filename": filename, "code": API_KEY},
        data=file.read()
    )
    return response.json().get("fileName", filename)


def download_file(filename, destination):
    response = requests.get(
        f"{API_BASE}/files/download",
        params={"filename": filename, "code": API_KEY},
        stream=True
    )
    with open(destination, "wb") as f:
        f.write(response.content)
    print("Download successful!")


def delete_file(filename):
    requests.delete(
        f"{API_BASE}/files/delete",
        params={"filename": filename, "code": API_KEY}
    )
    print("Delete successful!")


def list_files():
    response = requests.get(
        f"{API_BASE}/files",
        params={"code": API_KEY}
    )
    data = response.json()
    return [f["name"] for f in data.get("files", [])]