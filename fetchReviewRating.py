from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import textwrap
import csv
 
#windows(chromedriver.exeのパスを設定)
CHROME_PATH = r'..\chromedriver_win32\chromedriver.exe'
URL = 'https://www.amazon.co.jp/dp/B0B34R89ZX/'
 
# 全ページ分をリストにする
def get_all_reviews(url):
    review_list = []                        #　初期化
    i = 1                                   #　ループ番号の初期化
    while True:
        print(i,'page_search')              #　処理状況を表示
        i += 1                              #　ループ番号を更新
#        text = get_amazon_page_info(url)    #　amazonの商品ページ情報(HTML)を取得する

        driver.get(url)                         #　chromeブラウザでurlを開く
        text = driver.page_source               #　ページ情報を取得

        amazon_bs = BeautifulSoup(text, features='lxml')    #　HTML情報を解析する
        reviews = amazon_bs.select('.review-text')          #　ページ内の全レビューのテキストを取得
        
        for review in reviews:                              #　取得したレビュー数分だけ処理を繰り返す
            review_list.append(review)                      #　レビュー情報をreview_listに格納
             
        next_page = amazon_bs.select('li.a-last a')         # 「次へ」ボタンの遷移先取得
        
        # 次のページが存在する場合
        if next_page != []: 
            # 次のページのURLを生成   
            next_url = 'https://www.amazon.co.jp/' + next_page[0].attrs['href']    
            url = next_url  # 次のページのURLをセットする
            
            sleep(1)        # 最低でも1秒は間隔をあける(サーバへ負担がかからないようにする)
        else:               # 次のページが存在しない場合は処理を終了
            break
 
    return review_list
 
#インポート時は実行されないように記載
if __name__ == '__main__':
         
    options = Options()                     #　オプションを用意
    options.add_argument('--incognito')     #　シークレットモードの設定を付与

    #　chromedriverのパスとパラメータを設定
    driver = webdriver.Chrome(executable_path=CHROME_PATH, options=options)
    driver.implicitly_wait(20)              #　指定したドライバの要素が見つかるまでの待ち時間を設定

    
    

    # URLをレビューページのものに書き換える
    review_url = URL.replace('dp', 'product-reviews')
    # レビュー情報の取得
    review_list = get_all_reviews(review_url)    

    driver.quit()                           #　chromeブラウザを閉じる
     
    #CSVにレビュー情報の書き出し
    with open('data/sample.csv','w',encoding='Shift_JIS') as f:
        writer = csv.writer(f, lineterminator='\n')
 
        # 全データを表示
        for i in range(len(review_list)):
            csvlist=[]
            review_text = textwrap.fill(review_list[i].text, 500)
            #データ作成
            csvlist.append('No.{} : '.format(i+1))      #　便宜上「No.XX」の文字列を作成
            csvlist.append(review_text.strip())         #　レビューテキストの先頭・末尾の空白文字を除去
            # 出力    
            writer.writerow(csvlist)                    
        # ファイルクローズ
        f.close()
