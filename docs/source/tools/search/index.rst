.. title:: Search Tools - Web & Information Retrieval
.. _search-tools:

🔍 Search Tools Documentation
================================

.. raw:: html

   <div class="agent-hero-section">
      <div class="hero-content">
         <h2>🔍 Powerful Search & Information Retrieval</h2>
         <p class="hero-description">
            Comprehensive search tools for web content, documentation, academic papers, and structured data. 
            Enable your agents to find accurate, up-to-date information from multiple sources.
         </p>
      </div>
   </div>

Overview
--------

The Search Tools collection provides agents with powerful capabilities to find and retrieve information from various sources:

- **Web Search**: Real-time web content retrieval
- **Academic Search**: Scientific papers and research
- **Documentation Search**: Technical documentation and APIs
- **Semantic Search**: Vector-based similarity search
- **Structured Data**: Database and knowledge graph queries

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>✨ Available Search Tools</h2>
      </div>
      <div class="games-showcase">
         <div class="game-card">
            <div class="game-header">
               <div class="game-emoji">🌐</div>
               <h3 class="game-title">WebSearchTool</h3>
               <div class="game-category">General Web</div>
            </div>
            <p class="game-description">
               Real-time web search with result ranking, snippet extraction, and source verification. Supports multiple search engines.
            </p>
            <div class="game-features">
               <span class="game-feature">Multi-engine support</span>
               <span class="game-feature">Result ranking</span>
               <span class="game-feature">Safe search</span>
               <span class="game-feature">Rate limiting</span>
            </div>
            <div class="game-stats">
               <div class="game-stat">
                  <span class="game-stat-value">< 2s</span>
                  <span class="game-stat-label">Response Time</span>
               </div>
               <div class="game-stat">
                  <span class="game-stat-value">95%</span>
                  <span class="game-stat-label">Accuracy</span>
               </div>
               <div class="game-stat">
                  <span class="game-stat-value">10+</span>
                  <span class="game-stat-label">Sources</span>
               </div>
            </div>
         </div>

         <div class="game-card">
            <div class="game-header">
               <div class="game-emoji">📚</div>
               <h3 class="game-title">WikipediaSearchTool</h3>
               <div class="game-category">Encyclopedia</div>
            </div>
            <p class="game-description">
               Search and retrieve Wikipedia articles with structured content extraction and cross-references.
            </p>
            <div class="game-features">
               <span class="game-feature">Full articles</span>
               <span class="game-feature">Summaries</span>
               <span class="game-feature">Categories</span>
               <span class="game-feature">Multi-language</span>
            </div>
            <div class="game-stats">
               <div class="game-stat">
                  <span class="game-stat-value">6M+</span>
                  <span class="game-stat-label">Articles</span>
               </div>
               <div class="game-stat">
                  <span class="game-stat-value">300+</span>
                  <span class="game-stat-label">Languages</span>
               </div>
               <div class="game-stat">
                  <span class="game-stat-value">< 1s</span>
                  <span class="game-stat-label">Response</span>
               </div>
            </div>
         </div>

         <div class="game-card">
            <div class="game-header">
               <div class="game-emoji">🎓</div>
               <h3 class="game-title">ArxivSearchTool</h3>
               <div class="game-category">Academic</div>
            </div>
            <p class="game-description">
               Search scientific papers from arXiv with abstract retrieval, citation extraction, and PDF access.
            </p>
            <div class="game-features">
               <span class="game-feature">2M+ papers</span>
               <span class="game-feature">Daily updates</span>
               <span class="game-feature">PDF retrieval</span>
               <span class="game-feature">Citation data</span>
            </div>
            <div class="game-stats">
               <div class="game-stat">
                  <span class="game-stat-value">2M+</span>
                  <span class="game-stat-label">Papers</span>
               </div>
               <div class="game-stat">
                  <span class="game-stat-value">8</span>
                  <span class="game-stat-label">Categories</span>
               </div>
               <div class="game-stat">
                  <span class="game-stat-value">Free</span>
                  <span class="game-stat-label">Access</span>
               </div>
            </div>
         </div>

         <div class="game-card">
            <div class="game-header">
               <div class="game-emoji">🧠</div>
               <h3 class="game-title">SemanticSearchTool</h3>
               <div class="game-category">Vector Search</div>
            </div>
            <p class="game-description">
               Advanced semantic search using embeddings for finding conceptually similar content across documents.
            </p>
            <div class="game-features">
               <span class="game-feature">Vector similarity</span>
               <span class="game-feature">Cross-lingual</span>
               <span class="game-feature">Reranking</span>
               <span class="game-feature">Hybrid search</span>
            </div>
            <div class="game-stats">
               <div class="game-stat">
                  <span class="game-stat-value">768D</span>
                  <span class="game-stat-label">Embeddings</span>
               </div>
               <div class="game-stat">
                  <span class="game-stat-value">< 100ms</span>
                  <span class="game-stat-label">Query Time</span>
               </div>
               <div class="game-stat">
                  <span class="game-stat-value">99%</span>
                  <span class="game-stat-label">Recall</span>
               </div>
            </div>
         </div>
      </div>
   </div>

