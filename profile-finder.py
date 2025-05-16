import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import date
import requests
import json
from query import build_elasticsearch_query

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

def process_input(input):
  split_inputs = input.split(',')
  output = [split_input.strip() for split_input in split_inputs]

  return output

def calculate_yoe(profileDict): # not calculating it correctly --> only during nested? (e.g. multiple positions at same company)
  total_yoe = 0

  for experience in profileDict["experience"]:
    if experience["deleted"] == 0:
      if experience["date_to"] != None and experience["duration"] != None:
        temp = experience["duration"].split(" ")
        if (len(temp) == 4): # duration has years and months
          years = int(temp[0])
          months = int(temp[2])
          months_in_years = months / 12.0
          total_yoe = total_yoe + years + months_in_years
        elif (len(temp) == 2): # duration has only months
          months = int(temp[0])
          months_in_years = months / 12.0
          total_yoe += months_in_years
      else:
        if (experience["date_from_month"] != None):
          current_date = date.today()
          date_from = date(int(experience["date_from_year"]), int(experience["date_from_month"]), 1)
          
          years_diff = current_date.year - date_from.year
          months_diff = current_date.month - date_from.month

          diff = years_diff + (months_diff / 12.0)
          
          total_yoe += diff
  
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

  input_dict = input.__dict__
  payload = json.dumps(build_elasticsearch_query(input_dict))

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

  output_box = scrolledtext.ScrolledText(window, width=80, height=22)
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
    # degree = degree_entry.get()
    major = major_entry.get()
    education_institution = education_entry.get()
    skills = skills_entry.get()

    currInput = input()
    currInput.job_title = job_title
    currInput.location = location
    currInput.company = company
    currInput.years_of_experience = years_of_experience
    # currInput.degree = degree
    currInput.major = major
    currInput.education_institution = education_institution
    currInput.skills = skills

    searchResponse = call_coresignal_search_api(currInput)
    
    print(searchResponse)

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
    output_box.insert(tk.END, "Years of Experience: {:.2f}\n\n".format(calculate_yoe(responseDict)))

    for experience in responseDict["experience"]:
      if (experience["deleted"] == 0) and (company.lower().replace(" ", "") in experience["company_name"].lower().replace(" ", "")):
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
      if (education["deleted"] == 0) and (education_institution.lower().replace(" ", "") in education["institution"].lower().replace(" ", "")):
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
  run_profile_finder()

if __name__ == "__main__":
  main()