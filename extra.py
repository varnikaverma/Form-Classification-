import json
import time
from requests import get, post

def parseJson(d):
   clean = {}
   for k, v in d.items():
      if isinstance(v, dict):
         nested = parseJson(v)
         if len(nested.keys()) > 0:
            clean[k] = nested
      elif v is not None:
         clean[k] = v
      if k == "organisation":
          del clean['organisation']
      if k == "category":
          del clean['category']
      if k == "first name":
          del clean['first name']
      if k == "middle name":
          del clean['middle name']
      if k == "last name":
          del clean['last name']
      if k == "dob":
          del clean['dob']
      if k == "ssn":
          del clean['ssn']
      if k == "email":
          del clean['email']
      if k == "telephone":
          del clean['telephone']
      if k == "street":
          del clean['street']
      if k == "city":
          del clean['city']
      if k == "state":
          del clean['state']
      if k == "account no":
          del clean['account no']
   return clean

def extra_dets(input):
    # Endpoint URL
    endpoint = r"https://ontology-form-recog.cognitiveservices.azure.com/"
    # Subscription Key
    apim_key = "423f2b248b1145b3b5d45ff00dff11c5"
    # Model ID
    model_id = "8be6106a-3c62-462f-8141-87c8a61e3a7b"
    # API version
    API_version = "v2.1-preview.2"

    post_url = endpoint + "/formrecognizer/%s/custom/models/%s/analyze" % (API_version, model_id)

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
                print("Running extra dets ......")
                data = resp_json
                for i in data["analyzeResult"]["documentResults"]:
                    clean_d = parseJson(i["fields"])
                    d = {}
                    for key in clean_d:
                        value = i["fields"][key]["text"]
                        d.update({key: value})
                    return(d)
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