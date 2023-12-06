import re
import csv

error = {}
per_user = {}

error_format = r"ERROR (.*) \((.*)\)"
info_format = r"INFO (.*) \((.*)\)"

with open("syslog.log") as file:
    for line in file:
        error_match = re.search(error_format, line)
        info_match = re.search(info_format, line)

        if error_match:
            error_msg = error_match.group(1)
            if error_msg not in error:
                error[error_msg] = 0
            error[error_msg] += 1

            username = error_match.group(2)
            if username not in per_user:
                per_user[username] = {'INFO': 0, 'ERROR': 0}
            per_user[username]['ERROR'] += 1

        if info_match:
            username = info_match.group(2)
            if username not in per_user:
                per_user[username] = {'INFO': 0, 'ERROR': 0}
            per_user[username]['INFO'] += 1

sorted_errors = [("Error", "Count")] + sorted(error.items(), key=lambda x: x[1], reverse=True)

sorted_users = [("Username", "INFO", "ERROR")] + sorted(
    ((username, amounts['INFO'], amounts['ERROR']) for username, amounts in per_user.items()),
    key=lambda x: x[0])

with open('error_message.csv', 'w', newline='') as error_file:
    writer = csv.writer(error_file)
    writer.writerows(sorted_errors)

with open('user_statistics.csv', 'w', newline='') as per_user_file:
    writer = csv.writer(per_user_file)
    writer.writerows(sorted_users)
