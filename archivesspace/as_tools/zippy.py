from shutil import make_archive, move, rmtree
import os

today_str = "20200110"
zip_name = "TESTZIP"

parent_folder = "/cul/cul0/ldpd/archivesspace/test/resources"  # test folder

# Zip up the JSON.
zip_out = make_archive(
    zip_name,
    "zip",
    root_dir=parent_folder,
    # root_dir="/Users/dwh2128/Documents/git/archivesspace-reports",
    base_dir=today_str
    # base_dir="output",
)

print(zip_out)

print(move(zip_out, parent_folder))

print(rmtree(parent_folder + "/" + today_str))

