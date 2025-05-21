import json

html = "<html><head><title>Output</title></head><body>"

with open("example-json-output.json", "r") as json_file, open("output.html", "w") as output_file:
  json_data = json_file.read()
  json_data_dict = json.loads(json_data)

  for profile in json_data_dict:
    for key, value in profile.items():
      if key == "LinkedIn":
        html = html + f"<a href={value}>LinkedIn Profile</a>"
      else:
        html = html + f"<p>{key}: {value}<p>"
    html += "<br>=======================================================================</br>"

  html += "</body></html>"

  output_file.write(html)