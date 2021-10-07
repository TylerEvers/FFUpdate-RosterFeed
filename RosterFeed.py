import pyodbc
import databaseconfig as cfg
import pandas as pd

#Players DataFrame 
dfPlayers = pd.read_csv("D:\Downloads\Rosters.csv")

#Open SQL connection
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+cfg.sql["server"]+';DATABASE='+cfg.sql["database"]+';UID='+cfg.sql["username"]+';PWD='+ cfg.sql["password"])
cursor = cnxn.cursor()

#Update contract/roster info in Players table
for player in dfPlayers.index:
    query = ("""UPDATE p SET p.Position = '%s', p.TeamID = t.ID, p.contractThrough = %d, p.capSpace = %d FROM Players p INNER JOIN Teams t ON t.Name = '%s' AND TeamType = 0 WHERE p.PlayerName = '%s';""" 
            % (dfPlayers['Position'][player], int(dfPlayers['ContractThrough'][player]), int(dfPlayers['ContractAmount'][player]), dfPlayers['TeamName'][player].replace("'","''"), dfPlayers['PlayerName'][player].replace("'","''")))
    cursor.execute(query)

cnxn.commit()




