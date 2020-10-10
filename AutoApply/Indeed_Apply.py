import sqlite3
from scripts.web import display_textbox_question, display_radiobuttons_question, display_select_question, \
    construct_container, get_question_types, get_question_type_funcs

connection_to_db = sqlite3.connect("questions__answers_db.db")

cursor = connection_to_db.cursor()

initial_load_query = """SELECT * FROM data WHERE answer IS NULL;"""

data_tupperware = construct_container()

def print_welcome():
    print(
        '####################################################################\n',
        "\r# Hi! This is where you will answer questions scrapped from py_indeed.py.\n",
        "\r# Close the pop-up window or click 'Cancel' when finished or want to quit.\n",
        "\r# Author: Conner Crosby\n",
        '\r####################################################################')

    input("# Press Enter To Begin...\n")

def can_query(query):
    try:
        cursor.execute(query)
        return True
    except sqlite3.OperationalError:
        return False

def display_question(question, procedure, question_choices):
    return procedure(question, question_choices)

def write_to_database(question, what_to_write):
    parameters = {"input": what_to_write, "question": question}
    cursor.execute("""UPDATE data SET answer=:input WHERE question=:question""", parameters)
    connection_to_db.commit()

def load_into(db_row):
    return db_row[0], db_row[2], db_row[3]

def quit(answer):
    if (answer != None and answer != 'Cancel'):
        return False
    else:
        return True

def main():
    known_types = get_question_types(data_tupperware)
    print_welcome()
    if (not can_query(initial_load_query)):
        print("Error! If database (db) file does not exist, then run py_indeed first...")
        print("Click Enter to quit...")
    else:
        db_rows = cursor.fetchall()
        for db_row in db_rows:
            question, question_type, question_choices = load_into(db_row)
            funcs = get_question_type_funcs(data_tupperware, question_type)
            answer = display_question(question, funcs["print_question"], question_choices)
            if(quit(answer)):
                break
            else:
                write_to_database(question, answer)

main()
connection_to_db.close()