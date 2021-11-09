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

### **pythonでは1行コメントは行頭に「#」ですが複数行コメントアウトするときに「\"""」で囲います。**  
### **下のように記述するとコメント初め「\"""」の行頭を「#」に切り替えることで,**
### **簡単に複数行コメントを切り替えられます。**
例  
この時はprint文は実行される
> \#"""  
> print("test")  
> \#"""

この時はprint文は実行されない
> \"""  
> print("test")  
> \#"""  

<br><br>
### **PID制御について**  
PIDとは比例、微分、積分制御を同時におこなうことで正確な制御を行う制御です  
Kpは比例制御 `誤差が多ければ多いほど操作量を増やす`  
Kiは積分制御 `誤差のある状態が長い時間続けばそれだけ操作量の変化を大きくして目標値に近づけようとする`  
Kdは微分制御 `急激な操作量の変化が起こった場合その変化の大きさに比例した操作を行うことでその急激な操作量に抗しようとする役目を果たす。`
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
<br><br>

## 参考資料
***
クラス/インスタンスについて  
<https://uxmilk.jp/39906>  
<https://techacademy.jp/magazine/23289>
<br><br>

tryについて  
<https://note.nkmk.me/python-try-except-else-finally/>  
<https://docs.python.org/ja/3/tutorial/errors.html>
<br><br>

マルチプロセスについて  
<https://docs.python.org/ja/3/library/multiprocessing.html>  
<https://qiita.com/y518gaku/items/db3b0ced6d62b616f961>  
<https://qiita.com/t_okkan/items/4127a87177ed2b2db148>
<br><br>

PIDについて  
<https://qiita.com/BIG_LARGE_STONE/items/4f8af62b3edc4a03c4a5>  
<https://shizenkarasuzon.hatenablog.com/entry/2018/08/27/002812>  
<https://algorithm.joho.info/seigyoriron/python-control-pid/>  
<https://y373.sakura.ne.jp/data/sice_visit_study2020/part2.pdf>  
<http://www.picfun.com/motor05.html>  
***