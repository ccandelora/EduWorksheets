import os
import psycopg2

try:
    conn = psycopg2.connect(
        dbname=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        host=os.environ['PGHOST'],
        port=os.environ['PGPORT']
    )
    print("Successfully connected to the database.")
    
    # Check if the 'lti_user_id' column exists in the 'user' table
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='user' AND column_name='lti_user_id';")
    result = cur.fetchone()
    
    if result:
        print("The 'lti_user_id' column exists in the 'user' table.")
    else:
        print("The 'lti_user_id' column does not exist in the 'user' table.")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error connecting to the database: {str(e)}")
