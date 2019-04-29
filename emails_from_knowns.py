# Generate unknown emails from knowns in same organization
# By John Oberlin  |  github.com/oberljn


import pandas as pd
import re


# Email handle patterns, with elements wrapped in <>
patterns = [
    "<first><last>",
    "<last><first>",
    "<f><last>",
    "<last><f>",
    "<first><l>",
    "<first>.<last>",
    "<last>.<first>",
    "<f>.<last>",
    "<last>.<f>",
    "<first>.<l>",
    "<first>_<last>",
    "<last>_<first>",
    "<f>_<last>",
    "<last>_<f>",
    "<first>_<l>", 
]


# Get CSV
# CSV columns must be labeled as:
# ID | Target_First | Target_Last | Known_Email | Known_First | Known_Last
# Sheet set up at https://docs.google.com/spreadsheets/d/1FRrvsdQIqe3Ri0B8nL80NLyeq63t8mGAcwksVjYnlck/edit?usp=sharing
df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTMWC_UTtPwt6pF3kp8kmsQnOINaQjQ8yDo6HJVwYhaRNvsWRfHbrXcoyD3FVNki2UnjzZCZFlZoYem/pub?gid=0&single=true&output=csv",
  dtype={"ID": str})
#df.head()


# Declare output as CSV
csv = "ID,Target_First,Target_Last,Target_Email,Known_First,Known_Last,Known_Email\n"

# Iterate over imported data
for index, row in df.iterrows():
  
  # Get and label elements of an email handle. Labels same format as patterns
  target = {
      "<first>":  row["Target_First"].lower(),
      "<f>":      row["Target_First"][0].lower(),
      "<last>":   row["Target_Last"].lower(),
      "<l>":      row["Target_Last"][0].lower()
  }
  known = {
      "<first>":  row["Known_First"].lower(),
      "<f>":      row["Known_First"][0].lower(),
      "<last>":   row["Known_Last"].lower(),
      "<l>":      row["Known_Last"][0].lower() 
  }
  
  # Break out handle and domain from known email
  index = row["Known_Email"].index("@")
  handle = row["Known_Email"][:index].lower()
  domain = row["Known_Email"][index:].lower()
  
  # Use handle patterns to reconstruct test handle from known first, last
  # If test matches known email handle, apply pattern to target
  result = False
  for p in patterns:
    test = p
    for label, element in known.items():
      test = test.replace(label,element)
    
    if test == handle: 
      target_handle = p
      for label_, element_ in target.items():
        target_handle = target_handle.replace(label_, element_)
      
      csv += row["ID"] + ","
      csv += row["Target_First"] + ","
      csv += row["Target_Last"] + ","
      csv += target_handle + domain + ","
      csv += row["Known_First"] + ","
      csv += row["Known_Last"] + ","
      csv += row["Known_Email"] + "\n"

      result = True
      
  if result == False:
    csv += row["ID"] + ","
    csv += row["Target_First"] + ","
    csv += row["Target_Last"] + ","
    csv += "No result,"
    csv += row["Known_First"] + ","
    csv += row["Known_Last"] + ","
    csv += row["Known_Email"] + "\n"

    
#print(csv)

with open("generated_emails.csv", "w") as f:
  f.write(csv)
