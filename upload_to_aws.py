import requests


def execute_curl_request(url, username, password, json_file_path):
    with open(json_file_path, "rb") as json_file:
        json_data = json_file.read()

    auth = (username, password)

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, auth=auth, data=json_data, headers=headers)

    if response.status_code == 200:
        print("Requête exécutée avec succès !")
    else:
        print(
            f"Erreur lors de l'exécution de la requête. Code de réponse : {response.status_code}"
        )
        print(response.text)


if __name__ == "__main__":
    url = "https://search-pa-auto-driving-data-awet7az4c26j4mo73xaho73hzy.us-east-1.es.amazonaws.com/_bulk"
    username = "admin"
    password = "#########"
    json_file_path = "telemetry_acct.json"

    execute_curl_request(url, username, password, json_file_path)
