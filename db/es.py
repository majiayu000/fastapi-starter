from config import Config
from elasticsearch import Elasticsearch


def get_es():
    cfg = Config()
    ELASTICSEARCH_HOST = cfg.get_config("ELASTICSEARCH_HOST")
    ELASTICSEARCH_PORT = cfg.get_config("ELASTICSEARCH_PORT")
    es = Elasticsearch([{"host": ELASTICSEARCH_HOST, "port": ELASTICSEARCH_PORT}])
    return es


def create_index_mapping(es, schema, index_name):
    # 获取 UserLoginLog 模型的字段信息
    schema = schema.schema()

    # 构建 Elasticsearch 的索引映射
    properties = {
        field_name: {"type": "keyword"}  # 将所有字段都映射为 keyword 类型
        for field_name in schema["properties"].keys()
    }

    # 创建索引映射
    body = {"mappings": {"properties": properties}}

    # 创建索引
    es.indices.create(index=index_name, body=body)
