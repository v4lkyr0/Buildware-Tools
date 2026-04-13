# Copyright (c) 2026 v4lkyr0
# See LICENSE file for details

from Plugins.Utils import *
from Plugins.Config import *

try:
    from datetime import datetime
except Exception as e:
    MissingModule(e)

Title("Discord Snowflake Decoder")

def decode_snowflake(snowflake):
    try:
        snowflake_int = int(snowflake)
        timestamp_ms  = (snowflake_int >> 22) + 1420070400000
        timestamp     = datetime.fromtimestamp(timestamp_ms / 1000.0)
        worker_id     = (snowflake_int & 0x3E0000) >> 17
        process_id    = (snowflake_int & 0x1F000) >> 12
        increment     = snowflake_int & 0xFFF
        
        return {
            'valid': True,
            'snowflake': snowflake,
            'timestamp': timestamp,
            'timestamp_ms': timestamp_ms,
            'worker_id': worker_id,
            'process_id': process_id,
            'increment': increment,
            'binary': bin(snowflake_int)[2:].zfill(64)
        }
    except Exception as e:
        return {'valid': False, 'error': str(e)}

try:
    snowflake = input(f"{INPUT} Snowflake Id {red}->{reset} ").strip()
    
    if not snowflake:
        print(f"{ERROR} No Snowflake provided!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Decoding Snowflake..", reset)

    result = decode_snowflake(snowflake)
    
    if result['valid']:
        now = datetime.now()
        age = now - result['timestamp']
        days = age.days
        years = days // 365
        remaining_days = days % 365

        snowflake_id = snowflake
        created_at = result['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        timestamps_ms = result['timestamp_ms']
        worker_id = result['worker_id']
        process_id = result['process_id']
        increment = result['increment']
        binary = result['binary']

        Scroll(f"""
 {INFO} Snowflake Id    :{red} {snowflake_id}
 {INFO} Created At      :{red} {created_at}
 {INFO} Timestamps {red}({white}MS{red}){white} :{red} {timestamps_ms}
 {INFO} Worker Id       :{red} {worker_id}
 {INFO} Process Id      :{red} {process_id}
 {INFO} Increment       :{red} {increment}
 {INFO} Binary          :{red} {binary}
 {INFO} Age             :{red} {years} years, {remaining_days} days
""")
    else:
        ErrorId()
    
    Continue()
    Reset()

except Exception as e:
    Error(e)