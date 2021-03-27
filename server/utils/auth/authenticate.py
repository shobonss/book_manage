import hashlib
import datetime

def create_jwt(user_id: str):
  """ JWTトークンを自作する。以下3項目を SHA256でハッシュ化し、 '.'連結を行う。
  ヘッダ: ハッシュ化アルゴリズムと Tokenタイプ
  ペイロード：user_id と作成時刻
  署名: 秘密鍵
  INPUT:
    user_id (str): トークン作成ユーザのID。既にSHA256でハッシュ化されているからどうしよう・・・
  OUTPUT:
    token   (str): 作成された JWTトークン
  """
  now_time = datetime.datetime.now()
  now_time = "{0:%Y-%m-%d_%H:%M:%S}".format(now_time) 
  
  header = {
    'alg': 'SHA256',
    'typ': 'token'
  }
  payload = {
    'iat': user_id,
    'sub': now_time
  }
  secret_key = 'secret_book-manage'
  header_sha = hashlib.sha256(str(header).encode()).hexdigest()
  payload_sha = hashlib.sha256(str(payload).encode()).hexdigest()
  secret_sha = hashlib.sha256(secret_key.encode()).hexdigest()
  jwt_token = '{0}.{1}.{2}'.format(header_sha, payload_sha, secret_sha)
  return jwt_token

if __name__ == '__main__':
  import hashlib
  user_id = 'hogehoge_shobonss'
  user_id_sha = hashlib.sha256(user_id.encode()).hexdigest()
  jwt_token = create_jwt(user_id_sha)
  print(jwt_token)