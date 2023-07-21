import acc_mmap as acct
import json
import time
from utils import param_to_message


def create_telemetry_file(line_nb):
    path = "telemetry/telemetry_acct.json"

    with open(path, "w") as file:
        for i in range(line_nb):
            physics = acct.read_physics_to_dict()

            if physics["speedKmh"] == 0:
                continue
            json.dump({"index": {"_index": "telemetrie", "_id": str(i+1)}}, file)
            file.write('\n')
            json.dump(physics, file)
            file.write('\n')
