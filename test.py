import pymysql


if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password="Joker0422!", db="project")
    cursor = conn.cursor()

    sql = "select no, team, odds, amount, result from betting_data"
    cursor.execute(sql)
    conn.commit()

    datas = cursor.fetchall()

    for no, team, odds, amount, result in datas:
        if result is None:
            sql = "select result, odds from match_list where team=" + "'" + team + "'"
            cursor.execute(sql)
            conn.commit()

            datas_1 = cursor.fetchall()
            for result in datas_1:
                if result:
                    sql = "select total_plus from betting_data where no=" + "'" + str(int(no)-1) + "'"
                    cursor.execute(sql)
                    conn.commit()
                    datas_2 = cursor.fetchall()

                    for total_plus in datas_2:
                        total_plus = str(total_plus).replace("(", "").replace(",", "").replace(")", "")

                        sql = "update betting_data set result=True, plus=" + "'" + str(amount*odds-amount) + "'" +\
                              ",total_plus=" + "'" + str(int(total_plus)+amount*odds-amount) + "'" + "where team=" + "'" + str(team) + "'"
                        cursor.execute(sql)
                        conn.commit()


