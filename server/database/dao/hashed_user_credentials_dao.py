import sys
from pathlib import Path
sys.path.append(str(Path('../').resolve()))
print(sys.path)
import MySQLdb
from .base_dao import BaseDao
from utils.auth.authenticate import create_jwt

class HashedUserCredentialsDao(BaseDao):
  """ データベース Book_Manage, テーブル名 hashed_user_credentials に接続するための DAOクラス """
  __instance = None

  def __init__(self):
    super().__init__()
    self.TABLE_NAME = 'hashed_user_credentials'
    HashedUserCredentialsDao.__instance = self

  @staticmethod
  def get_instance():
    """ シングルトンにインスタンスを作成する """
    if HashedUserCredentialsDao.__instance == None:
      HashedUserCredentialsDao()
    return HashedUserCredentialsDao.__instance 
    
  def select_all(self) -> list:
    """ 全レコードを取得するための関数 """
    query_str = f'SELECT user_id, password FROM {self.TABLE_NAME};'
    try:
      self.connect()
      all_user_credentials = self.cur.execute(query_str)
      self.disconnect()
    except Exception as e:
      raise e 
    return all_user_credentials
  
  def authenticate_user(self, user_id: str, password: str) -> tuple:
    """ ユーザ認証を行うための関数。引数のユーザIDを持つレコードを検索し、パスワードが一致するか検証する。
    INPUT:
      user_id  (str): SHA256でハッシュ化されたユーザID
      password (str): SHA256でハッシュ化されたパスワード
    OUTPUT: tuple
      isSuccess (bool): 認証成否。成功した場合は Trueを取る
      id_token (dict): 
        user_id (str): 入力と同じユーザID (認証に失敗した場合は None )
        token   (str): ログイントークン。 60分くらい有効にする予定 (認証に失敗した場合は None )
    """
    query_str = f"SELECT user_id, password FROM {self.TABLE_NAME} WHERE user_id = '{user_id}';"
    print(query_str)
    isSuccess = False
    id_token = { 'user_id': None, 'jwt-token': None }
    try:
      self.connect()
      self.cur.execute(query_str)
      correct_password = self.cur.fetchone() 
      _, correct_password = correct_password
      self.disconnect()
    except Exception as e:
      return (isSuccess, id_token)
    # ユーザIDに一致するレコードが存在するかどうか判定
    # 登録されたパスワードと入力されたパスワードが一致するか判定する
    if correct_password == password:
      isSuccess = True
      token = create_jwt(user_id)
      id_token = { 'user_id': user_id, 'jwt-token': token }
    return (isSuccess, id_token)

  def insert_credentials(self, user_id: str, password: str) -> bool:
    """ テーブルに新たなユーザのクレデンシャルを追加する。 
    INPUT:
      user_id  (str): SHA256でハッシュ化されたユーザID
      password (str): SHA256でハッシュ化されたパスワード
    OUTPUT:
      登録に成功した場合 True を返し、失敗した場合はエラーを投げる
    """
    insert_str = f"INSERT INTO {self.TABLE_NAME} ( user_id, password ) VALUES ( '{user_id}', '{password}' );"
    isSuccess = False
    try:
      self.connect()
      res = self.cur.execute(insert_str)
      self.conn.commit()
      self.disconnect()
      isSuccess = True
    except Exception as e:
      raise e 
    return isSuccess 

if __name__ == '__main__':
  print('HashedUserCredentialsDao クラスのテスト')
  dao = HashedUserCredentialsDao.get_instance()
  credentials = dao.select_all()
  print('全レコードの取得完了')
  print(credentials)