Quick Start
-----------

.. raw:: html

   <div class="code-example-section">
      <h4>🚀 Basic Search Examples</h4>

.. code-block:: python

   from haive.tools.search import (
       WebSearchTool,
       WikipediaSearchTool,
       ArxivSearchTool,
       SemanticSearchTool
   )
   from haive.agents.react import ReactAgent
   from haive.core.engine.aug_llm import AugLLMConfig

   # 1. Web Search
   web_search = WebSearchTool(
       search_engine="google",  # or "bing", "duckduckgo"
       max_results=10,
       safe_search="moderate"
   )

   # Simple search
   results = web_search.invoke("latest AI developments 2025")
   for result in results:
       print(f"Title: {result['title']}")
       print(f"URL: {result['url']}")
       print(f"Snippet: {result['snippet']}\n")

   # 2. Wikipedia Search
   wiki_search = WikipediaSearchTool(
       lang="en",
       include_images=True,
       max_chars=5000
   )

   article = wiki_search.invoke("Transformer architecture AI")
   print(f"Title: {article['title']}")
   print(f"Summary: {article['summary'][:200]}...")
   print(f"Categories: {article['categories']}")

   # 3. Academic Search
   arxiv_search = ArxivSearchTool(
       max_results=5,
       sort_by="relevance",  # or "lastUpdatedDate", "submittedDate"
       include_pdf_url=True
   )

   papers = arxiv_search.invoke("attention is all you need")
   for paper in papers:
       print(f"Title: {paper['title']}")
       print(f"Authors: {', '.join(paper['authors'])}")
       print(f"Abstract: {paper['abstract'][:150]}...")
       print(f"PDF: {paper['pdf_url']}\n")

   # 4. Use in ReactAgent
   agent = ReactAgent(
       name="research_agent",
       engine=AugLLMConfig(),
       tools=[web_search, wiki_search, arxiv_search]
   )

   result = await agent.arun(
       "Find the latest research on quantum computing applications in cryptography"
   )

.. raw:: html

   </div>

Advanced Search Patterns
------------------------

.. raw:: html

   <div class="custom-section">
      <h3>🎯 Advanced Search Techniques</h3>

