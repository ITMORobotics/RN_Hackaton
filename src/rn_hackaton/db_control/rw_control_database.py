import sqlite3
from PIL import Image
import io
import copy
import os

class KernDBControl:
    def __init__(self, db_file_path: str):
        if not os.path.exists(db_file_path):
            print("unknown path db")
            raise RuntimeError('Unknown path database file')
        self.__connection = sqlite3.connect(db_file_path)


    @staticmethod
    def convertToBinaryData(pil_img: Image):
        new_img = copy.deepcopy(pil_img)
        buf = io.BytesIO()
        new_img.save(buf, format='PNG')
        byte_im = buf.getvalue()
        return byte_im

    def insert_analyze_data(self, id: int, mass: float, photo_front_pil: str, photo_left_pil: str):
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


        return False
    
    def read_last_analize_data(self, kern_id: int):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM kern_info WHERE kern_id=? ORDER BY kern_id DESC LIMIT 1", (kern_id,))
        row = list(cur.fetchone())
        # Convert the bytes into a PIL image
        pil_front_photo = Image.open(io.BytesIO(row[2]))
        pil_left_photo = Image.open(io.BytesIO(row[3]))
        return (row[:2], pil_front_photo, pil_left_photo)

    def read_kern_table_by_id(self, kern_id: int) -> tuple:
        # try:
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM kern WHERE id=?", (kern_id,))
        row = cur.fetchone()
        return row

    def __del__(self):
            self.__connection.close()
            print("The sqlite connection is closed")