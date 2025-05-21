import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json
import os
import time
from query import build_elasticsearch_query
from llm import call_openai, call_gemini, call_groq

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
        return json.dumps(contents_dict.get(key), indent=2)      
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

def process_input(input):
  split_inputs = input.split(',')
  output = [split_input.strip() for split_input in split_inputs]

  return output

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

def run_profile_finder():
  window = tk.Tk()
  window.title("Profile Finder")

  ttk.Label(window, text="Job Title:", font=(24)).grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
  job_title_entry = ttk.Entry(window, width=40)
  job_title_entry.grid(column=1, row=0, padx=5, pady=5)

  ttk.Label(window, text="Location:", font=(24)).grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
  location_entry = ttk.Entry(window, width=40)
  location_entry.grid(column=1, row=1, padx=5, pady=5)

  ttk.Label(window, text="Company:", font=(24)).grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
  company_entry = ttk.Entry(window, width=40)
  company_entry.grid(column=1, row=2, padx=5, pady=5)

  ttk.Label(window, text="Years of Experience:", font=(24)).grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
  yoe_entry = ttk.Entry(window, width=40)
  yoe_entry.grid(column=1, row=3, padx=5, pady=5)

  # ttk.Label(window, text="Degree:", font=(24)).grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
  # degree_entry = ttk.Entry(window, width=40)
  # degree_entry.grid(column=1, row=4, padx=5, pady=5)

  ttk.Label(window, text="Major:", font=(24)).grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
  major_entry = ttk.Entry(window, width=40)
  major_entry.grid(column=1, row=5, padx=5, pady=5)

  ttk.Label(window, text="Education Institution:", font=(24)).grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
  education_entry = ttk.Entry(window, width=40)
  education_entry.grid(column=1, row=6, padx=5, pady=5)

  ttk.Label(window, text="Skills:", font=(24)).grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
  skills_entry = ttk.Entry(window, width=40)
  skills_entry.grid(column=1, row=7, padx=5, pady=5)

  ttk.Label(window, text="Prompt:", font=(24)).grid(column=2, row=3, sticky=tk.W, padx=5, pady=5)
  text_area = tk.Text(window, width=54, height=4)
  text_area.grid(column=3, row=3, sticky=tk.W, padx=5, pady=5)

  output_box = scrolledtext.ScrolledText(window, width=84, height=22)
  output_box.grid(column=0, row=9, columnspan=2, padx=5, pady=5)

  llm_output_box = scrolledtext.ScrolledText(window, width=84, height=22)
  llm_output_box.grid(column=2, row=9, columnspan=2, padx=5, pady=5)

  def on_search():
    output_box.delete("1.0", tk.END)

    job_title = job_title_entry.get()
    location = location_entry.get()
    company =  company_entry.get()
    years_of_experience = yoe_entry.get()
    # degree = degree_entry.get()
    major = major_entry.get()
    education_institution = education_entry.get()
    skills = skills_entry.get()

    currInput = { # note: degree is not added here yet
      "job_title": job_title,
      "location": location,
      "company": company,
      "years_of_experience": years_of_experience,
      "major": major,
      "education_institution": education_institution,
      "skills": skills
    }

    searchResponse = call_coresignal_search_api(currInput)
    
    print(searchResponse)

    searchResponse = searchResponse[1:len(searchResponse) - 1]
    searchResponse = searchResponse.split(",")

    global profiles
    profiles = []
    for i in range(5): # change this to the number of profiles to display
      profile = check_in_cache(searchResponse[i])
      if profile != None: # check if available in cache
        profiles.append(profile)

        output_box.insert(tk.END, profile)
        continue
      
      else:
        print("Profile retrieved from Coresignal")
        collectResponse = call_coresignal_collect_api(searchResponse[i])

        responseDict = json.loads(collectResponse)

        if (responseDict.get("message", "all good") != "all good"):
          output_box.insert(tk.END, "No matching profiles found.")
          return
      
        output_box.insert(tk.END, json.dumps(responseDict, indent=2))

        profiles.append(json.dumps(responseDict, indent=2))
        store_in_cache(responseDict["id"], responseDict)
        
        time.sleep(2)

  def on_submit():
    prompt = text_area.get("1.0", tk.END)

    llm_output_box.delete("1.0", tk.END)

    response = call_gemini(prompt, "\n".join(profiles))

    llm_output_box.insert(tk.END, response)
  
  search_button = ttk.Button(window, text="Search", command=on_search)
  search_button.grid(column=0, row=8, columnspan=2, pady=10)
  
  submit_button = ttk.Button(window, text="Submit", command=on_submit)
  submit_button.grid(column=2, row=8, columnspan=2, pady=10)

  window.mainloop()
  
def main():
  run_profile_finder()

if __name__ == "__main__":
  main()