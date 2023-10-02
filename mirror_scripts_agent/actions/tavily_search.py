from tavily import Client
from config import Config

CFG = Config()

tavily_client = Client(CFG.tavily_api_key)

# For advanced search:
# results = tavily.search(query="Should I invest in Apple in 2024?", search_depth="advanced")