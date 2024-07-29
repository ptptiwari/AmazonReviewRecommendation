import csv
import sqlite3
import uuid

from Recommendation_System.enc_dec_usingDict import uuid_to_email, store_email_uuid_mapping

input_file = 'user_email_prefs.csv'
output_file1 = 'out_useremail_prefs.csv'
output_file2 = 'out_useremail_prefs2.csv'

def create_email_uuid_mapping_table(db_file='email_uuid.db'):
    """Creates the email_uuid table in the database."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_uuid (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            uuid TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def email_to_uuid(email):
    """Converts an email address to a UUID.

    Args:
        email: The email address to encode.

    Returns:
        The UUID representation of the email address.
    """
    uuid_value = str(uuid.uuid3(uuid.NAMESPACE_DNS, email))
    print(f"Email: {email}, UUID: {uuid_value}")  # For debugging
    return uuid_value

def encode(input_file, output_file, db_file='email_uuid.db'):
    """Processes a CSV file, converts emails to UUIDs, and writes results to another CSV.

    Args:
        input_file: The input CSV file containing email addresses, product IDs, and rate IDs.
        output_file: The output CSV file to store UUIDs, product IDs, and rate IDs.
        db_file: The database file to store email-UUID mappings.
    """
    create_email_uuid_mapping_table(db_file)

    with open(input_file, 'r', newline='') as csv_in, open(output_file, 'w', newline='') as csv_out:
        csv_reader = csv.reader(csv_in)
        csv_writer = csv.writer(csv_out)
        csv_writer.writerow(['uuid', 'prod_id', 'rate_id'])  # Write header row

        for row in csv_reader:
            email, prod_id, rate_id = row
            uuid_value = email_to_uuid(email)
            store_email_uuid_mapping(email)
            csv_writer.writerow([uuid_value, prod_id, rate_id])

def decode(input_file, output_file, db_file='email_uuid.db'):
    """Processes a CSV file, converts UUIDs to emails, and writes results to another CSV.

    Args:
        input_file: The input CSV file containing UUIDs, product IDs, and rate IDs.
        output_file: The output CSV file to store emails, product IDs, and rate IDs.
        db_file: The database file to store email-UUID mappings.
    """
    with open(input_file, 'r', newline='') as csv_in, open(output_file, 'w', newline='') as csv_out:
        csv_reader = csv.reader(csv_in)
        csv_writer = csv.writer(csv_out)
        csv_writer.writerow(['email', 'prod_id', 'rate_id'])  # Write header row

        for row in csv_reader:
            uuid_value, prod_id, rate_id = row
            email = uuid_to_email(uuid_value)
            print(f"UUID: {uuid_value}, Email: {email}")  # For debugging
            csv_writer.writerow([email, prod_id, rate_id])

# ... rest of the code

create_email_uuid_mapping_table()
encode(input_file, output_file1)
decode(output_file1, output_file2)
