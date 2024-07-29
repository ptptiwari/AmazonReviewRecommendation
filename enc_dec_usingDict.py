import csv

import pandas as pd
import uuid

def email_to_uuid(email):
    """Converts an email address to a UUID.

  Args:
    email: The email address to encode.

  Returns:
    The UUID representation of the email address.
  """
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, email))

def process_csv(input_file, output_file):
    """Processes a CSV file, converts emails to UUIDs, and writes results to another CSV.

  Args:
    input_file: The input CSV file containing email addresses.
    output_file: The output CSV file to store email-UUID pairs.
  """
    with open(input_file, 'r', newline='') as csv_in, open(output_file, 'w', newline='') as csv_out:
        csv_reader = csv.reader(csv_in)
        csv_writer = csv.writer(csv_out)
        #csv_writer.writerow(['email', 'uuid'])  # Write header row
        for row in csv_reader:
            email = row[0]
            prod_id = row[1]
            rate_id = row[2]
            uuid_value = email_to_uuid(email)
            csv_writer.writerow([ uuid_value,prod_id,rate_id ])


# Example usage
input_file = '../classwork/user_email_prefs.csv'
output_file = '../classwork/out_useremail_prefs.csv'
process_csv(input_file, output_file)





email_uuid_map = {}


def store_email_uuid_mapping(email):
    """Stores an email-UUID pair in the dictionary."""
    uuid_value = email_to_uuid(email)
    email_uuid_map[email] = uuid_value


def uuid_to_email(uuid_str):
    """Retrieves the email associated with a UUID from the dictionary."""
    for email, uuid_value in email_uuid_map.items():
        if uuid_value == uuid_str:
            return email
    return None


# Example usage
email = "prasanna@vmware.com"
store_email_uuid_mapping(email)
uuid_value = email_uuid_map[email]
print(uuid_value)

recovered_email = uuid_to_email(uuid_value)
print(recovered_email)
