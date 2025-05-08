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
  
import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json

def process_input(input): # capitalize the first letter (when necessary)
  split_inputs = input.split(',')
  output = [split_input.strip() for split_input in split_inputs]

  return output

def create_search_query(input):
  coresignalURL = "https://api.coresignal.com/cdapi/v2/employee_base/search/filter"

  payload = json.dumps({
    "location": input.location,
    "experience_title": input.job_title,
    "experience_company_name": input.company,
    "education_program_name": input.major,
    "education_institution_name": input.education_institution,
    "skill": input.skills
  })

  headers = {
      'accept': 'application/json',
      'Content-Type': 'application/json',
      'apikey': 'api_key'
  }

  response = requests.request("POST", coresignalURL, headers=headers, data=payload)

  print(response.text)
  return

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
    # note: these values below are arrays
    job_title = process_input(job_title_entry.get())
    location = process_input(location_entry.get())
    company =  process_input(company_entry.get())
    years_of_experience = process_input(yoe_entry.get())
    degree = process_input(degree_entry.get())
    major = process_input(major_entry.get())
    education = process_input(education_entry.get())
    skills = process_input(skills_entry.get())

    currInput = input()
    currInput.job_title = job_title
    currInput.location = location
    currInput.company = company
    currInput.years_of_experience = years_of_experience
    currInput.degree = degree
    currInput.major = major
    currInput.education_institution = education
    currInput.skills = skills

    response = create_search_query(currInput)

    output_box.delete("1.0", tk.END)

    output_box.insert(tk.END, f"Job Title: {job_title}\n")
    output_box.insert(tk.END, f"Location: {location}\n")
    output_box.insert(tk.END, f"Company: {company}\n")
    output_box.insert(tk.END, f"Years of Experience: {years_of_experience}\n")
    output_box.insert(tk.END, f"Degree: {degree}\n")
    output_box.insert(tk.END, f"Major: {major}\n")
    output_box.insert(tk.END, f"Education Institution: {education}\n")
    output_box.insert(tk.END, f"Skills: {skills}\n")
  
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
  create_search_query(test)

if __name__ == "__main__":
  main()