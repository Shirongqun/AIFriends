import lancedb
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import LanceDB
from langchain_text_splitters import RecursiveCharacterTextSplitter

from web.documents.utils.custom_embeddings import CustomEmbeddings


def insert_documents():
    # 文件读取器
    loader = TextLoader('./web/documents/data.txt', encoding='utf-8')
    documents = loader.load()
    # 文件切分器
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    print(f"已切分成 {len(texts)} 个片段。")

    # 创建向量化实例：创建 Embedding 对象
    embeddings = CustomEmbeddings()
    # 连接向量数据库：连接到 LanceDB 数据库
    db = lancedb.connect('./web/documents/lancedb_storage')
    # 创建向量表：将文档片段向量化并存储到数据库
    vector_db = LanceDB.from_documents(
        documents=texts,
        embedding=embeddings,
        connection=db,
        table_name='my_knowledge_base',
        mode='overwrite',
    )
    print(f"已插入 {vector_db._table.count_rows()} 行数据。")


