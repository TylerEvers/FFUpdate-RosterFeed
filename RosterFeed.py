import pyodbc
import databaseconfig as cfg

#Inst. Variables/Classes
lstPlayers = []

#Players Class
class Players:
    def __init__(self, Name, Position, ContractThrough, ContractAmount, Team):
        self.Name = Name.replace("'","''")
        self.Position = Position
        self.ContractThrough = ContractThrough
        self.ContractAmount = ContractAmount
        self.Team = Team.replace("'","''")

#Load Rosters.csv File into lstPlayers
f = open("D:\Downloads\Rosters.csv", "r")
i = 0
for x in f:
    if i > 0:
        lstRecord = x.split(",")
        print(lstRecord[0])
        lstPlayers.append( Players(lstRecord[0],lstRecord[1],lstRecord[2],lstRecord[3],lstRecord[4].rstrip() ))
    i += 1

#Open SQL connection
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+cfg.sql["server"]+';DATABASE='+cfg.sql["database"]+';UID='+cfg.sql["username"]+';PWD='+ cfg.sql["password"])
cursor = cnxn.cursor()

#Update contract/roster info in Players table
for player in lstPlayers:
    query = ("""UPDATE p SET p.Position = '%s', p.TeamID = t.ID, p.contractThrough = %d, p.capSpace = %d FROM Players p INNER JOIN Teams t ON t.Name = '%s' AND TeamType = 0 WHERE p.PlayerName = '%s';""" 
            % (player.Position, int(player.ContractThrough), int(player.ContractAmount), player.Team, player.Name))
    cursor.execute(query)

cnxn.commit()




