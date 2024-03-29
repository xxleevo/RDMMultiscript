#!/usr/bin/env python

#Requires Python MySQL Connector
#To install "pip install mysql-connector-python"
import datetime
import time
import os
import mysql.connector
from mysql.connector import Error
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
#import ConfigParser
import json
CONFIG_FILE = "config.ini"
config = ConfigParser()
#Get Database Config settings
#config.read(CONFIG_FILE)
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), CONFIG_FILE))

Host = config.get('DB','Host')
Name = config.get('DB','Name')
User = config.get('DB','User')
Pwd = config.get('DB','Password')
Port = config.get('DB','Port')

#Clean Config Settings
CleanPokemon = config.getboolean('Pokemon','CleanPokemon')
CleanPokemonHours = json.loads(config.get('Pokemon','CleanPokemonHours'))
CleanPokemonMinutes = json.loads(config.get('Pokemon','CleanPokemonMinutes'))
CleanPokemonLogging = config.getboolean('Pokemon','CleanPokemonLogging')

#Clean Truncate Config Settings
TruncatePokemon = config.getboolean('Pokemon','TruncatePokemon')
TruncatePokemonHours = json.loads(config.get('Pokemon','TruncatePokemonHours'))
TruncatePokemonMinutes = json.loads(config.get('Pokemon','TruncatePokemonMinutes'))
TruncatePokemonLogging = config.getboolean('Pokemon','TruncatePokemonLogging')

#Pokestop Config Settings
ConvertPokestops = config.getboolean('Pokestop','ConvertStops')
ConvertStopsHours = json.loads(config.get('Pokestop','ConvertStopsHours'))
ConvertStopsMinutes = json.loads(config.get('Pokestop','ConvertStopsMinutes'))
ConvertPokestopsLogging = config.getboolean('Pokestop','ConvertStopsLogging')

#Account Cooldown-Reset Settings
ResetCooldownAccounts = config.getboolean('Account Cooldown','ResetCooldownAccounts')
ResetCooldownAccountsHours = json.loads(config.get('Account Cooldown','ResetCooldownAccountsHours'))
ResetCooldownAccountsMinutes = json.loads(config.get('Account Cooldown','ResetCooldownAccountsMinutes'))
ResetCooldownAccountsLevelrange = json.loads(config.get('Account Cooldown','ResetCooldownAccountsLevelrange'))
ResetCooldownAccountsByCooldownedTime = config.getboolean('Account Cooldown','ResetCooldownAccountsByCooldownedTime')
ResetCooldownAccountsMinimumCooldowned = config.getint('Account Cooldown','ResetCooldownAccountsMinimumCooldowned')
ResetCooldownAccountsLogging = config.getboolean('Account Cooldown','ResetCooldownAccountsLogging')

#Spin Reset Settings
SpinReset = config.getboolean('Spin Reset','ResetSpins')
SpinResetHours = json.loads(config.get('Spin Reset','ResetSpinsHours'))
SpinResetMinutes = json.loads(config.get('Spin Reset','ResetSpinsMinutes'))
SpinResetLevelrange = json.loads(config.get('Spin Reset','ResetSpinsLevelrange'))
SpinResetLogging = config.getboolean('Spin Reset','ResetSpinsLogging')

#Warning Settings
WarningReset = config.getboolean('Warning Reset','ResetWarnings')
WarningsResetHours = json.loads(config.get('Warning Reset','ResetWarningsHours'))
WarningsResetMinutes = json.loads(config.get('Warning Reset','ResetWarningsMinutes'))
WarningsResetLevelrange = json.loads(config.get('Warning Reset','ResetWarningsLevelrange'))

WarningsResetOnlyWarnings = config.getboolean('Warning Reset','ResetWarningsOnly')
WarningsResetOnlyWarningsByPassedDays = config.getboolean('Warning Reset','ResetWarningsOnlyByPassedDays')
WarningsResetOnlyWarningsPassedDays = config.getint('Warning Reset','ResetWarningsOnlyByPassedDaysAmount')
WarningsResetLogging = config.getboolean('Warning Reset','ResetWarningsLogging')

#Logging
logFile = config.get('Logging','Logfile')
logActionsOnly = config.getboolean('Logging','LogActionsOnly')
verboseLogging = config.getboolean('Logging','Verbose')
debugLogging = config.getboolean('Logging','Debug')

