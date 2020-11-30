import json
import time
from requests import get, post
import os

def dl_extract_details(input):
    # Endpoint URL
    endpoint = r"https://extract-form.cognitiveservices.azure.com/"
    apim_key = "c083fcec96d542db80be71af00c0ee09"
    model_id = "a1721ef0-0173-41a8-9d28-9e1e4b5fd31a"
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
                        if i["fields"]["category"] is None:
                            cat = "Not present"
                        else:
                            print("Category : ", i["fields"]["category"]["text"])
                            cat = i["fields"]["category"]["text"]
                        if i["fields"]["first name"] is None:
                            fn = ""
                        else:
                            print("First Name: ", i["fields"]["first name"]["text"])
                            fn = i["fields"]["first name"]["text"]
                        if i["fields"]["middle name"] is None:
                            mn = ""
                        else:
                            print("Middle Name: ", i["fields"]["middle name"]["text"])
                            mn = i["fields"]["middle name"]["text"]
                        if i["fields"]["last name"] is None:
                            ln = ""
                        else:
                            print("First Name: ", i["fields"]["last name"]["text"])
                            ln = i["fields"]["last name"]["text"]
                        if i["fields"]["dob"] is None:
                            d = "Not present"
                        else:
                            print("DOB : ", i["fields"]["dob"]["text"])
                            d = i["fields"]["dob"]["text"]
                        if i["fields"]["street"] is None:
                            s = "Not present"
                        else:
                            print("Street : ", i["fields"]["street"]["text"])
                            s = i["fields"]["street"]["text"]
                        if i["fields"]["city"] is None:
                            c = "Not present"
                        else:
                            print("City : ", i["fields"]["city"]["text"])
                            c = i["fields"]["city"]["text"]
                        if i["fields"]["gender"] is None:
                            sex = "Not present"
                        else:
                            print(i["fields"]["gender"]["text"])
                            sex = i["fields"]["gender"]["text"]

                        org = "Not present"
                        ssn = "Not present"
                        email = "Not present"
                        tele = "Not present"
                        acc = "Not present"
                        st = "Not present"

                        return org, cat, fn, mn, ln, d, ssn, email, tele, s, c, st, sex, acc

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
