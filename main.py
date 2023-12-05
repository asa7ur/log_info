import re
import operator
import csv

error = {}

error_format = r"ERROR (.*) (\(.*\))"
with open("syslog.log") as file:
    for line in file:
        error_match = re.search(error_format, line)
        if error_match:
            error_msg = error_match.group(1)
            error[error_msg] = error.get(error_msg, 0) + 1

sorted_errors = [("Error", "Count")] + sorted(error.items(), key=operator.itemgetter(1), reverse=True)

with open('error_message.csv', 'w', newline='') as error_file:
    writer = csv.writer(error_file)
    writer.writerows(sorted_errors)
