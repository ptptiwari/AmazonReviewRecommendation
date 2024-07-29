import sqlite3
import uuid


def email_to_uuid(email):
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, email))

def create_email_uuid_mapping(db_file='email_uuid.db'):
    """Creates a SQLite database to store email-UUID mappings."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE email_uuid (
                      id INT PRIMARY KEY AUTOINCREMENT,
                      email VARCHAR(255) UNIQUE,
                      uuid VARCHAR(255) UNIQUE);""")
    conn.commit()
    conn.close()


def store_email_uuid_mapping(email, uuid_str, db_file='email_uuid.db'):
    """Stores an email-UUID pair in the database."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO email_uuid (email, uuid) VALUES (?, ?)', (email, uuid_str))
    conn.commit()
    conn.close()


def uuid_to_email(uuid_str, db_file='email_uuid.db'):
    """Retrieves the email associated with a UUID from the database."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM email_uuid WHERE uuid = ?', (uuid_str))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

create_email_uuid_mapping

# Example usage
email = "pankajt@vmware.com"
uuid_value = email_to_uuid(email)
print(uuid_value)

store_email_uuid_mapping(email, uuid_value)

# Recovering the email would involve a database lookup using the UUID
recovered_email = uuid_to_email(uuid_value)
#print(recovered_email)  # This would ideally return "pankajt@vmware.com"