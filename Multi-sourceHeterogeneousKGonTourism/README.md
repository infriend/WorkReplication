## Extract Knowledge from Heterogeneous Data

《基于多源异构数据的中文旅游知识图谱构建方法研究》的方法复现。该文章主要包括从百科网站和垂直网站获取旅游知识数据，构建知识图谱的方法。其中从网页的info box直接提取知识的部分，与游记非结构化无关。对于非结构化数据，该文章主要从中抽取属性值，补全知识图谱的实体缺失属性，其知识抽取方法大致如下：首先选择好需要抽取的属性，然后扫描句子，根据权重计算规则选择候选句，最后利用CRF对候选句中的属性值进行抽取。

### Environment Requirements

于Ubuntu 20.04.3 LTS，anaconda-2021.05的base环境下编写实现。

外部软件：crf++ v0.58

相关依赖包：

* Python 3.8
* jieba
* certifi==2020.6.20
* numpy==1.17.0

### Data

110篇携程游记的非结构化正文，需要组内给定的标准化数据集中的content_list，senmantic_list，以及train和test的json文件。此外需要template文件，用于CRF工具的训练，以及youji_test_list和youji_train_list，以标定语料的对应实体。

### Files

* data/

  * content_list/：该文件夹直接复制标准数据集即可

  * outputdata/

    * entity.txt：测试实体结果
    * relation.txt：测试关系结果

  * semantic_list/：该文件夹直接复制标准数据集即可

  * testdata/

    * test.txt：测试集标注文本
    * youji_test.json：该文件夹直接复制标准数据集即可

  * trainingdata/

    * template：模板文件
    * train.txt：训练集标注文本

    * youji_train.json：该文件夹直接复制标准数据集即可

  * youji_test_list.txt：标记test所属游记id

  * youji_train_list.txt：标记train所属游记id

* dataprocess/

  * datalabeling.py：自动标注
  * wordseg.py：词性标注和分词分句
  * readdata.py：数据预处理
  * candidate.py：词汇扩充处理，词频统计

* paper/：相应论文

* main.py：运行该文件，带参数--mode，参数包括“train”和“test”

* crfpp.py：CRF++的训练和调用脚本

### Usage

训练请直接运行main.py，带参数--mode，参数包括“train”和“test”两种，结果手动复制到标准评估脚本的相应目录进行评估。

### Result

运行配置：Intel® Core™ i5-6300HQ CPU @ 2.30GHz × 4 ，15.4 GiB，无独立显卡

|   表头   | 代码总行数 | 时间              | 测试指标                                                     |
| :------: | ---------- | ----------------- | ------------------------------------------------------------ |
| 实体提取 |            | 40.057419538497925 | Entity Precision: 0.05861627162075592<br/>Entity Recall: 0.10511200459506032 |
| 关系挖掘 |            | 40.057419538497925 | Triplet Precision: 0.003177405119152692<br/>Triplet Recall: 0.017212526894573272 |
| 实体提取和关系挖掘 | | 40.057419538497925 | Triplet Precision: 0.003177405119152692<br/>Triplet Recall: 0.017212526894573272<br/>Entity Precision: 0.058898847631242<br/>Entity Recall: 0.10568638713383113 |

