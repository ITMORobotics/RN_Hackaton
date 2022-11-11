import sqlite3
from PIL import Image
import io
import copy

class KernDBControl:
    def __init__(self, db_file_path: str):
        try:
            self.__connection = sqlite3.connect(db_file_path)
        except sqlite3.Error as e:
            print("Connection error", e)
        

    @staticmethod
    def convertToBinaryData(pil_img: Image):
        new_img = copy.deepcopy(pil_img)
        buf = io.BytesIO()
        new_img.save(buf, format='PNG')
        byte_im = buf.getvalue()
        return byte_im

    def insert_analyze_data(self, id: int, mass: float, photo_front_pil: str, photo_left_pil: str):
        try:
            cursor = self.__connection.cursor()
            print("Connected to SQLite")
            sqlite_insert_blob_query = """ INSERT OR REPLACE INTO kern_info (kern_id, mass, front_photo, left_photo) VALUES (?, ?, ?, ?)"""

            front_photo_bin = self.convertToBinaryData(photo_front_pil)
            left_photo_bin = self.convertToBinaryData(photo_left_pil)
            # Convert data into tuple format
            data_tuple = (id, mass, front_photo_bin, left_photo_bin)
            cursor.execute(sqlite_insert_blob_query, data_tuple)
            self.__connection.commit()
            print("New kern data succefully added")
            cursor.close()
            return True

        except sqlite3.Error as error:
            print("Failed to insert kern data in to table", error)

        return False
    
    def read_last_analize_data(self, kern_id: int):
        try:
            cur = self.__connection.cursor()
            cur.execute("SELECT * FROM kern_info WHERE kern_id=? ORDER BY kern_id DESC LIMIT 1", (kern_id,))
            row = list(cur.fetchone())
            # Convert the bytes into a PIL image
            print(type(row[2]))
            pil_front_photo = Image.open(io.BytesIO(row[2]))
            pil_left_photo = Image.open(io.BytesIO(row[3]))
            return (row[:2], pil_front_photo, pil_left_photo)

        except sqlite3.Error as error:
            print("Failed to read data from table: KERN-INFO", error)
        
        return None

    def read_kern_table_by_id(self, id: int) -> tuple:
        try:
            cur = self.__connection.cursor()
            cur.execute("SELECT * FROM kern WHERE id=?", (id,))
            row = cur.fetchone()
            return row

        except sqlite3.Error as error:
            print("Failed to read data from table: KERN", error)
        
        return None

    def __del__(self):
            self.__connection.close()
            print("The sqlite connection is closed")