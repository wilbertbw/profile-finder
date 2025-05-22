def convertJSONToHTML(profile):
  html = "<html><head><title>Output</title></head><body>"

  with open("output.html", "a") as output_file:
    for key, value in profile.items():
      if key == "LinkedIn":
        html = html + f"<a href={value} style=\"font-size:20px;\">LinkedIn Profile</a>"
      else:
        html = html + f"<p style=\"font-size:20px;\">{key}: {value}<p>"
    html += "<br>=======================================================================</br>"
    html += "</body></html>"

    output_file.write(html)