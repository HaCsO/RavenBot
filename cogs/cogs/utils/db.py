from mysql.connector import (connection)

class Connect():
	def conn():
		try:
			mydb = connection.MySQLConnection(
				host="fojvtycq53b2f2kx.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
				user="bvfa84n7qrsb0apv",
				passwd="wekmno5kvjnjz11a",
				database="e0nglnsygl2hevxn"
				)

			return mydb
		except Exception as e:
			print("[ERR]Connection failed")
			print(f"[ERR]Error = {e}")