.. code-block:: python

   from haive.tools.search import WebSearchTool, SearchConfig
   from typing import List, Dict
   import asyncio

   # Advanced web search configuration
   search_config = SearchConfig(
       # Search parameters
       max_results=20,
       time_range="past_year",  # "past_day", "past_week", "past_month"
       language="en",
       country="US",
       safe_search="strict",
       
       # Result filtering
       include_domains=["arxiv.org", "nature.com", "ieee.org"],
       exclude_domains=["blogspot.com", "medium.com"],
       file_type="pdf",  # Search for PDFs only
       
       # Performance
       timeout=5.0,
       retry_count=3,
       cache_results=True
   )

   advanced_search = WebSearchTool(config=search_config)

   # Multi-query search with different strategies
   async def multi_strategy_search(queries: List[str]) -> Dict[str, List]:
       """Search with multiple strategies in parallel."""
       
       strategies = [
           {"time_range": "past_day", "sort": "date"},
           {"time_range": "past_year", "sort": "relevance"},
           {"file_type": "pdf", "sort": "relevance"}
       ]
       
       results = {}
       for query in queries:
           strategy_results = []
           
           # Search with each strategy
           tasks = []
           for strategy in strategies:
               tool = WebSearchTool(**strategy)
               tasks.append(tool.ainvoke(query))
           
           # Gather results
           all_results = await asyncio.gather(*tasks)
           
           # Deduplicate and rank
           seen_urls = set()
           unique_results = []
           for result_set in all_results:
               for result in result_set:
                   if result['url'] not in seen_urls:
                       seen_urls.add(result['url'])
                       unique_results.append(result)
           
           results[query] = unique_results[:10]
       
       return results

   # Semantic search with reranking
   class EnhancedSemanticSearch(SemanticSearchTool):
       async def search_and_rerank(
           self,
           query: str,
           documents: List[str],
           top_k: int = 10
       ) -> List[Dict]:
           """Search and rerank results based on relevance."""
           
           # Initial semantic search
           initial_results = await self.ainvoke(
               query,
               documents=documents,
               top_k=top_k * 3  # Get more for reranking
           )
           
           # Rerank using cross-encoder
           reranked = await self.rerank(
               query,
               initial_results,
               model="cross-encoder/ms-marco-MiniLM-L-12-v2"
           )
           
           return reranked[:top_k]

   # Federated search across multiple sources
   class FederatedSearchTool:
       def __init__(self, tools: List):
           self.tools = tools
       
       async def search_all(
           self,
           query: str,
           max_per_source: int = 5
       ) -> Dict[str, List]:
           """Search across all configured sources."""
           
           tasks = [
               tool.ainvoke(query, max_results=max_per_source)
               for tool in self.tools
           ]
           
           results = await asyncio.gather(*tasks, return_exceptions=True)
           
           # Organize by source
           federated_results = {}
           for tool, result in zip(self.tools, results):
               if isinstance(result, Exception):
                   federated_results[tool.name] = {"error": str(result)}
               else:
                   federated_results[tool.name] = result
           
           return federated_results

.. raw:: html

   </div>

Search Result Processing
------------------------

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>📊 Processing Search Results</h2>
      </div>

