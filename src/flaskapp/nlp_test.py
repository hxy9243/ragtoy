from flaskapp.nlp import Preprocessor

testtexts = [
    {
        'text': '''1936年9月到1938年7月間，圖靈大部分時間都在普林斯頓大學的教堂下學習，
第二年被評選爲簡·伊麗莎·寶潔獎學金客座教授（Jane Eliza Procter Visiting Fellow）。
除了他的純數學工作外，他亦研究密碼學，並建造了機電二進制乘法器的四個階段中的其中三個。[16]
1938年6月，獲普林斯頓數學系博士學位；[17]他的論文基於序數的邏輯系統[18][19] ,介紹了序數邏輯的概念和相對計算的概念，
其中圖靈機增加了所謂的預言機，允許學者進一步研究圖靈機無法解決的問題。馮·諾依曼有意聘請圖靈做他的博士後助理，但他謝絕后又回到了英國。[20]
1939年图灵回到剑桥，聆听了维特根斯坦关于数学基本原理（Foundations of mathematics）的讲座。
他们激烈地争论，图灵为形式主义辩护，而维特根斯坦則认为把数学抬得太高反而不能发现任何绝对真理。
在第二次世界大戰期間，圖靈是布萊切利莊園破解德國密碼的主要參與者。歷史學家和戰時密碼破譯員
Asa Briggs曾說過：“你需要非凡的天賦，你需要布萊切利的天才，而圖靈就是那個天才。”[21]
從1938年9月起，圖靈在英國密碼破譯組織政府密碼和密碼學校(GC&CS)兼職工作。他與高級GC&CS密碼破譯員第利溫·諾克斯一起專注於對納粹德國使用的恩尼格玛密码机進行密碼分析。[22]
1939年7月，波蘭密碼局在華沙附近的會議上向英國和法國提供了恩尼格玛密码机機器的詳細信息以及他們解密恩尼格玛密码机機器信息的方法。
不久後，圖靈和諾克斯開發了一個更具廣泛性的解決方案。[23]波蘭方法依賴於德國人的不嚴謹的程序。圖靈的方法更通用，使用基於恩尼格玛分析，他為此製作了炸彈的功能規範（對波蘭炸彈的改進）。[24]
1939年图灵被英国皇家海军招聘，并在英国軍情六處监督下从事对納粹德国机密军事密码的破译工作。两年后他的小组成功破译了德国的密码系统恩尼格玛密码机[註 1]，
从而使得军情六处对德国的军事指挥和计划瞭如指掌。但是军情六处以機密为由隐瞒了图灵小组的存在和成就，将其所得情报据为己有。
通過使用統計技術來優化密碼破譯過程中不同可能性的試驗，圖靈為該課題做出了創新貢獻。他寫了兩篇有關數學計算方法的論文，
題為 The Applications of Probability to Cryptography[25]和Paper on Statistics of Repetitions[26] ,
對 GC&CS 及其繼任者GCHQ具有十分重要的價值，以至於它們直到2012年4月才被發布給英國國家檔案館，
也就是他誕辰一百週年前不久。一位GCHQ數學家，“他只承認自己是理查德”，當時說，根據官方保密法，
內容被封鎖了大約 70 年這一事實證明了它們的重要性，以及它們與戰後密碼分析的相關性：[27]''',
        'language': 'zh-tw',
    },
    {
        'text': '''Born in Maida Vale, London, Turing was raised in southern England. He graduated at King's College, Cambridge, with a degree in mathematics.
Whilst he was a fellow at Cambridge, he published a proof demonstrating that some purely mathematical yes–no questions can never be answered by computation
and defined a Turing machine, and went on to prove that the halting problem for Turing machines is undecidable.
In 1938, he obtained his PhD from the Department of Mathematics at Princeton University.
During the Second World War, Turing worked for the Government Code and Cypher School at Bletchley Park,
Britain's codebreaking centre that produced Ultra intelligence. For a time he led Hut 8,
the section that was responsible for German naval cryptanalysis.
Here, he devised a number of techniques for speeding the breaking of German ciphers,
including improvements to the pre-war Polish bomba method, an electromechanical machine that could find
settings for the Enigma machine. Turing played a crucial role in cracking intercepted coded messages that enabled the Allies to defeat the Axis powers in many crucial engagements,
including the Battle of the Atlantic.[11][12] ''',
        'language': 'en',
    },
    {
        'text': '''第二次世界大戦に先立つ1938年9月から、イギリスにおける暗号解読組織である政府暗号学校
(GCCS) でパートタイムで働き始める。そこで、ディリー・ノックス（英語版）と共にエニグマの解読に当たった[33]。
第二次世界大戦勃発の5週間前の1939年7月25日、ポーランド軍参謀本部第2部暗号局 (en)
とイギリスおよびフランスの関係者がワルシャワで会合し、ポーランドが解明したエニグマのローター回路についての情報を得ていた。
チューリングとノックスは、その情報を元に、問題にアプローチしようとしていた[34]。
ポーランドの解読法は不安定なもので、ドイツ側がいつでも変更可能だった。
実際1940年5月に変更されている。チューリングの方法はもっと汎用的でクリブ式暗号解読全般に使えるもので、最初の bombe（ボンブ）
の機能仕様に盛り込まれていた。
詳細は「マリアン・レイェフスキ#ボンバ設計者」を参照
詳細は「ヘンリク・ジガルスキ#ボンバ制作者のひとり」を参照
詳細は「イェジ・ルジツキ#ボンバ制作者のひとり」を参照
詳細は「ボンバ (暗号解読機)#ポーランド軍参謀本部第2部暗号局#作成」を参照
1939年9月4日、イギリスがドイツに宣戦布告した翌日、GCCSの戦時中の基地となっていたブレッチリー・パークに出頭した[35]。
bombe の仕様は戦時中の暗号解読でチューリングが成し遂げた5つの成果のうち最初の1つである。
他には、ドイツ海軍が使っていたインジケーター手続きの推測、Banburismus と名付けた bombe の効率を上げる統計的手法の開発、
Turingery と名付けた Lorenz SZ 40/42 (Tunny) のホイール群のカム設定を明らかにする手続きの開発、そして終戦間近に開発した音声信号スクランブラー Delilah である。
''',
        'language': 'ja',
    }
]


def test_langdetect():
    prep = Preprocessor()

    for testtext in testtexts:
        assert prep.get_lang(testtext['text']) == testtext['language'], \
            'Wrong language detected'


def test_chunkifier():
    prep = Preprocessor()

    for testtext in testtexts:
        text = testtext['text'].replace('\n', '')
        chunks = prep.chunkify(text, max_chunktokens=128)

        assert len(chunks) != 1, 'Chunks not splitted correctly?'
        for chunk, token in chunks:
            assert len(chunks) != 0, 'Detected empty chunk'

        print('#' * 40)

        for chunk, token in chunks:
            print('-' * 20)
            print(f'{token}:', chunk)

        print('#' * 40)
