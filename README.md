# 1. 单元测试目录

- [1. 单元测试目录](#1-单元测试目录)
  - [1.1. 记录常用的代码](#11-记录常用的代码)
  - [1.2. 单测运行方法](#12-单测运行方法)

## 1.1. 记录常用的代码

- 所有的代码尽量编写单测

- av 视频相关
- cmd_util 命令行
- fs 文件系统
- md5 统计md5
- net 网络相关
- system

## 1.2. 单测运行方法

- 运行所有测试例: `python3 -m pytest -v`
- 运行指定目录: `python3 -m pytest fs/`
- 运行指定文件: `python3 -m pytest fs/file_test.py`
- 运行指定类或函数: `python3 -m pytest fs/file_test.py::FileTest`
- 运行指定类函数: `python3 -m pytest fs/file_test.py::FileTest::test_file_size`
- 运行指定标记函数: `python3 -m pytest test -m finished`
- 包含详细信息加 -v 参数
- 打印print信息加 --capture=no
- 打印logging信息加  -o log_cli=true -o log_cli_level=DEBUG
- 举例 `python3 -m pytest -o log_cli=true -o log_cli_level=DEBUG src/av/audio_opt_test.py::SilenceAudioSegmentTest`

- module:sensitive_codec
  - python3 -m src.sensitive.sensitive_codec --help
  - python3 -m src.sensitive.sensitive_codec decode-file
  - python3 -m src.sensitive.sensitive_codec encode-json
  - python3 -m src.sensitive.sensitive_codec check-file
- module:sensitive_replace
  - python3 -m src.sensitive.sensitive_replace --help
  - python3 -m src.sensitive.sensitive_replace replace-root --dir=testdata
  - python3 -m src.sensitive.sensitive_replace replace-root --dir=testdata --enc=0
  - python3 -m src.sensitive.sensitive_replace replace-root --dir=testdata --enc=1

- package:fs
  - python3 -m src.fs.dir_util
  - python3 -m src.fs.file_replace
