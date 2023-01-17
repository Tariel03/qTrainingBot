import pymysql
from connector import host,dbName,Port,Pass,User
try:
    connection = pymysql.connect(
        host = host,
        port = Port,
        user = User,
        password = Pass,
        database=dbName,
        cursorclass=pymysql.cursors.DictCursor

    )
    print("success!")
    def insert(idUser,firstName,lastName,isBot):
        try:
            with connection.cursor() as cursor:

                insert_command = f"INSERT INTO `tariel`.`tar` (`id_user`, `first_name`, `last_name`,`is_bot`) VALUES " \
                                 f"(%s, %s, %s, %s); "
                cursor.execute(insert_command,(idUser,firstName,lastName,isBot))
                connection.commit()

        except Exception as ex:
            print(ex)
        finally:
            connection.close()
    def select(idUSer):
        try:
            with connection.cursor() as cursor:
                select = "SELECT `first_name`,`last_name` FROM `tar` WHERE `id_user`= %s"
                cursor.execute(select,(idUSer))
                rows = cursor.fetchall()
                return rows

        except Exception as e:
            print(e)

except Exception as ex:
    print(ex)