### 具体的数据最新状态汇总

##### 一些已经固定的数据

- [x] 原始对话数据Chinese-LLaMa-Alpaca:[datagiikin](..%2F..%2F_giikin_pro_conversations%2FChinese-LLaMA-Alpaca%2Fdatagiikin)
- [x] 人工数据：sdtconvdatahuman_**.json 添加data信息存储，做好数据格式的修正以及ly的格式转换；因为BL的数据是从LY format得到的；
- [x] 人工标注的标准数据：[sdtconvdatahuman_0923.json](sdtconvdatahuman_0923.json)
- enhance std data：
    - [x] @截至1007：有最新的增强出来的数据没有处理：[enhanceData.jsonl](enhanceData.jsonl)
- 增强过程中生成的其它数据
    - [ ] [wrongparser.jsonl](wrongparser.jsonl)：没有处理

##### @截至1008~1011 做的一些数据增添与改动

###### version-2-process-1：将conv数据和instruction数据分开标注【得到BL format data】

- [x] 基于[splitintentandconvdata.py](splitintentandconvdata.py)准备了第二版模型数据文件 （LY format）：
    - jsonl 版本：
        - [all_train_human_enhancedata_all_conv.jsonl](all_train_human_enhancedata_all_conv.jsonl)
        - [all_train_human_enhancedata_all_intentslot.jsonl](all_train_human_enhancedata_all_intentslot.jsonl)
    - json 版本：
        - [all_train_human_enhancedata_all_conv.json](all_train_human_enhancedata_all_conv.json)
        - [all_train_human_enhancedata_all_intentslot.json](all_train_human_enhancedata_all_intentslot.json)
    - 这个脚本还给出了即将用于拼接 BL format train data 的初步的instruction data

- [x] 新增了一些人工数据(ly format)：[sdtconvdatahuman_1007.txt](sdtconvdatahuman_1007.json)，changed file name 2 sdtconvdatahuman_1007.json

- [x] 再从[all_train_human_enhancedata_all_conv.json](all_train_human_enhancedata_all_conv.json)中标注并分离一些conv数据，

- 最后通过[all_traindata_base_ly_change2_belle.py](all_traindata_base_ly_change2_belle.py)：
  得到一批标注的（LY）对话数据：[all_train_human_enhancedata_all_conv.batch.1.json](all_train_human_enhancedata_all_conv.batch.1.json)；
  **【值得注意的是】**：在上述标注对话的过程中，也生成了一些难处理的conv：[add_new_conv.json](add_new_conv.json)。

- [x] **【BLformat指令数据的获取】** 新增了一些指令数据：[all_train_human_enhancedata_all_intentslot.batch.1.json](all_train_human_enhancedata_all_intentslot.batch.1.json)
  这部分的数据是从[all_train_human_enhancedata_all_intentslot.json](all_train_human_enhancedata_all_intentslot.json)中标注后剪切出来的，
  同时在标注slot数据的过程中，新增了一些新的意图以及难处理的业务问题数据：[add_new_intent.json](add_new_intent.json)；
  **同时借助脚本将其构造成为BL format instruction数据（借助的脚本是[transintentslotdata2belleinstructiondata.py](transintentslotdata2belleinstructiondata.py)）**

- [x] 最后，生成的整体的 BL format数据就是如下三部分：
    - LY format enhance data and trans 2 BL format data
    - LY format human data and trans 2 BL formta data
    - BL format instruction data
    - **上述过程均在:
      [all_traindata_base_ly_change2_belle.py](all_traindata_base_ly_change2_belle.py)
      +[transintentslotdata2belleinstructiondata.py](transintentslotdata2belleinstructiondata.py)中完成！**

- 添加了instruction数据到 BELLE conv 数据中：
    - [transintentslotdata2belleinstructiondata.py](transintentslotdata2belleinstructiondata.py)
    - [train_instdata.belle.batch.1.json](train_instdata.belle.batch.1.json)
- 通过上述步骤（人工+enhance conv data + instruction data），共得到基于version-2的conv数据 for bl format data:
    - [all_train_human_enhancedata_all_belle.version.2.train.json](all_train_human_enhancedata_all_belle.version.2.train.json)
    - [all_train_human_enhancedata_all_belle.version.2.dev.json](all_train_human_enhancedata_all_belle.version.2.dev.json)
- [x] 顺便存储一份 ly format data：[all_train_human_enhancedata_all_ly.json](all_train_human_enhancedata_all_ly.json) 以备 ly 使用；
  另外需要说明的是，这个数据中没有包含 instruction 的数据，因为这个数据一开始就是BL的格式，没有BL format 转化为 LY format的脚本，所有就没存。

###### 再重新得到 LY format train data

- 由于BL format data 对于 instruction的训练挺好的，因此对于LY，不再处理LY format 的 instruction data
- 只新增一个[all_traindata_base_ly_change2_ly.py](all_traindata_base_ly_change2_ly.py)，用来得到LY format data，执行LY训练
- 最后得到的 LY format conv data：[all_train_human_enhancedata_all_ly.json](all_train_human_enhancedata_all_ly.json)

-----------------------------------------------------------------------------------------

##### 关于1007号及以前的所有训练数据说明 （~~第一个版本的对话(指令)数据 version-1~~ 这个版本的数据已经作废 ）

###### version-1-process-1：获取所有数据：人工+enhance：enhance data 和人工标注的数据的 【初步】 修正与转换 （4 LY）

- check的是[enhanceData.jsonl](enhanceData.jsonl)增强出来的数据，基于脚本：[giikindataforly.py](giikindataforly.py)；
  同时这个文件还是将原始的enhance出来的数据 trans2 ly format data 的脚本，且这个文件的数据用完以后记得清空，以便后续继续增强；
- 该脚本生成的大的文件的是：[correct_enhance_data.jsonl](correct_enhance_data.jsonl)
- 融合人工标注的数据；
- 最终得到[all_train_human_enhancedata_all.jsonl](all_train_human_enhancedata_all.jsonl)；

###### version-1-process-2：enhance data 和人工标注的数据 【初步】 的修正与转换后 ---> 存储 (4 LY format)

- [x] 每次修正与转换的enhance data存储在[correct_enhance_data.jsonl](correct_enhance_data.jsonl)中； for ly format： {human，assistant}
- [x] 每次修正与转换的human data存储在[correct_human_data.jsonl](correct_human_data.jsonl)中； for ly format：{human，assistant}
- [x] 每次修正后的数据，都将和以前标注的数据汇合存储在：[all_train_human_enhancedata_all.jsonl](all_train_human_enhancedata_all.jsonl)文件中；
- [x] 整理好的数据cp至LY项目:将all_train_human_enhancedata_all.jsonl cp 至
  [giikin_train_data.jsonl](..%2F..%2F_giikin_pro_conversations%2FFirefly%2Fdata%2Fgiikin_train_data.jsonl) 方便LY训练

###### 得到version-1-process-3: 得到BL的训练数据

这个版本就是基于[all_traindata_base_ly_change2_belle.py](all_traindata_base_ly_change2_belle.py)获得的。

- [all_train_human_enhancedata_all_belle.dev.json](all_train_human_enhancedata_all_belle.dev.json)
- [all_train_human_enhancedata_all_belle.train.json](all_train_human_enhancedata_all_belle.train.json)

###### version-1的训练数据基于BL训练后的问题

- [x] 在这个版本中，指令和对话标注在一起，但是训练的效果不理想，模型过于拟合；