# Script to download assessments from AS.

import ASFunctions as asf
import json
import datetime
import os.path
import dateutil.parser

# set Prod | Dev | Test
target_server = "Prod"  # Prod | Dev | Test
asf.setServer(target_server)


my_name = __file__

# This makes sure the script can be run from any working directory and still find related files.
my_path = os.path.dirname(__file__)


now1 = datetime.datetime.now()
start_time = str(now1)
end_time = ""  # set later
# day_offset = now1.weekday() + 1 # Calculate the Sunday of current week
day_offset = 7  # use past seven days, regardless of current day

print("Script " + my_name + " begun at " + start_time + ". ")


output_dir = os.path.join(my_path, "output")
# TODO: output files to a more useful location.

the_repos = [3, 5, 4, 2]

for r in the_repos:
    out_file_name = "assessments_" + str(r) + ".json"
    out_path = os.path.join(output_dir, out_file_name)

    print("Saving assessments for repo " + str(r) + " in " + str(out_path))

    with open(out_path, "w+") as f:
        try:
            x = asf.getAssessments(r)
            f.write(x)
        except:
            raise ValueError("There was an error in getting assessment data!")

