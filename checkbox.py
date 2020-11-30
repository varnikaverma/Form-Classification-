import json
import time
from requests import get, post

def getSelected(dct, value):
    return [key for key in dct if (dct[key]["text"] == value)]


def getUnselected(dct, value):
    return [key for key in dct if (dct[key]["text"] == value)]

def composed_model_details(input):
    selected_cb = []
    unselected_cb = []
    org = ""
    cat = ""

    print(input)

    # Endpoint URL
    endpoint = r"https://ontology-form-recog.cognitiveservices.azure.com/"
    # Subscription Key
    apim_key = "423f2b248b1145b3b5d45ff00dff11c5"
    # Model ID
    model_id = "861c058f-2f19-4973-b847-220335f4e156"
    # API version
    API_version = "v2.1-preview.2"

    post_url = endpoint + "/formrecognizer/%s/custom/models/%s/analyze" % (API_version, model_id)

    params = {
        "includeTextDetails": True
    }

    headers = {
        # Request headers
        'Content-Type': 'image/png',
        'Ocp-Apim-Subscription-Key': apim_key,
    }
    with open(input, 'rb') as f:
        data_bytes = f.read()
    try:
        resp = post(url=post_url, data=data_bytes, headers=headers, params=params)
        if resp.status_code != 202:
            print("POST analyze failed:\n%s" % json.dumps(resp.json()))
            quit()
        #print("POST analyze succeeded:\n%s" % resp.headers)
        get_url = resp.headers["operation-location"]
    except Exception as e:
        print("POST analyze failed:\n%s" % str(e))
        quit()

    n_tries = 15
    n_try = 0
    wait_sec = 5
    max_wait_sec = 60

    while n_try < n_tries:
        try:
            resp = get(url=get_url, headers={"Ocp-Apim-Subscription-Key": apim_key})
            resp_json = resp.json()
            if resp.status_code != 200:
                #print("GET analyze results failed:\n%s" % json.dumps(resp_json))
                quit()
            status = resp_json["status"]
            if status == "succeeded":
                #print("Running......")
                data = resp_json
                for i in data["analyzeResult"]["documentResults"]:
                    org = i["fields"]["organization"]["text"]
                    cat = i["fields"]["category"]["text"]
                    selected_cb = getSelected(i["fields"], "selected")
                    unselected_cb = getUnselected(i["fields"], "unselected")

                    return org, cat, selected_cb, unselected_cb
                quit()
            if status == "failed":
                print("Analysis failed:\n%s" % json.dumps(resp_json))
                quit()
            # Analysis still running. Wait and retry.
            time.sleep(wait_sec)
            n_try += 1
            wait_sec = min(2 * wait_sec, max_wait_sec)
        except Exception as e:
            msg = "GET analyze results failed:\n%s" % str(e)
            print(msg)
            quit()
    print("Analyze operation did not complete within the allocated time.")