def log(msg):
  # open the specified log file
  file = open(logFile,"a")
  # write log message with timestamp to log file
  file.write("%s: %s\n" % (time.strftime("%d.%m.%Y %H:%M:%S"), msg))
  # close log file
  file.close

#start the script
try:	
	conn = None
	now = datetime.datetime.now()
	
	#Pokemon Logging
	if debugLogging:
		print('')
		print('[DEBUG] Clean Pokemon: {}'.format(CleanPokemon))
	if verboseLogging:
		print('[VERBOSE] Clean Pokemon at the following hours: {}'.format(CleanPokemonHours))
		print('[VERBOSE] Clean Pokemon at the following minutes: {}'.format(CleanPokemonMinutes))
		print('')
		
	#Pokemon Logging
	if debugLogging:
		print('')
		print('[DEBUG] Truncate Pokemon: {}'.format(TruncatePokemon))
	if verboseLogging:
		print('[VERBOSE] Truncate Pokemon at the following hours: {}'.format(TruncatePokemonHours))
		print('[VERBOSE] Truncate Pokemon at the following minutes: {}'.format(TruncatePokemonMinutes))
		print('')
		
	#Pokestop Logging
	if debugLogging:
		print('[DEBUG] Convert Pokestops: {}'.format(ConvertPokestops))
	if verboseLogging:
		print('[VERBOSE] Convert Stops at the following hours: {}'.format(ConvertStopsHours))
		print('[VERBOSE] Convert Stops at the following minutes: {}'.format(ConvertStopsMinutes))
		print('')
		
	#Cooldown Logging
	if debugLogging:
		print('[DEBUG] Reset Cooldowns: {}'.format(ResetCooldownAccounts))
	if verboseLogging:
		print('[VERBOSE] Reset Cooldown at the following hours: {}'.format(ResetCooldownAccountsHours))
		print('[VERBOSE] Reset Cooldown at the following minutes: {}'.format(ResetCooldownAccountsMinutes))
		print('[VERBOSE] Reset Cooldown for the following levels: {}'.format(ResetCooldownAccountsLevelrange))
		print('')
		
	#Spin Reset
	if debugLogging:
		print('[DEBUG] Reset Spins: {}'.format(SpinReset))
	if verboseLogging:
		print('[VERBOSE] Reset Spins at the following hours: {}'.format(SpinResetHours))
		print('[VERBOSE] Reset Spins at the following minutes: {}'.format(SpinResetMinutes))
		print('[VERBOSE] Reset Spins for the following levels: {}'.format(SpinResetLevelrange))
		print('')
		
	#Spin Reset
	if debugLogging:
		print('[DEBUG] Reset Warnings: {}'.format(WarningReset))
	if verboseLogging:
		print('[VERBOSE] Reset Warnings at the following hours: {}'.format(WarningsResetHours))
		print('[VERBOSE] Reset Warnings at the following minutes: {}'.format(WarningsResetMinutes))
		print('[VERBOSE] Reset Warnings for the following levels: {}'.format(WarningsResetLevelrange))
		print('')
	
	#Declare every script execute set to false
	executeCleanPokemon = False
	executeTruncatePokemon = False
	executeConvert = False
	executeCooldown = False
	executeSpinReset = False
	executeWarningReset = False

	#Handling Pokemon Cleaning to execute
	if CleanPokemon:
		for i in CleanPokemonHours:
			if i == now.hour:
				for j in CleanPokemonMinutes:
					if j == now.minute:
						executeCleanPokemon = True
	#Handling Pokemon Cleaning to execute
	if TruncatePokemon:
		for i in TruncatePokemonHours:
			if i == now.hour:
				for j in TruncatePokemonMinutes:
					if j == now.minute:
						executeTruncatePokemon = True
	#Handling Cooldown Reset to execute
	if ResetCooldownAccounts:
		for i in ResetCooldownAccountsHours:
			if i == now.hour:
				for j in ResetCooldownAccountsMinutes:
					if j == now.minute:
						executeCooldown = True
	#Handling Pokestop Convertion to execute
	if ConvertPokestops:
		for i in ConvertStopsHours:
			if i == now.hour:
				for j in ConvertStopsMinutes:
					if j == now.minute:
						executeConvert = True
	#Handling Spin Reset to execute
	if SpinReset:
		for i in SpinResetHours:
			if i == now.hour:
				for j in SpinResetMinutes:
					if j == now.minute:
						executeSpinReset = True
						
	#Handling Spin Reset to execute
	if WarningReset:
		for i in WarningsResetHours:
			if i == now.hour:
				for j in WarningsResetMinutes:
					if j == now.minute:
						executeWarningReset = True

	#When Config says to execute something, do that
	if ConvertPokestops or ResetCooldownAccounts or CleanPokemon or TruncatePokemon or SpinReset or WarningReset:
		conn = mysql.connector.connect(host=Host,
                             database=Name,
                             user=User,
                             password=Pwd,
                             port=Port)

		#Execute Cooldown Script
		if executeCooldown:
			print('')
			print('[Cooldown] Executing cooldown script...')
			resetMinlevel = str(ResetCooldownAccountsLevelrange[0])
			resetMaxlevel = str(ResetCooldownAccountsLevelrange[1])
			if debugLogging:
				print ('[Cooldown][DEBUG] Executing with levelrange: {min} to {max}'.format(min=resetMinlevel,max=resetMaxlevel))
				print ('[DEBUG] Only Reset Cooldowns by time: {}'.format(ResetCooldownAccountsByCooldownedTime))
				if ResetCooldownAccountsByCooldownedTime:
					print ('[DEBUG] Min Cooldown-Time: {}'.format(ResetCooldownAccountsMinimumCooldowned))
			if ResetCooldownAccountsByCooldownedTime:
				input = (resetMinlevel, resetMaxlevel, ResetCooldownAccountsMinimumCooldowned)
				sql = """SELECT username FROM account WHERE last_encounter_time IS NOT NULL AND level >=%s AND level <= %s  AND last_encounter_time <= UNIX_TIMESTAMP(NOW() - INTERVAL %s MINUTE)"""
			else:
				input = (resetMinlevel, resetMaxlevel)
				sql = """SELECT username FROM account WHERE last_encounter_time IS NOT NULL AND level >=%s AND level <= %s"""
			cursor = conn.cursor()
			cursor.execute(sql, input)
			
			cooldownedAccounts = cursor.fetchall()
			if cooldownedAccounts == []:
				if ResetCooldownAccountsLogging:
					if not logActionsOnly:
						log("[Cooldown] Script executed - no accounts on cooldown({})".format(len(cooldownedAccounts)))
				print("[Cooldown] Cooldown script was executed, but no account in cooldown was found for levelrange: {min}-{max}".format(min=resetMinlevel,max=resetMaxlevel))
				cursor.close
			else:
				if ResetCooldownAccountsByCooldownedTime:
					sql_update = """UPDATE account set last_encounter_time=NULL, last_encounter_lat=NULL, last_encounter_lon=NULL WHERE level >=%s AND level <= %s AND last_encounter_time <= UNIX_TIMESTAMP(NOW() - INTERVAL %s MINUTE)"""
				else:
					sql_update = """UPDATE account set last_encounter_time=NULL, last_encounter_lat=NULL, last_encounter_lon=NULL WHERE level >=%s AND level <= %s"""
				if debugLogging:
					print ('[DEBUG] SQL Query for Cooldown Accs: {}'.format(ResetCooldownAccountsMinimumCooldowned))
				cursor = conn.cursor()
				cursor.execute(sql_update, input)
				conn.commit()
				if ResetCooldownAccountsLogging:
					log("[Cooldown] {} Account(s) have been taken out of cooldown".format(cursor.rowcount))
				print(" ")
				print("[Cooldown] {} Account(s) have been taken out of cooldown".format(cursor.rowcount))
			
		#Execute Convertion Script
		if executeConvert:
			print('')
			print('[Conversion] Executing stop convertion script...')
			cursor = conn.cursor()
			sql = """SELECT gym.id FROM gym INNER JOIN pokestop ON pokestop.id = gym.id"""
			cursor.execute(sql)
			convertedGyms = cursor.fetchall()
			if debugLogging:
				print('[Conversion][DEBUG] Convertable Gyms: {}'.format(cursor.rowcount))
			if convertedGyms == []:
				if ConvertPokestopsLogging:
					if not logActionsOnly:
						log("[Conversion] Script executed - no stop was changed to a gym({})".format(len(convertedGyms)))
				print("[Conversion] Convertion script was executed, but no stop was changed to a gym")
				cursor.close
			else:
				sql_update = """UPDATE gym INNER JOIN pokestop ON pokestop.id = gym.id SET gym.name = pokestop.name, gym.url = pokestop.url WHERE pokestop.name IS NOT NULL"""
				sql_delete = """DELETE FROM pokestop USING pokestop INNER JOIN gym WHERE pokestop.id = gym.id"""
				cursor = conn.cursor()
				cursor.execute(sql_update)
				conn.commit()
				updated = cursor.rowcount
				cursor.execute(sql_delete)
				conn.commit()
				if ConvertPokestopsLogging:
					log("[Cooldown] {updated} stopname(s) converted to gym and {deleted} stop(s) got deleted".format(updated=updated,deleted=cursor.rowcount))
				print("[Conversion] {updated} stopname(s) converted to gym and {deleted} stop(s) got deleted".format(updated=updated,deleted=cursor.rowcount))

		#Execute Spin Reset Script
		if executeSpinReset:
			print('')
			print('[SpinReset] Executing spin-reset script...')
			resetMinlevel = str(SpinResetLevelrange[0])
			resetMaxlevel = str(SpinResetLevelrange[1])
			if debugLogging:
				print ('[SpinReset][DEBUG] Executing with levelrange: {min} to {max}'.format(min=resetMinlevel,max=resetMaxlevel))
			input = (resetMinlevel, resetMaxlevel)
			cursor = conn.cursor()
			sql = """SELECT username FROM account WHERE spins > 1 AND level >=%s AND level <= %s"""
			cursor.execute(sql, input)
			cooldownedAccounts = cursor.fetchall()
			if cooldownedAccounts == []:
				if SpinResetLogging:
					if not logActionsOnly:
						log("[SpinReset] Script executed - no accounts on cooldown({})".format(len(cooldownedAccounts)))
				print("[SpinReset] SpinReset script was executed, but no account with spins was found for levelrange: {min}-{max}".format(min=resetMinlevel,max=resetMaxlevel))
				cursor.close
			else:
				sql_update = """UPDATE account set spins=0 WHERE level >=%s AND level <= %s"""
				cursor = conn.cursor()
				cursor.execute(sql_update, input)
				conn.commit()
				if SpinResetLogging:
					log("[SpinReset] {} Account(s) were changed to 0 spins".format(cursor.rowcount))
				print(" ")
				print("[SpinReset] {} Account(s) were changed to 0 spins".format(cursor.rowcount))
				
		if executeWarningReset:
			print('')
			print('[WarningReset] Executing warning-reset script...')
			resetMinlevel = str(WarningsResetLevelrange[0])
			resetMaxlevel = str(WarningsResetLevelrange[1])
			if debugLogging:
				print ('[WarningReset][DEBUG] Executing with levelrange: {min} to {max}'.format(min=resetMinlevel,max=resetMaxlevel))
				if WarningsResetOnlyWarningsByPassedDays:
					print ('[WarningReset][DEBUG] Only resetting Accounts with warnings older than day: {}'.format(WarningsResetOnlyWarningsPassedDays))
				elif WarningsResetOnlyWarnings:
					print ('[WarningReset][DEBUG] Only Hard Reset Warnings Mode')
			if WarningsResetOnlyWarningsByPassedDays:
				input = (WarningsResetOnlyWarningsPassedDays, resetMinlevel, resetMaxlevel)
				sql = """SELECT username FROM account WHERE (first_warning_timestamp < UNIX_TIMESTAMP(NOW() - INTERVAL %s DAY)) AND level >=%s AND level <= %s"""
			elif WarningsResetOnlyWarnings:
				input = (resetMinlevel, resetMaxlevel)
				sql = """SELECT username FROM account WHERE (first_warning_timestamp IS NOT NULL) AND level >=%s AND level <= %s"""
			else:
				input = (resetMinlevel, resetMaxlevel)
				sql = """SELECT username FROM account WHERE (first_warning_timestamp IS NOT NULL OR failed IS NULL OR failed_timestamp IS NOT NULL) AND level >=%s AND level <= %s"""
			cursor = conn.cursor()
			cursor.execute(sql, input)
			cooldownedAccounts = cursor.fetchall()
			if cooldownedAccounts == []:
				if WarningsResetLogging:
					if not logActionsOnly:
						log("[WarningReset] Script executed - no accounts with warnings (or failed)({})".format(len(cooldownedAccounts)))
				print("[WarningReset] WarningReset script was executed, but no account with warnings was found for levelrange: {min}-{max}".format(min=resetMinlevel,max=resetMaxlevel))
				cursor.close
			else:
				if WarningsResetOnlyWarningsByPassedDays:
					sql_update = """UPDATE account set first_warning_timestamp=null WHERE first_warning_timestamp < UNIX_TIMESTAMP(NOW() - INTERVAL %s DAY) AND level >=%s AND level <= %s"""
				elif WarningsResetOnlyWarnings:
					sql_update = """UPDATE account set first_warning_timestamp=null WHERE level >=%s AND level <= %s"""
				else:
					sql_update = """UPDATE account set first_warning_timestamp=null, failed = null, failed_timestamp = null WHERE level >=%s AND level <= %s"""
				cursor = conn.cursor()
				cursor.execute(sql_update, input)
				conn.commit()
				if WarningsResetLogging:
					log("[WarningReset] {} Account(s) cleared warnings/(failed)".format(cursor.rowcount))
				print(" ")
				print("[WarningReset] {} Account(s) cleared warnings/(failed)".format(cursor.rowcount))

		#Execute CleanPokemon Script
		if executeCleanPokemon:
			cleanedCount = 0
			chunks = 1
			print('')
			print('[PokemonClean] Executing pokemon cleanup script...')
			cursor = conn.cursor()
			tstamp = time.time()
			if debugLogging:
				print('[Pokemon][DEBUG] timestamp used to delete Pokemon in chunks: {}'.format(tstamp))
			sql = """DELETE from pokemon WHERE expire_timestamp <=%s LIMIT 1000"""
			cursor.execute(sql, (time.time(),) )
			cleanedCount = cleanedCount + cursor.rowcount
			conn.commit()
			#Clean chunks in size of 1k Pokemon
			while cursor.rowcount > 999:
				cursor.execute(sql, (time.time(),) )
				cleanedCount = cleanedCount + cursor.rowcount
				chunks = chunks + 1
				if chunks % 5 == 0:
					if debugLogging:
						print('[Pokemon][DEBUG] 5 Chunks(1000) cleared. Total cleared now: {}'.format(chunks))
				conn.commit()
			if debugLogging:
				print('[Pokemon][DEBUG] Done. Chunks(1000) cleared: {}'.format(chunks))
			if cleanedCount <= 0:
				if CleanPokemonLogging:
					if not logActionsOnly:
						log("[PokemonClean] Script executed - Pokemon table already clean({})".format(cleanedCount))
				print("[PokemonClean] Pokemon table is already clean")
			else:
				if CleanPokemonLogging:
					log("[PokemonClean] {} Pokemon were cleaned from the database".format(cleanedCount))
				print("[PokemonClean] {} Pokemon were cleaned from the database".format(cleanedCount))
                
		#Execute TruncatePokemon Script
		if executeTruncatePokemon:
			truncated = 0
			print('')
			print('[PokemonTruncate] Executing pokemon truncate script...')
			cursor = conn.cursor()
			tstamp = time.time()
			if debugLogging:
				print('[PokemonTruncate][DEBUG] timestamp used to truncate Pokemon: {}'.format(tstamp))
			sql = """TRUNCATE TABLE pokemon"""
			cursor.execute(sql)
			truncated = 1
			conn.commit()
			if debugLogging:
				print("[PokemonTruncate] Pokemontable truncated.")
			if TruncatePokemonLogging:
				log("[PokemonTruncate] Pokemontable truncated.")
				print("[PokemonTruncate] Pokemontable truncated.")
	else:
		if not logActionsOnly:
			log("[Script] Multiscript was started, but no configs were enabled".format(len(convertedGyms)))
		if debugLogging:
			print("[DEBUG] Script was executed, but no configs were enabled")
            


except Error as e :
	print ("Error", e)
	print(" ")
	print("[ERROR] Script Ran with Error at: ")
	now = datetime.datetime.now()
	print ('[ERROR] {}'.format(now.strftime("%H:%M:%S, %Y-%m-%d")))
	if conn is not None:
		conn.rollback()

finally:
    #closing database connection.
	if conn is not None:
		if(conn.is_connected()):
			conn.close()
			if debugLogging:
				print(" ")
				print("[DEBUG] MySQL connection is closed")
			if verboseLogging:
				print("[VERBOSE] Script Succesfully Ran at: ")
				now = datetime.datetime.now()
				print ('[VERBOSE] {}'.format(now.strftime("%H:%M:%S, %Y-%m-%d")))