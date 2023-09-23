###### 数据来源

- human std data：
    - ~~[sdtconvdatahuman.json](sdtconvdatahuman.json) (截至0329)；~~
      已经处理了，无需再关心；
    - 未来再有新的人工数据：sdtconvdatahuman_**.json 添加data信息存储；
- enhance std data：
    - [enhanceData.jsonl](enhanceData.jsonl)
    - [wrongparser.jsonl](wrongparser.jsonl)

###### enhance data 修正与转换

- 首先 check 数据中的错误数据：[giikindataforly.py](giikindataforly.py)
- 然后将修正的数据转换为微调ly需要的标准数据格式：[giikindataforly.py](giikindataforly.py)
- 每次修正与转换的enhance data存储在[correct_enhance_data.jsonl](correct_enhance_data.jsonl)中；
- 每次修正与转换的human data存储在[correct_human_data.jsonl](correct_human_data.jsonl)中

###### human data 修正与转换

- ~~人工标注数据：[sdtconvdatahuman.json](sdtconvdatahuman.json) (截至0923人工标注数据)；~~
  这个数据不用再看了，因为它已经被第一批的训练整理完毕了
- 未来再有新的人工标注的数据，做好数据格式的修正以及ly的格式转换；

###### 人工数据和enhance数据的融合以供ly训练

- 截至0923： 人工 + enhance 得到的标准 ly 数据存储在 [all_train_human_enhancedata_0923.jsonl](all_train_human_enhancedata_0923.jsonl)
- 未来再得到的新的训练数据：存储在human_enhancedata_**.jsonl 文件中

###### 所有训练数据的融合

~~~
旧版本的训练数据与新的训练数据的融合，之后再展开训练过程;
均融合进入：all_train_human_enhancedata_all.jsonl中；
所有训练过程，均以all_train_human_enhancedata_all.jsonl数据为训练数据；
~~~


