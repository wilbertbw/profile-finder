import json

html = "<html><head><title>Output</title></head><body>"

with open("example-json-output.json", "r") as json_file, open("output.html", "w") as output_file:
  json_data = json_file.read()
  json_data_dict = json.loads(json_data)

  for profile in json_data_dict:
    html = html + "<h3>" + profile["name"] + "</h3>"
    html = html + "<p>Experience: " + profile["experience"] + "</p>"
    html = html + "<p>Education: " + profile["education"] + "</p>"
    html = html + "<p>Major: " + profile["major"] + "</p>"

  html += "</body></html>"

  output_file.write(html)