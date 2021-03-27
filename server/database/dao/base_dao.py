import MySQLdb

class BaseDao:
  __instance = None
  HOST = 'localhost'
  USER = 'bm_admin'
  PASSWD = 'kou46490603'
  DB = 'book_manage'
  CHARSET = 'utf8'

  @staticmethod
  def get_instance():
    """ シングルトンにインスタンスを作成する """
    if BaseDao.__instance == None:
      BaseDao()
    return BaseDao.__instance 

  def __init__(self):
    """ 初期設定。 """
    if BaseDao.__instance != None:
      raise Exception("すでにインスタンスが存在します")
    self.conn = None
    self.cur  = None
    BaseDao.__instance = self 

  def connect(self):
    """ DB との接続を行う。処理終了後は disconnect を呼ぶこと
    予期せぬ自体が発生した場合に例外を投げる
    """
    try:
      if self.conn is not None or self.cur is not None:
        raise Exception('DBへの接続が初期化されていません')
      self.conn = MySQLdb.connect( # DBへの接続の確保
        host=BaseDao.HOST,
        user=BaseDao.USER,
        passwd=BaseDao.PASSWD,
        charset=BaseDao.CHARSET,
        db=BaseDao.DB
      ) 
      self.cur = self.conn.cursor() # カーソルの作成
      # self.cur.execute(f'USE {BaseDao.db};')
    except Exception as e:
      raise e

  def disconnect(self):
    """ DB との接続解除を行う。 DBへ接続 (connect)後に使用する。
    予期せぬ自体が発生した場合に例外を投げる
    """
    if self.conn == None or self.cur == None:
      raise Exception('DBに接続されていません')
    
    try:
      self.cur.close()
      self.conn.close()
    except Exception as e:
      raise e
    finally:
      self.cur = None
      self.conn = None

if __name__ == '__main__':
  sql_str = 'SHOW COLUMNS FROM hashed_user_credentials;'
  dao = BaseDao.get_instance()
  dao.connect()
  print('DB 接続開始')
  dao.disconnect()
  print('DB 接続解除')