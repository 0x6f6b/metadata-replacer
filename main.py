# iterate through json files in the existing_metadata folder

from pathlib import Path
import json
import os
import shutil
from progress.bar import Bar

# get all files in the existing_metadata folder
files = Path('existing_metadata').glob('*.json')

rank_to_set = "Sergeant"

# iterate through all files
progress_bar = Bar('Processing', max=len(os.listdir('existing_metadata')))
for file in files:
  # increment progress bar
  progress_bar.next()

  filename_without_extension = file.stem
  
  data = json.loads(file.read_text())

  data["721"]["<policy_id>"][filename_without_extension]["legionData"]["Rank"] = rank_to_set


  head = data["721"]["<policy_id>"][filename_without_extension]["attributes"]["Head"]
  background = data["721"]["<policy_id>"][filename_without_extension]["attributes"]["Background"]
  armour = data["721"]["<policy_id>"][filename_without_extension]["equipment"]["Armour"]
  weapon = data["721"]["<policy_id>"][filename_without_extension]["equipment"]["Weapon"]
  accessory = data["721"]["<policy_id>"][filename_without_extension]["equipment"]["Accessory"]

  # print("Head: " + head)
  # print("Background: " + background)
  # print("Armour: " + armour)
  # print("Weapon: " + weapon)

  # iterate through all of the files within the new_metadata folder
  for new_file in Path('new_metadata').glob('*.json'):
    new_filename_without_extension = new_file.stem
    new_data = json.loads(new_file.read_text())
    
    new_head = new_data["721"]["<policy_id>"][new_filename_without_extension]["Head"]
    new_background = new_data["721"]["<policy_id>"][new_filename_without_extension]["Background"]
    new_armour = new_data["721"]["<policy_id>"][new_filename_without_extension]["Armour"]
    new_weapon = new_data["721"]["<policy_id>"][new_filename_without_extension]["Weapon"]
    new_accessory = new_data["721"]["<policy_id>"][new_filename_without_extension]["Accessory"]
  
    # if any four of the attributes match, output the one that doesn't match
    matches = {
      "Head": head == new_head,
      "Background": background == new_background,
      "Armour": armour == new_armour,
      "Weapon": weapon == new_weapon,
      "Accessory": accessory == new_accessory
    }
  
    # count the number that match
    count = 0
    for key, value in matches.items():
      if value:
        count += 1

    # if all four match, output the one that doesn't match
    if count == 4:
      # output the key that has a false value
      for key, value in matches.items():
        if not value:
          new_filename = rank_to_set + filename_without_extension[filename_without_extension.find(" "):]

          data["721"]["<policy_id>"][filename_without_extension]["equipment"]["Accessory"] = new_accessory
          data["721"]["<policy_id>"][new_filename] = data["721"]["<policy_id>"].pop(filename_without_extension)
          data["721"]["<policy_id>"][new_filename]["name"] = new_filename

          # copy the image with the name new_filename_without_extension.png to the generated folder from new_images and rename it to filename_without_extension.png
          newImage = "new_images/" + new_filename_without_extension + ".png"
          outputdir = "generator/"
          # copy the newImage to the outputdir relative to the current directory (windows)
          shutil.copy(newImage, outputdir + new_filename + ".png")

          
          # write the "data" to a new file in the generator folder
          # replace the first word of filename_without_extension with the variable "rank_to_set"
          
          with open('generator/' + new_filename + '.json', 'w') as outfile:
            json.dump(data, outfile)




