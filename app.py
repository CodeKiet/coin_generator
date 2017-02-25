import os
import shutil
import json
import re
import subprocess

def git(*args):
    return subprocess.check_call(['git'] + list(args))

def create_folder(path):
    os.mkdir(path)

def generate_coin_config(line):
    configuration = line.split(';')
    STAT = bool(configuration[1])
    SYMBOL = configuration[2]
    CoinName = configuration[3]
    RepCoinName = configuration[2]
    BlockTime = int(configuration[4])
    Confs = int(configuration[5])
    TX_FEE = float(configuration[6])
    LIMIT_MIN = float(configuration[7])
    SCRIPT_ADDRESS = int(configuration[8])
    PUBKEY_ADDRESS = int(configuration[9])
    IP = configuration[10]
    MAIN_IP = configuration[11]
    NET_NAME = configuration[12]
    GitRep = configuration[13]
    URL = configuration[14]
    EXPLORER = configuration[15]
    DEMON_NAME = configuration[16]
    IS_BASE = bool(configuration[17])
    PROXY = configuration[18]
    PROXY_PORT = configuration[19]
    STORAGE = configuration[22]

    if bool(STAT):
        print ('Coin: {0} start gen'.format(CoinName))
        path = data_dir + '/' + RepCoinName + '_compiler'
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=False, onerror=None)
            create_folder(path)
        else:
            create_folder(path)

        os.chdir(path)

        app_file = open(path + '/app.py', 'w')

        app_file.write('{0}\n'.format('import os'))
        app_file.write('{0}\n'.format('import shutil'))
        app_file.write('{0}\n'.format(''))
        app_file.write('{0}\n'.format('#// configuration section'))

        app_file.write('{0}\n'.format(''))
        app_file.write('{0}\n'.format('def create_folder(path):'))
        app_file.write('{0}\n'.format('    os.mkdir(path)'))

        app_file.write('{0}\n'.format(''))

        app_file.write('{0} = \'{1}\'\n'.format('DATA_DIR', '/root/coin_base/data'))
        app_file.write('{0} = \'{1}\'\n'.format('LOG_DIR', '/root/coin_base/log'))
        app_file.write('{0} = \'{1}\'\n'.format('APP_DIR', '/root/coin_base/app'))
        app_file.write('{0} = \'{1}\'\n'.format('SOURCE_DIR', '/root/coin_base/source'))
        app_file.write('{0} = \'{1}\'\n'.format('SQL_FILE', '/root/coin_base/export.sql'))

        app_file.write('{0}\n'.format(''))
        app_file.write('{0}\n'.format('if not os.path.exists(\'/root/coin_base\'):'))
        app_file.write('{0}\n'.format('    create_folder(\'/root/coin_base\')'))

        app_file.write('{0}\n'.format(''))
        app_file.write('{0}\n'.format('if not os.path.exists(DATA_DIR):'))
        app_file.write('{0}\n'.format('    create_folder(DATA_DIR)'))

        app_file.write('{0}\n'.format(''))
        app_file.write('{0}\n'.format('if not os.path.exists(DATA_DIR/' + RepCoinName + '):'))
        app_file.write('{0}\n'.format('    create_folder(if os.path.exists(DATA_DIR/' + RepCoinName + ')'))

        app_file.write('{0}\n'.format(''))
        app_file.write('{0}\n'.format('if not os.path.exists(SOURCE_DIR):'))
        app_file.write('{0}\n'.format('    create_folder(SOURCE_DIR)'))

        app_file.write('{0}\n'.format(''))
        app_file.write('{0}\n'.format('if not os.path.exists(LOG_DIR):'))
        app_file.write('{0}\n'.format('    create_folder(LOG_DIR)'))

        app_file.write('{0}\n'.format(''))
        app_file.write('{0}\n'.format('if not os.path.exists(APP_DIR):'))
        app_file.write('{0}\n'.format('    create_folder(APP_DIR)'))

        app_file.close()

        git("clone", GitRep, RepCoinName)

        if os.path.exists(path + '/' + RepCoinName):
            rpcdump_file = path + '/' + RepCoinName + '/src/rpcdump.cpp'
            if os.path.exists(rpcdump_file):
                fhand = open(rpcdump_file)
                for file_line in fhand:
                    start = file_line.find('if (fHelp || params.size() < 1 || params.size() >')
                    if start > -1:
                        tmp_method = int(file_line.split()[9].replace(')', ''))
                        if tmp_method == 3:
                            METHOD = 1
                        else:
                            METHOD = 2
                        break
                fhand.close()
            else:
                rpcdump_file = path + '/' + RepCoinName + '/src/wallet/rpcdump.cpp'
                if os.path.exists(rpcdump_file):
                    fhand = open(rpcdump_file)
                    for file_line in fhand:
                        start = file_line.find('if (fHelp || params.size() < 1 || params.size() >')
                        if start > -1:
                            tmp_method = int(file_line.split()[9].replace(')', ''))
                            if tmp_method == 3:
                                METHOD = 1
                            else:
                                METHOD = 2
                            break
                    fhand.close()

            if os.path.exists(path + '/' + RepCoinName + '/src/clientversion.h'):
                clientversion_file = path + '/' + RepCoinName + '/src/clientversion.h'
            else:
                if os.path.exists(path + '/' + RepCoinName + '/src/version.h'):
                    clientversion_file = path + '/' + RepCoinName + '/src/version.h'

            if os.path.exists(clientversion_file):
                fhand = open(clientversion_file)
                tmp_MAJOR = 0
                tmp_MINOR = 0
                tmp_REVISION = 0
                tmp_BUILD = 0
                for file_line in fhand:
                    start_MAJOR = file_line.find('#define CLIENT_VERSION_MAJOR')
                    if start_MAJOR > -1:
                        tmp_MAJOR = file_line.split()[2]
                        continue

                    start_MINOR = file_line.find('#define CLIENT_VERSION_MINOR')
                    if start_MINOR > -1:
                        tmp_MINOR = file_line.split()[2]
                        continue

                    start_REVISION = file_line.find('#define CLIENT_VERSION_REVISION')
                    if start_REVISION > -1:
                        tmp_REVISION = file_line.split()[2]
                        continue

                    start_BUILD = file_line.find('#define CLIENT_VERSION_BUILD')
                    if start_BUILD > -1:
                        tmp_BUILD = file_line.split()[2]
                        break
                fhand.close()
                wallet_version = '{0}.{1}.{2}.{3}'.format(tmp_MAJOR, tmp_MINOR, tmp_REVISION, tmp_BUILD)
            else:
                wallet_version = '0.0.0.0'

            if os.path.exists(path + '/' + RepCoinName + '/autogen.sh'):
                Compile_Method = 1
            else:
                Compile_Method = 2

            if os.path.exists(path + '/' + RepCoinName + '/Makefile.am'):
                make_file = path + '/' + RepCoinName + '/Makefile.am'
            else:
                if os.path.exists(path + '/' + RepCoinName + '/src/makefile.unix'):
                    make_file = path + '/' + RepCoinName + '/src/makefile.unix'
                else:
                    if os.path.exists(path + '/' + RepCoinName + '/src/Makefile.unix'):
                        make_file = path + '/' + RepCoinName + '/src/Makefile.unix'
                    else:
                        if os.path.exists(path + '/' + RepCoinName + '/src/makefile'):
                            make_file = path + '/' + RepCoinName + '/src/makefile'
                        else:
                            if os.path.exists(path + '/' + RepCoinName + '/src/Makefile'):
                                make_file = path + '/' + RepCoinName + '/src/Makefile'

            if os.path.exists(make_file):
                fhand = open(make_file)
                tmp_deamon = 0
                regex = re.compile(r'([a-z][a-z-\']+[a-z])', re.I)
                for file_line in fhand:
                    start_deamon = file_line.find('BITCOIND_BIN=')
                    if start_deamon > -1:
                        tmp_deamon = re.compile(r'(src/[A-z]+)', re.I).search(file_line).groups()[0]
                        tmp_deamon = tmp_deamon.replace('src/', '')
                        continue

                    start_deamon = file_line.find('BITMARKD_BIN=')
                    if start_deamon > -1:
                        tmp_deamon = file_line.split()[2]
                        continue

                    start_deamon = file_line.find('D_BIN=')
                    if start_deamon > -1:
                        tmp_deamon = file_line.split()[2]
                        break
                fhand.close()
                deamon = '{0}'.format(tmp_deamon)
            else:
                deamon = ''

            coin_config_json_file = open(current_dir + '/configuration' + '/' + RepCoinName + '.json', 'w')
            coin_config_json = json.dumps({"Coin": SYMBOL,
                                           "Settings": {"Method": METHOD,
                                                        "Version": wallet_version,
                                                        "Compile_Method": Compile_Method,
                                                        "CoinName": CoinName,
                                                        "BlockTime": BlockTime,
                                                        "Confs": Confs,
                                                        "Tx_Fee": TX_FEE,
                                                        "Limit_Min": LIMIT_MIN,
                                                        "Script_Address": SCRIPT_ADDRESS,
                                                        "Pubkey_Address": PUBKEY_ADDRESS,
                                                        "IP": IP,
                                                        "Main_IP": MAIN_IP,
                                                        "Net_Name": NET_NAME,
                                                        "Git": GitRep,
                                                        "Deamon_Name": deamon,
                                                        "Is_Base": IS_BASE,
                                                        "Storage": STORAGE,
                                                        "Port": START_PORT,
                                                        "RPC_Port": START_RPC_PORT,
                                                        "Number": Counter},
                                           "Make_Settings": {"NO_PAY_TX_FEE": NO_PAY_TX_FEE,
                                                             "RECREATE_CONFIG": RECREATE_CONFIG,
                                                             "LOG_COMPILE": LOG_COMPILE,
                                                             "SQL_MODE": SQL_MODE,
                                                             "USE_TOR": USE_TOR,
                                                             "ALL_CORES": ALL_CORES},
                                           "Dirs_Settings": {"DATA_DIR": "/root/coin_base/data",
                                                             "LOG_DIR": "/root/coin_base/log",
                                                             "APP_DIR": "/root/coin_base/app",
                                                             "SOURCE_DIR": "/root/coin_base/source",
                                                             "SQL_FILE": "/root/coin_base/export.sql"}

                                           }, sort_keys=True, indent=4)
            coin_config_json_file.write(coin_config_json + '\n')
            coin_config_json_file.close()

    else:
        print ('Coin: {0} ignore'.format(CoinName))
    shutil.rmtree(path, ignore_errors=False, onerror=None)

path = 'coin_source.csv'
current_dir = os.getcwd()
data_dir = current_dir + '/DATADIR'

if os.path.exists(data_dir):
    shutil.rmtree(data_dir, ignore_errors=False, onerror=None)
    create_folder(data_dir)
else:
    create_folder(data_dir)

if os.path.exists(current_dir + '/configuration'):
    shutil.rmtree(current_dir + '/configuration', ignore_errors=False, onerror=None)
    create_folder(current_dir + '/configuration')
else:
    create_folder(current_dir + '/configuration')


Counter = int(input("Enter start number: "))
START_PORT = int(input("Enter port start number: "))
START_RPC_PORT = int(input("Enter rpc port start number: "))
NO_PAY_TX_FEE = bool(input("No pay tx fee?: "))
RECREATE_CONFIG = bool(input("Re-create config?: "))
LOG_COMPILE = bool(input("Logging compilation?: "))
SQL_MODE = int(input("Enter SQL MODE: "))
USE_TOR = bool(input("Use TOR?: "))
ALL_CORES = bool(input("Use all CPU cores?: "))

f = open(path, 'r')
for line in f:
    generate_coin_config(line)

    Counter += 1
    START_PORT += 2
    START_RPC_PORT += 2

f.close()
