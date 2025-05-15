# from utils import build_elasticsearch_query
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import date
import requests
import json


class input:
  def __init__(self):
    self.job_title = ""
    self.company = ""
    self.years_of_experience = ""
    self.location = ""
    self.degree = ""
    self.major = ""
    self.education_institution = ""
    self.skills = ""

def process_input(input): # capitalize the first letter (when necessary)
  split_inputs = input.split(',')
  output = [split_input.strip() for split_input in split_inputs]

  return output

def calculate_yoe(profileDict):
  total_yoe = 0

  for experience in profileDict["experience"]:
    if experience["deleted"] == 0:
      if experience["date_to"] != None:
        total_yoe += int(experience["duration"])
      else:
        currentYear = date.today().year
        total_yoe += (currentYear - int(experience["date_from_year"]))
  
  return total_yoe

def filter_by_yoe(yoe_requirement, profiles):
  result = [];

  for profile in profiles:
    yoe = calculate_yoe(profile)
    if (yoe >= yoe_requirement):
      result.append(profile)
  
  return result


def call_coresignal_search_api(input):
  coresignalURL = "https://api.coresignal.com/cdapi/v2/employee_base/search/es_dsl"

  # input_dict = input.__dict__
  # payload = json.dumps(build_elasticsearch_query(input_dict))

  # note: for experience and education, it is possible that the one in the search requirements isn't the first one in the profile
  # so might need to find it

  payload = json.dumps({
    "query": {
      "bool": {
        "must": [
          {
            "term": {
              "is_parent": 1
            }
          },
          {
            "term": {
              "deleted": 0
            }
          },
          {
            "match": {
              "location": input.location
            }
          },
          {
            "nested": {
              "path": "experience",
              "query": {
                "bool": {
                  "must": [
                    {
                      "match_phrase": {
                        "experience.company_name": f"\"{input.company}\""
                      }
                    },
                    {
                      "match": {
                        "experience.title": input.job_title
                      }
                    },
                    {
                      "term": {
                        "experience.deleted": 0
                      }
                    }
                  ]
                }
              }
            }
          },
          {
            "nested": {
              "path": "education",
              "query": {
                "bool": {
                  "must": [
                    {
                      "match_phrase": {
                        "education.institution": f"\"{input.education_institution}\""
                      }
                    },
                    {
                      "match": {
                        "education.program": input.major
                      }
                    },
                    {
                      "term": {
                        "education.deleted": 0
                      }
                    }
                  ]
                }
              }
            }
          },
          {
            "nested": {
              "path": "skills",
              "query": {
                "bool": {
                  "must": [
                    {
                      "match": {
                        "skills.skill": input.skills
                      }
                    }
                  ]
                }
              }
            }
          }
        ]
      }
    }
  })

  headers = {
      'accept': 'application/json',
      'Content-Type': 'application/json',
      'apikey': 'lDIWfl32thDy12HTg64rsyY9vEmHGW1M'
  }

  response = requests.request("POST", coresignalURL, headers=headers, data=payload)

  return response.text

def call_coresignal_collect_api(profile_id):
  coresignalURL = "https://api.coresignal.com/cdapi/v2/employee_base/collect/" + profile_id

  headers = {
      'accept': 'application/json',
      'apikey': 'lDIWfl32thDy12HTg64rsyY9vEmHGW1M'
  }

  response = requests.request("GET", coresignalURL, headers=headers)

  return response.text

