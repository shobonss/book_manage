import sys
import responder
import json
from pathlib import Path
dao_path = str(Path('../database/').resolve())
print(dao_path)
sys.path.append(dao_path)
from dao.hashed_user_credentials_dao import HashedUserCredentialsDao

# Vue.jsクライアントサーバからのみアクセス可能にする
api = responder.API(cors=True, cors_params={
  'allow_origins': ['http://192.168.10.106:8080'],
  'allow_methods': ['*'],
  'allow_headers': ['*']
})

@api.route('/')
def hello_world(req,resp):
  resp.media = {
    'hello': 'world'
  }

# ログイン認証を行う。認証が成功した場合、トークンを返す
# 直接Stringでパスワードを送信するのは避けたほうがいい？
@api.route('/auth/login')
async def auth_login(req, resp):
  # POST メソッド以外でのアクセスを禁じる
  if req.method != 'post':
    resp.status_code = 403

  data = await req.media()
  print('login called: ', data['userID'], data['password'])
  dao = HashedUserCredentialsDao.get_instance()
  (isSuccess, id_token) = dao.authenticate_user(data['userID'], data['password'])
  
  if isSuccess:
    resp.status_code = 200
  else:
    resp.status_code = 401
  resp.media = { 'isSuccess': isSuccess, 'id_token': id_token }
  print(isSuccess, id_token)

# 新規ユーザを登録する。パスワードは暗号化した上で保持する。 
@api.route('/auth/create/user')
async def auth_create_user(req, resp):
  # POST メソッド以外でのアクセスを禁じる
  if req.method != 'post':
    resp.status_code = 403
    return
  print('auth_create_user')
  user_data = await req.media()

  # リクエストにクレデンシャル情報が含まれていることの確認 
  if user_data['credentials']['userID'] == '' or user_data['credentials']['password'] == '':
    return
  print(user_data)
  credentials = user_data['credentials']
  user_id, password = credentials['userID'], credentials['password']
  dao = HashedUserCredentialsDao.get_instance()
  isSuccess = dao.insert_credentials(user_id, password)
  if isSuccess:
    resp.media = user_data 
  print('登録処理: ', isSuccess)


def hasCredentials(payload: dict) -> bool:
  """ 送信されたリクエストの中にクレデンシャル情報が存在するか判定する """
  key_set = set(payload.keys())
  return 'username' in key_set and 'password' in key_set

if __name__ == '__main__':
  api.run()