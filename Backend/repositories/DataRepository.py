from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def add_history(deviceid, userid, value):
        sql = "INSERT INTO History (HistoryValue, DeviceID, UserID) VALUES (%s, %s, %s);"
        params = [value, deviceid, userid]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_logging_per_device(deviceid):
        sql = "SELECT HistoryValue, DATE_FORMAT(HistoryDate, '%H:%i') as DateTime FROM History WHERE DeviceID = %s ORDER BY HistoryID DESC limit 10;"
        params = [deviceid]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_logging_per_user(deviceid, userid):
        sql = "SELECT HistoryValue, DATE_FORMAT(HistoryDate, '%H:%i %d/%m') as DateTime FROM History WHERE DeviceID = %s and UserID = %s ORDER BY HistoryID limit 10;"
        params = [deviceid, userid]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_logging():
        sql = "SELECT DeviceID, HistoryValue, DATE_FORMAT(HistoryDate, '%H:%i') as DateTime FROM History ORDER BY HistoryID DESC limit 10;"
        return Database.get_rows(sql)

    @staticmethod
    def read_total_water_consumption(userid):
        sql = "SELECT round(Sum(HistoryValue),0) as Total FROM History WHERE DeviceID = 4 and UserID = %s"
        params = [userid]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_average_water_consumption(userid):
        sql = "SELECT round((round(Sum(HistoryValue),0))/(count(distinct(DATE(HistoryDate)))),2) as Average FROM History WHERE DeviceID = 4 and UserID = %s"
        params = [userid]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_total_consumption_per_user(userid):
        sql = "SELECT ROUND(SUM(HistoryValue),0) as Value FROM History WHERE DATE(HistoryDate) = current_date() and DeviceID = 4 and UserID = %s;"
        params = [userid]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_consumption_logs(userid):
        sql = "SELECT ROUND(HistoryValue) as Value, DATE_FORMAT(HistoryDate, '%H:%i') as HistoryDate FROM History WHERE DATE(HistoryDate) = current_date() and DeviceID = 4 and UserID = %s ORDER BY HistoryDate DESC;"
        params = [userid]
        return Database.get_rows(sql, params)
    
    @staticmethod
    def add_user(nickname, firstname, lastname, password, rfid, containerid):
        sql = "INSERT INTO User (Nickname, Firstname, LastName, Password, RFID, ContainerID) VALUES (%s,%s,%s,%s,%s,%s);"
        params = [nickname, firstname, lastname, password, rfid, containerid]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_userid():
        sql = "SELECT UserID from User"
        return Database.get_one_row(sql)

    @staticmethod
    def get_userid_by_rfid(rfid):
        sql = "SELECT Nickname, UserID FROM User WHERE RFID = %s"
        params = [rfid]
        return Database.get_one_row(sql, params)

    @staticmethod
    def add_goal(goal, userid):
        sql = "INSERT INTO Settings (DailyGoal, UserID) VALUES (%s, %s)"
        params = [goal, userid]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_goal(userid):
        sql = "SELECT DailyGoal FROM Settings WHERE UserID = %s ORDER BY SettingsID DESC limit 1"
        params = [userid]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_all_goals(userid):
        sql = "SELECT DailyGoal, DATE_FORMAT(Datetime, '%d/%m') as Datetime FROM Settings WHERE UserID = %s ORDER BY SettingsID DESC limit 10"
        params = [userid]
        return Database.get_rows(sql, params)