.. code-block:: python

   from haive.tools.search import WebSearchTool
   from haive.tools.search.processors import (
       ResultFilter,
       ResultRanker,
       ContentExtractor,
       SourceValidator
   )
   from typing import List, Dict
   import re

   # Result filtering
   class CustomResultFilter(ResultFilter):
       def filter(self, results: List[Dict]) -> List[Dict]:
           """Apply custom filtering logic."""
           filtered = []
           
           for result in results:
               # Check URL patterns
               if self.is_valid_source(result['url']):
                   # Check content quality
                   if self.has_quality_content(result):
                       # Check freshness
                       if self.is_recent(result):
                           filtered.append(result)
           
           return filtered
       
       def is_valid_source(self, url: str) -> bool:
           """Validate source credibility."""
           trusted_domains = [
               'edu', 'gov', 'org',
               'nature.com', 'science.org',
               'ieee.org', 'acm.org'
           ]
           return any(domain in url for domain in trusted_domains)
       
       def has_quality_content(self, result: Dict) -> bool:
           """Check content quality indicators."""
           snippet = result.get('snippet', '')
           
           # Check for citations/references
           has_citations = bool(re.search(r'\[\d+\]|\(\d{4}\)', snippet))
           
           # Check for technical terms
           tech_terms = ['algorithm', 'method', 'analysis', 'results']
           has_tech_terms = any(term in snippet.lower() for term in tech_terms)
           
           return has_citations or has_tech_terms

   # Content extraction from search results
   class EnhancedContentExtractor(ContentExtractor):
       async def extract_full_content(self, url: str) -> Dict:
           """Extract full content from URL."""
           import aiohttp
           from bs4 import BeautifulSoup
           
           async with aiohttp.ClientSession() as session:
               async with session.get(url) as response:
                   html = await response.text()
           
           soup = BeautifulSoup(html, 'html.parser')
           
           # Extract structured content
           content = {
               'title': soup.find('title').text if soup.find('title') else '',
               'headings': [h.text for h in soup.find_all(['h1', 'h2', 'h3'])],
               'paragraphs': [p.text for p in soup.find_all('p')],
               'links': [a.get('href') for a in soup.find_all('a', href=True)],
               'metadata': self.extract_metadata(soup)
           }
           
           return content
       
       def extract_metadata(self, soup) -> Dict:
           """Extract page metadata."""
           metadata = {}
           
           # Open Graph tags
           for tag in soup.find_all('meta', property=re.compile(r'^og:')):
               key = tag.get('property').replace('og:', '')
               metadata[key] = tag.get('content')
           
           # Other meta tags
           for tag in soup.find_all('meta', attrs={'name': True}):
               metadata[tag['name']] = tag.get('content', '')
           
           return metadata

   # Intelligent result ranking
   class IntelligentRanker(ResultRanker):
       def __init__(self, weights: Dict[str, float]):
           self.weights = weights
       
       def rank(self, results: List[Dict], query: str) -> List[Dict]:
           """Rank results based on multiple factors."""
           scored_results = []
           
           for result in results:
               score = 0.0
               
               # Relevance score
               score += self.weights['relevance'] * self.calculate_relevance(
                   query, result
               )
               
               # Authority score
               score += self.weights['authority'] * self.calculate_authority(
                   result
               )
               
               # Freshness score
               score += self.weights['freshness'] * self.calculate_freshness(
                   result
               )
               
               # Engagement score
               score += self.weights['engagement'] * self.calculate_engagement(
                   result
               )
               
               result['ranking_score'] = score
               scored_results.append(result)
           
           # Sort by score
           return sorted(
               scored_results,
               key=lambda x: x['ranking_score'],
               reverse=True
           )

.. raw:: html

   </div>

Search Tool Combinations
------------------------

.. raw:: html

   <div class="api-grid">
      <div class="api-section">
         <h4>🔗 Chain Searches</h4>

.. code-block:: python

   # Progressive search refinement
   async def progressive_search(
       initial_query: str,
       depth: int = 3
   ):
       web = WebSearchTool()
       wiki = WikipediaSearchTool()
       
       # Start broad
       results = await web.ainvoke(initial_query)
       
       # Extract entities
       entities = extract_entities(results)
       
       # Deep dive on entities
       for entity in entities[:depth]:
           wiki_data = await wiki.ainvoke(entity)
           # Process and integrate

.. raw:: html

      </div>
      
      <div class="api-section">
         <h4>🌐 Cross-Reference</h4>

.. code-block:: python

   # Verify information across sources
   async def verify_facts(claim: str):
       sources = [
           WebSearchTool(),
           WikipediaSearchTool(),
           ArxivSearchTool()
       ]
       
       evidence = []
       for source in sources:
           result = await source.ainvoke(claim)
           evidence.append({
               'source': source.name,
               'support': analyze_support(result, claim)
           })
       
       return aggregate_evidence(evidence)

.. raw:: html

      </div>
   </div>

Performance Optimization
------------------------

.. raw:: html

   <div class="custom-section">
      <h3>⚡ Search Performance Tips</h3>

