from typing import List, Optional
from pydantic import BaseModel  

class JournalismReviewState(BaseModel):
    current_query: str
    article_text: str
    chunks: List[str]
    actions: List[str]
    summary_result: Optional[str]
    # need to check
    fact_check_result: Optional[List[FactCheckResult]]
    tone_analysis_result: Optional[str]
    quote_extraction_result: Optional[str]
    grammar_and_bias_review_result: Optional[str]
    review_result: Optional[str]