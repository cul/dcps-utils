import ASFunctions as asf
import json
import os.path
import pickle


my_name = __file__

# This makes sure the script can be run from any working directory and still find related files.
my_path = os.path.dirname(__file__)

asf.setServer("Prod")  # AS instance: Prod | Dev | Test

the_info = [
    {"name": "families", "endpoint": "/agents/families",},
    {"name": "corporate", "endpoint": "/agents/corporate_entities",},
    {"name": "persons", "endpoint": "/agents/people",},
]

for i in the_info:
    print("Getting agents: " + i["name"])
    out_path = os.path.join(my_path, "output/agents_" + i["name"] + ".pickle")

    # Get a list of agent ids from API
    agents_list = json.loads(asf.getResponse(i["endpoint"] + "?all_ids=true"))

    print("Number of agents: " + str(len(agents_list)))

    cnt = 0

    agent_data = []

    # Loop through agent ids and get full record from API.
    for agent in agents_list:
        cnt += 1
        # print("COUNT: " + str(cnt))
        # print("Agent # " + str(agent))
        x = asf.getResponse(i["endpoint"] + "/" + str(agent))
        agent_data.append(json.loads(x))

    print("Saving to " + str(out_path) + "...")
    with open(out_path, "wb") as f:
        pickle.dump(agent_data, f)

    print(" ")

