import streamlit as st

# 1. Give the webpage a clean title
st.title("📊 Run Lockroom script")
st.write("Click the button below to run the Activate Ice ream Locker room script.")

# 2. Create the big trigger button
if st.button("🚀 Run Script Now", type="primary"):
    with st.spinner("Running... please wait."):
        
        try:
            # --------------------------------------------------
import gspread
import pymysql
from tqdm import tqdm

# URL for sheet: "2026 SPRING FPB Orders"
URL = 'https://docs.google.com/spreadsheets/d/1Iv0Dy9v8iNDto8UMWkQIJMiGbtw_s8ZZ-Umi2B_-0eo/edit?gid=107303743#gid=107303743'
gc = gspread.service_account(filename='locker-room-api-429201-06ac45b92626.json')
sh = gc.open_by_url(URL)
worksheet = sh.worksheet('Orders')

conn = pymysql.connect(
    host='67.217.58.155',
    user='infoplast_dev',
    password='2lqz989Ej-E{',
    database='infoplast_wp_fpbto'
)
USER_TABLE = 'bc8mYiC_users'
meta_key = 'ice_cream_section_show'
cursor = conn.cursor()

sheetdata = worksheet.get_all_values()

for i in (range(1, worksheet.row_count)):
    try:
        user_email = sheetdata[i][5]
        # get user ID
        cursor.execute(f'SELECT ID FROM LsRm07_users WHERE user_email="{user_email}"')
        res = cursor.fetchone()
        if res is None:
            continue
        else:
            user_id = res[0]
            print([user_email, user_id, sheetdata[i][20]])
            if sheetdata[i][20] != '':
                cursor.execute(f'SELECT umeta_id FROM LsRm07_usermeta WHERE user_id={user_id} AND meta_key="{meta_key}"')
                res = cursor.fetchone()
                if res is None:
                    # INSERT
                    sql = 'INSERT INTO LsRm07_usermeta (user_id, meta_key, meta_value) VALUES (%s, %s, %s)'
                    values = (user_id, meta_key, '1')
                    try:
                        cursor.execute(sql, values)
                        conn.commit()  # Commit the transaction
                        print("\tRecord inserted successfully")
                    except pymysql.MySQLError as e:
                        print(f"\tError: {e}")
                        conn.rollback()  # Rollback in case of error
                else:
                    # UPDATE
                    sql = 'UPDATE LsRm07_usermeta SET meta_value = %s WHERE user_id = %s AND meta_key = %s'
                    values = ('1', user_id, meta_key)
                    try:
                        cursor.execute(sql, values)
                        conn.commit()  # Commit the transaction
                        print("\tRecord updated successfully")
                    except pymysql.MySQLError as e:
                        print(f"\tError: {e}")
                        conn.rollback()  # Rollback in case of error
            else:
                cursor.execute(f'SELECT umeta_id FROM LsRm07_usermeta WHERE user_id={user_id} AND meta_key="{meta_key}"')
                res = cursor.fetchone()
                if res is None:
                    # INSERT
                    sql = 'INSERT INTO LsRm07_usermeta (user_id, meta_key, meta_value) VALUES (%s, %s, %s)'
                    values = (user_id, meta_key, '0')
                    try:
                        cursor.execute(sql, values)
                        conn.commit()  # Commit the transaction
                        print("\tRecord inserted successfully")
                    except pymysql.MySQLError as e:
                        print(f"\tError: {e}")
                        conn.rollback()  # Rollback in case of error
                else:
                    # UPDATE
                    sql = 'UPDATE LsRm07_usermeta SET meta_value = %s WHERE user_id = %s AND meta_key = %s'
                    values = ('0', user_id, meta_key)
                    try:
                        cursor.execute(sql, values)
                        conn.commit()  # Commit the transaction
                        print("\tRecord updated successfully")
                    except pymysql.MySQLError as e:
                        print(f"\tError: {e}")
                        conn.rollback()  # Rollback in case of error
    except:
        pass
    # # if user has his locker room
    # if user_email in members or len(members) == 0:
    #     # get user ID
    #     cursor.execute(f'SELECT ID FROM bc8mYiC_users WHERE user_email="{user_email}"')
    #     res = cursor.fetchone()
    #     if res is None:
    #         continue
    #     else:
    #         user_id = res[0]
    #         print([user_email, user_id])
    #         # MVP Ring
    #         for j in range(10):
    #             val = sheetdata[i][MVP1_NUM + j]
    #             meta_key = 'mvp'
    #             if j > 0:
    #                 meta_key += str(j)
    #             print('\t', [sheetdata[0][MVP1_NUM + j], meta_key, val])
    #             if '*' in val:
    #                 val = val.split('*')[1].strip()

    #                 cursor.execute(f'SELECT umeta_id FROM bc8mYiC_usermeta WHERE user_id={user_id} AND meta_key="{meta_key}"')
    #                 res = cursor.fetchone()
    #                 if res is None:
    #                     # INSERT
    #                     sql = 'INSERT INTO bc8mYiC_usermeta (user_id, meta_key, meta_value) VALUES (%s, %s, %s)'
    #                     values = (user_id, meta_key, val)
    #                     try:
    #                         cursor.execute(sql, values)
    #                         conn.commit()  # Commit the transaction
    #                         print("\tRecord inserted successfully")
    #                     except pymysql.MySQLError as e:
    #                         print(f"\tError: {e}")
    #                         conn.rollback()  # Rollback in case of error
    #                 else:
    #                     # UPDATE
    #                     sql = 'UPDATE bc8mYiC_usermeta SET meta_value = %s WHERE user_id = %s AND meta_key = %s'
    #                     values = (val, user_id, meta_key)
    #                     try:
    #                         cursor.execute(sql, values)
    #                         conn.commit()  # Commit the transaction
    #                         print("\tRecord updated successfully")
    #                     except pymysql.MySQLError as e:
    #                         print(f"\tError: {e}")
    #                         conn.rollback()  # Rollback in case of error
    #             else:
    #                 print('')
    #         # College Ring
    #         for j in range(10):
    #             val = sheetdata[i][COLLEGE1_NUM + j]
    #             meta_key = 'college'
    #             meta_key += str(j + 1)
    #             print('\t', [sheetdata[0][COLLEGE1_NUM + j], meta_key, val])
    #             if '*' in val:
    #                 val = val.split('*')[1].strip()

    #                 cursor.execute(
    #                     f'SELECT umeta_id FROM bc8mYiC_usermeta WHERE user_id={user_id} AND meta_key="{meta_key}"')
    #                 res = cursor.fetchone()
    #                 if res is None:
    #                     # INSERT
    #                     sql = 'INSERT INTO bc8mYiC_usermeta (user_id, meta_key, meta_value) VALUES (%s, %s, %s)'
    #                     values = (user_id, meta_key, val)
    #                     try:
    #                         cursor.execute(sql, values)
    #                         conn.commit()  # Commit the transaction
    #                         print("\tRecord inserted successfully")
    #                     except pymysql.MySQLError as e:
    #                         print(f"\tError: {e}")
    #                         conn.rollback()  # Rollback in case of error
    #                 else:
    #                     # UPDATE
    #                     sql = 'UPDATE bc8mYiC_usermeta SET meta_value = %s WHERE user_id = %s AND meta_key = %s'
    #                     values = (val, user_id, meta_key)
    #                     try:
    #                         cursor.execute(sql, values)
    #                         conn.commit()  # Commit the transaction
    #                         print("\tRecord updated successfully")
    #                     except pymysql.MySQLError as e:
    #                         print(f"\tError: {e}")
    #                         conn.rollback()  # Rollback in case of error
    #             else:
    #                 print('')
    #         # Coin
    #         for j in range(30):
    #             val = sheetdata[i][COIN1_NUM + j]
    #             meta_key = 'coin'
    #             meta_key += str(j + 1)
    #             print('\t', [sheetdata[0][COIN1_NUM + j], meta_key, val])
    #             if '*' in val:
    #                 val = val.split('*')[1].strip()

    #                 cursor.execute(
    #                     f'SELECT umeta_id FROM bc8mYiC_usermeta WHERE user_id={user_id} AND meta_key="{meta_key}"')
    #                 res = cursor.fetchone()
    #                 if res is None:
    #                     # INSERT
    #                     sql = 'INSERT INTO bc8mYiC_usermeta (user_id, meta_key, meta_value) VALUES (%s, %s, %s)'
    #                     values = (user_id, meta_key, val)
    #                     try:
    #                         cursor.execute(sql, values)
    #                         conn.commit()  # Commit the transaction
    #                         print("\tRecord inserted successfully")
    #                     except pymysql.MySQLError as e:
    #                         print(f"\tError: {e}")
    #                         conn.rollback()  # Rollback in case of error
    #                 else:
    #                     # UPDATE
    #                     sql = 'UPDATE bc8mYiC_usermeta SET meta_value = %s WHERE user_id = %s AND meta_key = %s'
    #                     values = (val, user_id, meta_key)
    #                     try:
    #                         cursor.execute(sql, values)
    #                         conn.commit()  # Commit the transaction
    #                         print("\tRecord updated successfully")
    #                     except pymysql.MySQLError as e:
    #                         print(f"\tError: {e}")
    #                         conn.rollback()  # Rollback in case of error
    #             else:
    #                 print('')
    #         # Banner
    #         for j in range(9):
    #             val = sheetdata[i][BANNER1_NUM + j]
    #             meta_key = 'banner'
    #             meta_key += str(j + 1)
    #             print('\t', [sheetdata[0][BANNER1_NUM + j], meta_key, val])
    #             if '*' in val:
    #                 val = val.split('*')[1].strip()

    #                 cursor.execute(
    #                     f'SELECT umeta_id FROM bc8mYiC_usermeta WHERE user_id={user_id} AND meta_key="{meta_key}"')
    #                 res = cursor.fetchone()
    #                 if res is None:
    #                     # INSERT
    #                     sql = 'INSERT INTO bc8mYiC_usermeta (user_id, meta_key, meta_value) VALUES (%s, %s, %s)'
    #                     values = (user_id, meta_key, val)
    #                     try:
    #                         cursor.execute(sql, values)
    #                         conn.commit()  # Commit the transaction
    #                         print("\tRecord inserted successfully")
    #                     except pymysql.MySQLError as e:
    #                         print(f"\tError: {e}")
    #                         conn.rollback()  # Rollback in case of error
    #                 else:
    #                     # UPDATE
    #                     sql = 'UPDATE bc8mYiC_usermeta SET meta_value = %s WHERE user_id = %s AND meta_key = %s'
    #                     values = (val, user_id, meta_key)
    #                     try:
    #                         cursor.execute(sql, values)
    #                         conn.commit()  # Commit the transaction
    #                         print("\tRecord updated successfully")
    #                     except pymysql.MySQLError as e:
    #                         print(f"\tError: {e}")
    #                         conn.rollback()  # Rollback in case of error
    #             else:
    #                 print('')
    #         # state_ranking
    #         val = sheetdata[i][STATE_RANKING]
    #         meta_key = 'state_ranking'
    #         print('\t', [sheetdata[0][STATE_RANKING], meta_key, val])
    #         cursor.execute(
    #             f'SELECT umeta_id FROM bc8mYiC_usermeta WHERE user_id={user_id} AND meta_key="{meta_key}"')
    #         res = cursor.fetchone()
    #         if res is None:
    #             # INSERT
    #             sql = 'INSERT INTO bc8mYiC_usermeta (user_id, meta_key, meta_value) VALUES (%s, %s, %s)'
    #             values = (user_id, meta_key, val)
    #             try:
    #                 cursor.execute(sql, values)
    #                 conn.commit()  # Commit the transaction
    #                 print("\tRecord inserted successfully")
    #             except pymysql.MySQLError as e:
    #                 print(f"\tError: {e}")
    #                 conn.rollback()  # Rollback in case of error
    #         else:
    #             # UPDATE
    #             sql = 'UPDATE bc8mYiC_usermeta SET meta_value = %s WHERE user_id = %s AND meta_key = %s'
    #             values = (val, user_id, meta_key)
    #             try:
    #                 cursor.execute(sql, values)
    #                 conn.commit()  # Commit the transaction
    #                 print("\tRecord updated successfully")
    #             except pymysql.MySQLError as e:
    #                 print(f"\tError: {e}")
    #                 conn.rollback()  # Rollback in case of error

    #         # national_ranking
    #         val = sheetdata[i][NATIONAL_RANKING]
    #         meta_key = 'national_ranking'
    #         print('\t', [sheetdata[0][NATIONAL_RANKING], meta_key, val])
    #         cursor.execute(
    #             f'SELECT umeta_id FROM bc8mYiC_usermeta WHERE user_id={user_id} AND meta_key="{meta_key}"')
    #         res = cursor.fetchone()
    #         if res is None:
    #             # INSERT
    #             sql = 'INSERT INTO bc8mYiC_usermeta (user_id, meta_key, meta_value) VALUES (%s, %s, %s)'
    #             values = (user_id, meta_key, val)
    #             try:
    #                 cursor.execute(sql, values)
    #                 conn.commit()  # Commit the transaction
    #                 print("\tRecord inserted successfully")
    #             except pymysql.MySQLError as e:
    #                 print(f"\tError: {e}")
    #                 conn.rollback()  # Rollback in case of error
    #         else:
    #             # UPDATE
    #             sql = 'UPDATE bc8mYiC_usermeta SET meta_value = %s WHERE user_id = %s AND meta_key = %s'
    #             values = (val, user_id, meta_key)
    #             try:
    #                 cursor.execute(sql, values)
    #                 conn.commit()  # Commit the transaction
    #                 print("\tRecord updated successfully")
    #             except pymysql.MySQLError as e:
    #                 print(f"\tError: {e}")
    #                 conn.rollback()  # Rollback in case of error

    #         # tournament_teams
    #         val = sheetdata[i][TOURNAMENT_TEAMS]
    #         meta_key = 'tournament_teams'
    #         print('\t', [sheetdata[0][TOURNAMENT_TEAMS], meta_key, val])
    #         cursor.execute(
    #             f'SELECT umeta_id FROM bc8mYiC_usermeta WHERE user_id={user_id} AND meta_key="{meta_key}"')
    #         res = cursor.fetchone()
    #         if res is None:
    #             # INSERT
    #             sql = 'INSERT INTO bc8mYiC_usermeta (user_id, meta_key, meta_value) VALUES (%s, %s, %s)'
    #             values = (user_id, meta_key, val)
    #             try:
    #                 cursor.execute(sql, values)
    #                 conn.commit()  # Commit the transaction
    #                 print("\tRecord inserted successfully")
    #             except pymysql.MySQLError as e:
    #                 print(f"\tError: {e}")
    #                 conn.rollback()  # Rollback in case of error
    #         else:
    #             # UPDATE
    #             sql = 'UPDATE bc8mYiC_usermeta SET meta_value = %s WHERE user_id = %s AND meta_key = %s'
    #             values = (val, user_id, meta_key)
    #             try:
    #                 cursor.execute(sql, values)
    #                 conn.commit()  # Commit the transaction
    #                 print("\tRecord updated successfully")
    #             except pymysql.MySQLError as e:
    #                 print(f"\tError: {e}")
    #                 conn.rollback()  # Rollback in case of error

    #         # mvp_selection
    #         val = sheetdata[i][MVP_SELECTION]
    #         meta_key = 'mvp_selection'
    #         print('\t', [sheetdata[0][MVP_SELECTION], meta_key, val])
    #         cursor.execute(
    #             f'SELECT umeta_id FROM bc8mYiC_usermeta WHERE user_id={user_id} AND meta_key="{meta_key}"')
    #         res = cursor.fetchone()
    #         if res is None:
    #             # INSERT
    #             sql = 'INSERT INTO bc8mYiC_usermeta (user_id, meta_key, meta_value) VALUES (%s, %s, %s)'
    #             values = (user_id, meta_key, val)
    #             try:
    #                 cursor.execute(sql, values)
    #                 conn.commit()  # Commit the transaction
    #                 print("\tRecord inserted successfully")
    #             except pymysql.MySQLError as e:
    #                 print(f"\tError: {e}")
    #                 conn.rollback()  # Rollback in case of error
    #         else:
    #             # UPDATE
    #             sql = 'UPDATE bc8mYiC_usermeta SET meta_value = %s WHERE user_id = %s AND meta_key = %s'
    #             values = (val, user_id, meta_key)
    #             try:
    #                 cursor.execute(sql, values)
    #                 conn.commit()  # Commit the transaction
    #                 print("\tRecord updated successfully")
    #             except pymysql.MySQLError as e:
    #                 print(f"\tError: {e}")
    #                 conn.rollback()  # Rollback in case of error

# print(worksheet.row_count, worksheet.col_count, worksheet.cell(1, 1).value)

cursor.close()
conn.close()

            # --------------------------------------------------
            
            st.success("✅ Done! The script completed successfully.")
            
        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")