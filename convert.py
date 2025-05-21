import json

def convertJSONToHTML(llm_output):
  llm_output = llm_output[8:-4] # remove the ```json at the start and the ``` at the end of the LLM response

  html = "<html><head><title>Output</title></head><body>"

  profiles = json.loads(llm_output)

  with open("output.html", "w") as output_file:
    for profile in profiles:
      for key, value in profile.items():
        if key == "LinkedIn":
          html = html + f"<a href={value} style=\"font-size:20px;\">LinkedIn Profile</a>"
        else:
          html = html + f"<p style=\"font-size:20px;\">{key}: {value}<p>"
      html += "<br>=======================================================================</br>"

    html += "</body></html>"

    output_file.write(html)