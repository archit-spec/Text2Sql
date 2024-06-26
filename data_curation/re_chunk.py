from semantic_chunkers import StatisticalChunker
from semantic_router.encoders import HuggingFaceEncoder
encoder = HuggingFaceEncoder(name = "sentence-transformers/all-MiniLM-L6-v2")
chunker = StatisticalChunker(encoder=encoder,
    dynamic_threshold=True,
    min_split_tokens=30,
    max_split_tokens=40,
    window_size=2,
    enable_statistics=False,  # to print chunking stats
)


lis = []
chunks = chunker._chunk(lis)
