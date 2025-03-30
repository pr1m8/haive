class CoreAPIWrapper(BaseModel):
    """Simple wrapper around the CORE API."""
    base_url: ClassVar[str] = "https://api.core.ac.uk/v3"
    api_key: ClassVar[str] = os.environ["CORE_API_KEY"]

    top_k_results: int = Field(description = "Top k results obtained by running a query on Core", default = 1)

    def _get_search_response(self, query: str) -> dict:
        http = urllib3.PoolManager()

        # Retry mechanism to handle transient errors
        max_retries = 5    
        for attempt in range(max_retries):
            response = http.request(
                'GET',
                f"{self.base_url}/search/outputs", 
                headers={"Authorization": f"Bearer {self.api_key}"}, 
                fields={"q": query, "limit": self.top_k_results}
            )
            if 200 <= response.status < 300:
                return response.json()
            elif attempt < max_retries - 1:
                time.sleep(2 ** (attempt + 2))
            else:
                raise Exception(f"Got non 2xx response from CORE API: {response.status} {response.data}")

    def search(self, query: str) -> str:
        response = self._get_search_response(query)
        results = response.get("results", [])
        if not results:
            return "No relevant results were found"

        # Format the results in a string
        docs = []
        for result in results:
            published_date_str = result.get('publishedDate') or result.get('yearPublished', '')
            authors_str = ' and '.join([item['name'] for item in result.get('authors', [])])
            docs.append((
                f"* ID: {result.get('id', '')},\n"
                f"* Title: {result.get('title', '')},\n"
                f"* Published Date: {published_date_str},\n"
                f"* Authors: {authors_str},\n"
                f"* Abstract: {result.get('abstract', '')},\n"
                f"* Paper URLs: {result.get('sourceFulltextUrls') or result.get('downloadUrl', '')}"
            ))
        return "\n-----\n".join(docs)

class SearchPapersInput(BaseModel):
    """Input object to search papers with the CORE API."""
    query: str = Field(description="The query to search for on the selected archive.")
    max_papers: int = Field(description="The maximum number of papers to return. It's default to 1, but you can increase it up to 10 in case you need to perform a more comprehensive search.", default=1, ge=1, le=10)

class DecisionMakingOutput(BaseModel):
    """Output object of the decision making node."""
    requires_research: bool = Field(description="Whether the user query requires research or not.")
    answer: Optional[str] = Field(default=None, description="The answer to the user query. It should be None if the user query requires research, otherwise it should be a direct answer to the user query.")

class JudgeOutput(BaseModel):
    """Output object of the judge node."""
    is_good_answer: bool = Field(description="Whether the answer is good or not.")
    feedback: Optional[str] = Field(default=None, description="Detailed feedback about why the answer is not good. It should be None if the answer is good.")
