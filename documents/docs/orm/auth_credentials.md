# AuthCredentials

| カラム名          | 型    | NULL | UNIQ | PK  | FK  | 概要 |
|-------------------|-------|:----:|:----:|:---:|:---:|------|
| id                | Text  |      | 〇   | 〇  |     | ユーザID、UUID4 |
| username          | Text  |      | 〇   |     |     | Basic認証を行うためのユーザ名 |
| password          | Text  |      |      |     |     | Basic認証を行うためのパスワード |
| token             | Text  | 〇   | 〇   |     |     | Bearer認証を行うためのトークン |
| token_due         | Text  | 〇   |      |     |     | Bearer認証を行うためのトークンの有効期限 |
| refresh_token     | Text  | 〇   | 〇   |     |     | Bearer認証を行うためのリフレッシュトークン |
| refresh_token_due | Text  | 〇   |      |     |     | Bearer認証を行うためのリフレッシュトークンの有効期限 |
| salt              | Text  | 〇   |      |     |     | トークン生成時に使われたsalt |
