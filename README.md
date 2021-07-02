# このプロジェクトは2021年作成海洋ロボットのプロジェクトです

## フォルダ構成
***
- main  
    - config `mainをどのように動かすか設定ファイル格納`
    - my_mod `自作関数格納`
<br><br>

- presonal `個人用フォルダ`
<br><br>

- pool `学校プール実験用`
    - my_mod `自作関数格納`
    - Teaching_data `Teachingデータ格納用`
***
<br><br>

## 役立つ知識
***

pythonでは1行コメントは行頭に「#」ですが複数行コメントアウトするときに「\"""」で囲います  
下のように記述するとコメント初め「\"""」の行頭を「#」に切り替えることで簡単に複数行コメントを切り替えられます。
> 例  
> この時はprint文は実行される
>> \#"""  
>> print("test")  
>> \#"""
>
> この時はprint文は実行されない
>> \"""  
>> print("test")  
>> \#"""
***
<br><br>

## 書き方できをつけている事
***
### **try文**
エラーが発生しそうな場所はtry文でエラーを検出してます。  
機体の航行に影響する重大なエラーはループを抜けるように設計しています。  
また、通信をはじめる時にエラーが発生する場合があります。  
通信開始時のエラーは処理を再試行するように、  
ループを抜ける時は必ずどのファイルのどの関数でどんなエラーが発生したか記述しています。
<br><br>

### **ループを抜けるとき**
ループから抜ける時は必ずモータを止めること。もし、止めなかったらモータが周り続ける。  
その時は緊急用スイッチを抜いてもよい。
<br><br>

### **処理が重いコード**
処理が重いコードはmultiproceeを使ってコアを分割して処理をしています。  
しかし、raspiはコアが4しかないためコアを分割して処理を軽くできるのはprocessが4つ程と考えられる。
cpu使用率やコアの使用率を検証していないので正確ではないかもしれないが、  
process数は4つに制限している。
<br><br>

### **コンフィグファイル**
機体の動きを切り替えるときコードを編集したりコメントアウトするのは手間が掛かるため、  
コンフィグファイルを採用している。  
コード実行するときにコンフィグファイルが読み込まれる。  
コンフィグファイルの書き方はファイルに記述している。
***