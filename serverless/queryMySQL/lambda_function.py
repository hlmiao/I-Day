import json
import sys
import logging
import rds_config
import pymysql

rds_host  = "db-****.cieypdfdsfsfadfds.rds.cn-northwest-1.amazonaws.com.cn"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    print("ERROR: Unexpected error: Could not connect to MySQL instance.")
    print(e)
    sys.exit()
logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def lambda_handler(event, context):
    # TODO implement
    item_count = 0
    result = []
    print ("event:",event)
    str1 = event['requestContext']['identity']['userArn']
    strlist = str1.split('/')
    table_name = event['queryStringParameters']['data_table']
    print ("strlist-1:",strlist[-1])
    sqlstr = "select percolumn from data_permission where access_key = '{}' and data_table = '{}'".format(strlist[-1],table_name)
    print ("sqlstr:",sqlstr)

    
    with conn.cursor() as cur:
        
        cur.execute(sqlstr)
        row = cur.fetchone()
        columns = row[0]
        
        cur.execute("select {} from {}".format(columns,table_name))
        columnslst = columns.split(',')
        print ("columnslst:",columnslst)
        rows = cur.fetchall()

        for row in rows:
            print ("row:",row)
            
            col_num = 0
            row_map = {}
            for col in columnslst:
                
                row_map[col] = str(row[col_num])
                col_num = 1 + col_num
                #print(row["quote_time"], row["open_price"])
            result.append(row_map)
            print ("row_map:",row_map)
            print("--------------------------")
        print(result)
    
    #conn.commit()
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
