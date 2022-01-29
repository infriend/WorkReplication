## Research and Implementation on Construction Method of Knowledge Graph in Tourism Domain

《旅游领域知识图谱构建方法的研究和实现》的方法复现，该文章在知识提取方面的主要工作是属性值提取，包括模式匹配、搜索引擎问答、词汇场和监督学习四种方法，并最终四种方法混合使用，实现了旅游景点知识图谱的知识扩充。本工作的复现包括了原文中的地址属性值的提取。

具体而言，模式匹配方法通过人工构建触发词和匹配规则，并匹配待提取句子中出现的触发词前后的词性，若满足匹配规则就保存提取的关系。搜索引擎问答通过请求搜索引擎回答，爬取返回结果的第一条实现提取，目前由于搜索引擎变化，爬取方法已无法与文章对应，故而放弃该方法。词汇场通过把训练语料中的特定词汇取出并附上相应权值构建词汇场，扫描待提取语料中的词汇，计算其命中的词汇场中的词汇权值，决定是否提取词语作为属性值。监督学习方法训练分类器，对所有的词性为“ns”的词语进行分类，确定其是否为有效属性值。

### Environment Requirements

于Ubuntu 20.04.3 LTS，anaconda-2021.05的base环境下编写实现。

相关依赖包：

* Python 3.8

* ltp 4.1.5

* numpy

* torch 1.10.1

### Data

110篇携程游记的非结构化正文，需要组内给定的标准化数据集中的content_list，senmantic_list，以及train和test的json文件。此外需要youji_test_list和youji_train_list，以标定语料的对应实体。

* synonyms.txt ：本文需要地址属性的相应触发词，需要否定词集，为此准备的同义词林文件
* triggers_filtered.txt：经过机器筛选、人工再筛选的触发词集
* myallnegs.txt：经过机器筛选、人工再筛选的否定词集

### Files

* data/
  * content_list/：该文件夹直接复制标准数据集即可
  * negatives/
    * dict_negative.txt：收集得到的基准否定词集
    * myallnegs.txt：同义词林扩充后人工筛选的否定词集
    * negatives01.txt：同义词林扩充后否定词集
  * outputdata/
    * entity.txt：测试实体结果
    * relation.txt：测试关系结果
  * semantic_list/：该文件夹直接复制标准数据集即可
  * testdata/
    * test_ns_poses.npy：有ns词性词汇的句子词性集合
    * test_ns_sentences.npy：有ns词性词汇的句子分词集合
    * test_x.npy：测试集特征
    * test_y.npy：测试集标签
    * testwordfrequency.npy：测试集词频文件
    * youji_test.json：该文件夹直接复制标准数据集即可
  * trainingdata/
    * word_frequency_training.npy：训练集词频文件
    * youji_train.json：该文件夹直接复制标准数据集即可
  * eclf.pkl：voting模型文件
  * scaler.pkl：训练集标准化模型
  * synonyms.txt：同义词林
  * triggers.txt：扩充的触发词集
  * triggers_filtered.txt：人工筛选的触发词集
  * wordfield.npy：词汇场
  * youji_test_list.txt：标记test所属游记id
  * youji_train_list.txt：标记train所属游记id
* dataprocess/
  * all_ns_poses.npy：训练集词性
  * all_ns_sentences.npy：训练集分词
  * datalabeling.py：自动标注
  * ltpprocess.py：词性标注和分词分句
  * readdata.py：数据预处理
  * vocabulary.py：词汇扩充处理，词频统计
* extractmethod/
  * machinelearning.py：监督学习模块，训练和提取
  * patternmatch.py：模式匹配模块
  * wordfield.py：词汇场模块的构建和提取
* paper/：相应论文
* main.py：无实际作用，记录了大致思路
* train.py：训练3种方法
* test.py：实际应用三种方法，生成entity.txt和relation.txt

### Usage

由于所需的额外词汇文件均提前准备好，不再重复进行需要人工的词汇扩充。

训练请直接运行train.py，提取请运行test.py，结果手动复制到标准评估脚本的相应目录进行评估。

### Result

运行配置：Intel® Core™ i5-6300HQ CPU @ 2.30GHz × 4 ，15.4 GiB，无独立显卡

|   表头   | 代码总行数 | 时间              | 测试指标                                                     |
| :------: | ---------- | ----------------- | ------------------------------------------------------------ |
| 实体提取 |            | 453.9712839126587 | Entity Precision: 0.3333333333333333<br/>Entity Recall: 0.0008615738081562321 |
| 关系挖掘 |            | 453.9712839126587 | Triplet Precision: 0.0<br/>Triplet Recall: 0.0               |