def run_profile_finder():
  window = tk.Tk()
  window.title("Profile Finder")

  ttk.Label(window, text="Job Title:").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
  job_title_entry = ttk.Entry(window, width=40)
  job_title_entry.grid(column=1, row=0, padx=5, pady=5)

  ttk.Label(window, text="Location:").grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
  location_entry = ttk.Entry(window, width=40)
  location_entry.grid(column=1, row=1, padx=5, pady=5)

  ttk.Label(window, text="Company:").grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
  company_entry = ttk.Entry(window, width=40)
  company_entry.grid(column=1, row=2, padx=5, pady=5)

  ttk.Label(window, text="Years of Experience:").grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
  yoe_entry = ttk.Entry(window, width=40)
  yoe_entry.grid(column=1, row=3, padx=5, pady=5)

  ttk.Label(window, text="Degree:").grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
  degree_entry = ttk.Entry(window, width=40)
  degree_entry.grid(column=1, row=4, padx=5, pady=5)

  ttk.Label(window, text="Major:").grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
  major_entry = ttk.Entry(window, width=40)
  major_entry.grid(column=1, row=5, padx=5, pady=5)

  ttk.Label(window, text="Education Institution:").grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
  education_entry = ttk.Entry(window, width=40)
  education_entry.grid(column=1, row=6, padx=5, pady=5)

  ttk.Label(window, text="Skills:").grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
  skills_entry = ttk.Entry(window, width=40)
  skills_entry.grid(column=1, row=7, padx=5, pady=5)

  output_box = scrolledtext.ScrolledText(window, width=80, height=15)
  output_box.grid(column=0, row=9, columnspan=2, padx=5, pady=5)

  def on_search():
    # the values below are arrays
    # job_title = process_input(job_title_entry.get())
    # location = process_input(location_entry.get())
    # company =  process_input(company_entry.get())
    # years_of_experience = process_input(yoe_entry.get())
    # degree = process_input(degree_entry.get())
    # major = process_input(major_entry.get())
    # education = process_input(education_entry.get())
    # skills = process_input(skills_entry.get())

    output_box.delete("1.0", tk.END)

    job_title = job_title_entry.get()
    location = location_entry.get()
    company =  company_entry.get()
    years_of_experience = yoe_entry.get()
    degree = degree_entry.get()
    major = major_entry.get()
    education_institution = education_entry.get()
    skills = skills_entry.get()

    currInput = input()
    currInput.job_title = job_title
    currInput.location = location
    currInput.company = company
    currInput.years_of_experience = years_of_experience
    currInput.degree = degree
    currInput.major = major
    currInput.education_institution = education_institution
    currInput.skills = skills

    searchResponse = call_coresignal_search_api(currInput)

    searchResponse = searchResponse[1:len(searchResponse) - 1]
    searchResponse = searchResponse.split(",")

    collectResponse = call_coresignal_collect_api(searchResponse[0])

    responseDict = json.loads(collectResponse)

    if (responseDict.get("message", "all good") != "all good"):
      output_box.insert(tk.END, "No matching profiles found.")
      return

    # print()
    # print(responseDict)
    # print()
    # print(responseDict["experience"])
    # print()
    # print(responseDict["education"])
    # print()
    # print(responseDict["skills"])
    # print()

    output_box.insert(tk.END, f"Full Name: {responseDict["full_name"]}\n\n")
    output_box.insert(tk.END, f"Profile Link: {responseDict["profile_url"]}\n\n")
    output_box.insert(tk.END, f"Location: {responseDict["location"]}\n\n")

    # output_box.insert(tk.END, f"Years of Experience: {calculate_yoe(responseDict)}\n")

    for experience in responseDict["experience"]:
      if (experience["deleted"] == 0) and (company.lower().replace(" ", "") in experience["company_name"].lower().replace(" ", "")): # might want to normalize all strings before doing this (all lowercase, remove spaces)
        if experience["date_to"] != None:
          if experience["date_from"] == None:
            output_box.insert(tk.END, f"Company: {experience["company_name"]} (unknown - {experience["date_to"]})\n")
            output_box.insert(tk.END, f"  Job Title: {experience["title"]}\n\n")
          else:
            output_box.insert(tk.END, f"Company: {experience["company_name"]} ({experience["date_from"]} - {experience["date_to"]})\n")
            output_box.insert(tk.END, f"  Job Title: {experience["title"]}\n\n")
        else:
          if experience["date_from"] == None:
            output_box.insert(tk.END, f"Company: {experience["company_name"]} (unknown)\n")
            output_box.insert(tk.END, f"  Job Title: {experience["title"]}\n\n")
          else:
            output_box.insert(tk.END, f"Company: {experience["company_name"]} ({experience["date_from"]} - present)\n")
            output_box.insert(tk.END, f"  Job Title: {experience["title"]}\n\n")

    # output_box.insert(tk.END, f"Degree: {degree}\n")

    for education in responseDict["education"]:
      if (education["deleted"] == 0) and (education_institution.lower().replace(" ", "") in education["institution"].lower().replace(" ", "")): # might want to normalize all strings before doing this (all lowercase, remove spaces)
        if education["date_to"] != None:
          if education["date_from"] == None:
            output_box.insert(tk.END, f"Education Institution: {education["institution"]} (unknown - {education["date_to"]})\n")
            output_box.insert(tk.END, f"  Major: {education["program"]}\n\n")
          else:
            output_box.insert(tk.END, f"Education Institution: {education["institution"]} ({education["date_from"]} - {education["date_to"]})\n")
            output_box.insert(tk.END, f"  Major: {education["program"]}\n\n")
        else:
          if education["date_from"] == None:
            output_box.insert(tk.END, f"Education Institution: {education["institution"]} (unknown)\n")
            output_box.insert(tk.END, f"  Major: {education["program"]}\n\n")
          else:
            output_box.insert(tk.END, f"Education Institution: {education["institution"]} ({education["date_from"]} - present)\n")
            output_box.insert(tk.END, f"  Major: {education["program"]}\n\n")
    
    skill_str = "Skills: "
    for i in range(len(responseDict["skills"])):
      curr_skill = responseDict["skills"][i]

      if (curr_skill["deleted"] == 1):
        skill_str += curr_skill["skill"]
        if (i != len(responseDict["skills"]) - 1):
          skill_str += ", "
        else:
          skill_str += "\n"

    output_box.insert(tk.END, skill_str)
  
  search_button = ttk.Button(window, text="Search", command=on_search)
  search_button.grid(column=0, row=8, columnspan=2, pady=10)

  window.mainloop()
  
def main():
  test = input()
  test.job_title = "Software Engineer"
  test.location = "New York"
  test.company = "Google"
  test.years_of_experience = "3"
  test.degree = "Bachelor's"
  test.major = "Computer Science"
  test.education_institution = "Carnegie Mellon University"
  test.skills = "C++"
  # call_coresignal_search_api(test)

  run_profile_finder()

if __name__ == "__main__":
  main()