## 檔案說明
- crawler 寫到有點厭世的爬蟲們
    - record.py 操作資料庫的共用函數
    - chromedriver.exe 驅動器(請自備)
    - chinatimes.py 中時爬蟲
    - tvbs.py TVBS爬蟲
    - udn 聯合報爬蟲
    - udn_star 聯合報娛樂版爬蟲
- model 訓練完的模型
    - head_5 使用首段訓練，可辨別5分類
    - title_5 使用標題訓練，可辨別5分類
- plots 圖表
    - dataset.png 資料集組成圖
- articles.db 珍貴的資料集 SQLite格式
- BertClassifier.py 分類器模型物件定義
- Dataset.py 預處理資料集物件定義
- train.py 訓練分類器模型
- train.log 訓練過程的log
- demo.py 展示分類成果
- bertTest.py bert實驗
- evaluate_types.py 測量單個模型在各類別的精準度
- evaluate.py 測量各模型的精準度
- split.py 分割訓練、測試資料集
- statistic.py 統計資料集組成，並顯示圖表
- readme.md 說明檔案


以下模型由於LFS空間不足，無法上傳，需要的話可視情況自己訓練👍
- head_4 使用首段訓練，可辨別4分類
- title_4 使用標題訓練，可辨別4分類 