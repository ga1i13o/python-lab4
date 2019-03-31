import pymysql


def main():
    fp = open("task_list.txt")
    v = fp.readlines()
    fp.close()
    for i in range(0, len(v)):
        v[i] = v[i].strip()

    sql = "insert into task(todo) values(%s);"
    connection = pymysql.connect(user="utente", password="piru",
                                 host="localhost", database="tasklist")
    cursor = connection.cursor()
    for x in v:
        cursor.execute(sql, (x,))

    connection.commit()

    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()