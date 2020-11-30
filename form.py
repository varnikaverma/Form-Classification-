import json
import time
from requests import get, post
import os

def extract_details(input):
    # Endpoint URL
    endpoint = r"https://extract-form.cognitiveservices.azure.com/"
    apim_key = "c083fcec96d542db80be71af00c0ee09"
    model_id = "61f7e1fd-e5d8-49ce-9738-a78230ffd7d9"
    post_url = endpoint + "formrecognizer/v2.0/custom/models/%s/analyze" % model_id
    #source = r'samplecra.pdf'
    params = {
        "includeTextDetails": True
    }

    headers = {
        # Request headers
        'Content-Type': 'application/pdf',
        'Ocp-Apim-Subscription-Key': apim_key,
    }
    with open(input, 'rb') as f:
        data_bytes = f.read()
    try:
        resp = post(url=post_url, data=data_bytes, headers=headers, params=params)
        if resp.status_code != 202:
            # print("POST analyze failed:\n%s" % json.dumps(resp.json()))
            quit()
        # print("POST analyze succeeded:\n%s" % resp.headers)
        get_url = resp.headers["operation-location"]
    except Exception as e:
        # print("POST analyze failed:\n%s" % str(e))
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
                print("GET analyze results failed:\n%s" % json.dumps(resp_json))
                quit()
            status = resp_json["status"]
            if status == "succeeded":
                print("Running......")
                data = resp_json

                for i in data["analyzeResult"]["documentResults"]:
                    if (i["docType"] == "custom:form"):
                        if i["fields"]["organisation"] is None:
                            org = "Not present"
                        else:
                            print("Organisation : ", i["fields"]["organisation"]["text"])
                            org = i["fields"]["organisation"]["text"]
                        if i["fields"]["category"] is None:
                            cat = "Not present"
                        else:
                            print("Category : ", i["fields"]["category"]["text"])
                            cat = i["fields"]["category"]["text"]
                        return org, cat

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