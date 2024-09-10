# Apifox Markdown 美化

## 简介

通过 [Apifox](https://apifox.com/) 导出的 Markdown 文档，部分超链接、标题采用了`<a>`、`<h2>`标签。

导致在部分 Markdown 编辑器中无法正确展示目录层级结构，因此编写本脚本，用于将这些标签进行转换。

## 使用方式

```shell
python3 beautify-apifox-md.py /your_file_path/xxx.md
```
