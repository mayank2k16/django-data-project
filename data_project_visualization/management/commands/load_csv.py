from django.core.management.base import BaseCommand
import pymysql

class Command(BaseCommand):
    help = 'Loads the csv file into mysql database'

    def handle(self, *args, **kwargs):
        mydb = pymysql.connect(
        host="localhost",
        user="dell",
        passwd="mayank",
        database="django_orm_db",
        autocommit=True,
        local_infile=1
        )
        mycursor = mydb.cursor()
        
        query_to_transfer_matches_to_mysql = "LOAD DATA LOCAL INFILE '/var/lib/mysql-files/matches.csv' INTO TABLE django_orm_db.data_project_visualization_matches FIELDS TERMINATED BY ','  IGNORE 1 LINES;"
        mycursor.execute(query_to_transfer_matches_to_mysql)

        query_to_transfer_deliveries_to_mysql = "LOAD DATA LOCAL INFILE '/var/lib/mysql-files/deliveries.csv' INTO TABLE django_orm_db.data_project_visualization_deliveries FIELDS TERMINATED BY ','  IGNORE 1 LINES(match_id,inning,batting_team,bowling_team,over,ball,batsman,non_striker,bowler,is_super_over,wide_runs,bye_runs,legbye_runs,noball_runs,penalty_runs,batsman_runs,extra_runs,total_runs,player_dismissed,dismissal_kind,fielder);"
        mycursor.execute(query_to_transfer_deliveries_to_mysql)

        mycursor.close()
        mydb.close()