.. code-block:: python

   from haive.tools.search import WebSearchTool
   from functools import lru_cache
   import asyncio
   import aioredis

   # 1. Caching search results
   class CachedSearchTool(WebSearchTool):
       def __init__(self, cache_ttl: int = 3600, **kwargs):
           super().__init__(**kwargs)
           self.cache_ttl = cache_ttl
           self.redis = None
       
       async def connect_cache(self):
           self.redis = await aioredis.create_redis_pool(
               'redis://localhost'
           )
       
       async def ainvoke(self, query: str, **kwargs):
           # Check cache first
           cache_key = f"search:{query}:{hash(str(kwargs))}"
           cached = await self.redis.get(cache_key)
           
           if cached:
               return json.loads(cached)
           
           # Perform search
           results = await super().ainvoke(query, **kwargs)
           
           # Cache results
           await self.redis.setex(
               cache_key,
               self.cache_ttl,
               json.dumps(results)
           )
           
           return results

   # 2. Parallel search execution
   async def parallel_search(
       queries: List[str],
       tool: WebSearchTool,
       max_concurrent: int = 5
   ) -> Dict[str, List]:
       """Execute searches in parallel with concurrency limit."""
       
       semaphore = asyncio.Semaphore(max_concurrent)
       
       async def search_with_limit(query: str):
           async with semaphore:
               return await tool.ainvoke(query)
       
       tasks = [search_with_limit(q) for q in queries]
       results = await asyncio.gather(*tasks)
       
       return dict(zip(queries, results))

   # 3. Streaming search results
   class StreamingSearchTool(WebSearchTool):
       async def astream(
           self,
           query: str,
           chunk_size: int = 5
       ):
           """Stream results as they arrive."""
           
           # Start search
           search_task = asyncio.create_task(
               self._perform_search(query)
           )
           
           # Yield results in chunks
           results = []
           while True:
               if search_task.done():
                   all_results = await search_task
                   # Yield remaining results
                   for i in range(0, len(all_results), chunk_size):
                       yield all_results[i:i + chunk_size]
                   break
               
               # Check for partial results
               await asyncio.sleep(0.1)

   # 4. Search query optimization
   class OptimizedSearchTool(WebSearchTool):
       def optimize_query(self, query: str) -> str:
           """Optimize search query for better results."""
           
           # Remove stop words
           stop_words = {'the', 'a', 'an', 'and', 'or', 'but'}
           words = query.lower().split()
           words = [w for w in words if w not in stop_words]
           
           # Add search operators
           if len(words) > 3:
               # Use phrase search for multi-word queries
               return f'"{" ".join(words)}"'
           
           return ' '.join(words)

.. raw:: html

   </div>

API Reference
-------------

.. automodule:: haive.tools.search
   :members:
   :show-inheritance:

.. autoclass:: haive.tools.search.WebSearchTool
   :members:
   :show-inheritance:

.. autoclass:: haive.tools.search.WikipediaSearchTool
   :members:
   :show-inheritance:

.. autoclass:: haive.tools.search.ArxivSearchTool
   :members:
   :show-inheritance:

.. autoclass:: haive.tools.search.SemanticSearchTool
   :members:
   :show-inheritance:

Next Steps
----------

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>🚀 Explore More Tools</h2>
      </div>
      <div class="agent-showcase">
         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">💻</div>
               <div>
                  <h3 class="agent-title">Code Tools</h3>
                  <p class="agent-subtitle">Code execution and analysis</p>
               </div>
            </div>
            <p class="agent-description">
               Execute code, analyze repositories, and generate code with specialized development tools.
            </p>
            <a href="../code/index.html" class="agent-link">Explore Code Tools</a>
         </div>

         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">📊</div>
               <div>
                  <h3 class="agent-title">Data Tools</h3>
                  <p class="agent-subtitle">Data processing and analysis</p>
               </div>
            </div>
            <p class="agent-description">
               Process CSV, JSON, and other data formats with powerful analysis and visualization tools.
            </p>
            <a href="../data/index.html" class="agent-link">Explore Data Tools</a>
         </div>

         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">🧮</div>
               <div>
                  <h3 class="agent-title">Math Tools</h3>
                  <p class="agent-subtitle">Mathematical computation</p>
               </div>
            </div>
            <p class="agent-description">
               Perform complex calculations, symbolic math, and statistical analysis.
            </p>
            <a href="../math/index.html" class="agent-link">Explore Math Tools</a>
         </div>
      </div>
   </div>

.. seealso::

   - :doc:`../../agents/react/index` - Using tools with ReactAgent
   - :doc:`../../guides/tool_composition` - Combining multiple tools
   - :doc:`../index` - Back to tools overview