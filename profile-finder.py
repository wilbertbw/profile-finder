import requests
import json
import os
import time
from query import build_elasticsearch_query
from llm import call_openai, call_gemini, call_groq
from convert import convertJSONToHTML

def check_in_cache(profile_id):
  with open("cache.json", "r") as file:
    contents = file.read()

    if contents.strip() == "": # file empty
      return None
    else: # file not empty
      key = f"{profile_id}"
      contents_dict = json.loads(contents)

      if (contents_dict.get(key)): # profile in cache
        print("Profile retrieved from cache")
        return contents_dict.get(key)
      else: # profile not in cache
        return None


def store_in_cache(profile_id, profile_dict):
  with open("cache.json", "r") as file:
    contents = file.read()
  
  if contents.strip() == "": # when file is empty
    with open("cache.json", "w") as file:
      dict_to_write = {}
      key = f"{profile_id}"
      dict_to_write[key] = profile_dict
      
      json_format = json.dumps(dict_to_write, indent=2)
      file.write(json_format)

  else: # when file is not empty
    with open("cache.json", "w") as file:
      contents_dict = json.loads(contents)
      key = f"{profile_id}"
      contents_dict[key] = profile_dict

      json_format = json.dumps(contents_dict, indent=2)
      file.write(json_format)
  
  return

def call_coresignal_search_api(input):
  coresignalURL = "https://api.coresignal.com/cdapi/v2/employee_base/search/es_dsl"

  payload = json.dumps(build_elasticsearch_query(input))

  headers = {
      'accept': 'application/json',
      'Content-Type': 'application/json',
      'apikey': os.environ.get("coresignal_api_key")
  }

  response = requests.request("POST", coresignalURL, headers=headers, data=payload)

  return response.text

def call_coresignal_collect_api(profile_id):
  coresignalURL = "https://api.coresignal.com/cdapi/v2/employee_base/collect/" + profile_id

  headers = {
      'accept': 'application/json',
      'apikey': os.environ.get("coresignal_api_key")
  }

  response = requests.request("GET", coresignalURL, headers=headers)

  return response.text

def read_spec_file(filename):
  file = open(filename)
  contents = file.read()
  contents_dict = json.loads(contents)

  return contents_dict

def read_prompt_file(filename):
  file = open(filename)
  contents = file.read()
  
  return contents

def search_profile(input_dict):
  currInput = {
    "job_title": input_dict["job_title"],
    "location": input_dict["location"],
    "company": input_dict["company"],
    "years_of_experience": input_dict["years_of_experience"],
    "major": input_dict["major"],
    "education_institution": input_dict["education_institution"],
    "skills": input_dict["skills"]
  }
  num_profiles = input_dict["num_profiles"]

  searchResponse = call_coresignal_search_api(currInput)

  print(searchResponse)

  searchResponse = searchResponse[1:len(searchResponse) - 1]
  searchResponse = searchResponse.split(",")

  profiles = []
  for i in range(int(num_profiles)):
    profile = check_in_cache(searchResponse[i])
    if profile != None: # check if available in cache
      profiles.append(profile)
      continue
    
    else:
      print("Profile retrieved from Coresignal")
      collectResponse = call_coresignal_collect_api(searchResponse[i])

      responseDict = json.loads(collectResponse)

      if (responseDict.get("message", "all good") != "all good"):
        print("No matching profiles found.")
        return

      profiles.append(responseDict)
      store_in_cache(responseDict["id"], responseDict)
      
      time.sleep(2)
  
  with open("search_output.json", "w") as file:
    file.write(json.dumps(profiles, indent=2))
  
  return profiles

def call_llm(prompt, profiles):
  responses = call_gemini(prompt, profiles)
  convertJSONToHTML(responses)

  with open("llm_output.json", "w") as file:
    file.write(json.dumps(responses, indent=2))

  return
  
def main():
  spec_filename = input("Specifications filename (.txt): ")
  prompt_filename = input("Input filename (.txt file or default-prompt.txt): ")

  specs_dict = read_spec_file(spec_filename)
  profiles = search_profile(specs_dict)

  prompt = read_prompt_file(prompt_filename)
  call_llm(prompt, profiles)

  print("Process finished. Raw search outputs are in search_output.json and the LLM outputs are in llm_output.json.")

  return

if __name__ == "__main__":
  main()