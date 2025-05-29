"""
RAG (Retrieval Augmented Generation) Service for UK Legal Data
"""

import requests
import json
from typing import List, Dict, Any
import os
from datetime import datetime
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

class UKLegalRAGService:
    """RAG service for UK legal data collection and retrieval"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self._init_pinecone()
    
    def _init_pinecone(self):
        """Initialize Pinecone vector database"""
        try:
            pinecone.init(
                api_key=os.getenv("PINECONE_API_KEY"),
                environment=os.getenv("PINECONE_ENVIRONMENT")
            )
            
            # Create index if it doesn't exist
            index_name = "uk-legal-rag"
            if index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=index_name,
                    dimension=1536,  # OpenAI embedding dimension
                    metric="cosine"
                )
            
            self.vector_store = Pinecone.from_existing_index(
                index_name=index_name,
                embedding=self.embeddings
            )
        except Exception as e:
            print(f"Pinecone initialization failed: {e}")
            self.vector_store = None
    
    def collect_uk_legal_data(self):
        """Collect and index UK legal data from various sources"""
        
        print("🔍 Collecting UK Legal Data for RAG...")
        
        # 1. Collect Government Guidance
        self._collect_gov_uk_data()
        
        # 2. Collect Case Law
        self._collect_case_law()
        
        # 3. Collect Legislation
        self._collect_legislation()
        
        # 4. Collect Property Data
        self._collect_property_data()
        
        # 5. Collect Tax Information
        self._collect_tax_data()
        
        print("✅ RAG Data Collection Complete!")
    
    def _collect_gov_uk_data(self):
        """Collect UK Government guidance and forms"""
        
        # Probate guidance URLs
        probate_urls = [
            "https://www.gov.uk/applying-for-probate",
            "https://www.gov.uk/inherits-someone-dies-without-will",
            "https://www.gov.uk/inheritance-tax",
            "https://www.gov.uk/valuing-estate-of-someone-who-died",
            "https://www.gov.uk/probate-application"
        ]
        
        # Divorce guidance URLs
        divorce_urls = [
            "https://www.gov.uk/divorce",
            "https://www.gov.uk/money-property-when-relationship-ends",
            "https://www.gov.uk/looking-after-children-divorce",
            "https://www.gov.uk/court-fees-what-they-are"
        ]
        
        all_urls = probate_urls + divorce_urls
        
        for url in all_urls:
            try:
                # In a real implementation, you'd scrape these pages
                # For now, we'll create sample data
                content = self._fetch_gov_content(url)
                if content:
                    self._index_content(content, "government_guidance", url)
            except Exception as e:
                print(f"Failed to collect from {url}: {e}")
    
    def _collect_case_law(self):
        """Collect UK case law from BAILII"""
        
        # Sample case law topics for probate/divorce
        case_topics = [
            "probate disputes",
            "inheritance act claims", 
            "divorce financial remedies",
            "property division",
            "inheritance tax",
            "estate administration"
        ]
        
        for topic in case_topics:
            try:
                # In real implementation, query BAILII API
                cases = self._fetch_bailii_cases(topic)
                for case in cases:
                    self._index_content(case, "case_law", topic)
            except Exception as e:
                print(f"Failed to collect case law for {topic}: {e}")
    
    def _collect_legislation(self):
        """Collect relevant UK legislation"""
        
        legislation_acts = [
            {
                "title": "Inheritance (Provision for Family and Dependants) Act 1975",
                "content": "Key provisions for family claims against estates...",
                "relevance": "probate"
            },
            {
                "title": "Matrimonial Causes Act 1973", 
                "content": "Grounds for divorce and financial provisions...",
                "relevance": "divorce"
            },
            {
                "title": "Administration of Estates Act 1925",
                "content": "Rules for estate administration and distribution...",
                "relevance": "probate"
            },
            {
                "title": "Inheritance Tax Act 1984",
                "content": "Inheritance tax rules and exemptions...",
                "relevance": "tax"
            }
        ]
        
        for act in legislation_acts:
            self._index_content(act, "legislation", act["relevance"])
    
    def _collect_property_data(self):
        """Collect property market data"""
        
        # Sample property data structure
        property_data = {
            "london_prices": "Average property prices in London by postcode...",
            "manchester_prices": "Average property prices in Manchester...",
            "valuation_methods": "RICS approved valuation methodologies...",
            "market_trends": "Current UK property market trends..."
        }
        
        for key, content in property_data.items():
            self._index_content({"content": content}, "property_data", key)
    
    def _collect_tax_data(self):
        """Collect HMRC tax guidance"""
        
        tax_guidance = [
            {
                "title": "Inheritance Tax Rates 2024/25",
                "content": "Current IHT rates: 40% above £325,000 threshold...",
                "category": "inheritance_tax"
            },
            {
                "title": "Residence Nil Rate Band",
                "content": "Additional £175,000 allowance for family homes...",
                "category": "inheritance_tax"
            },
            {
                "title": "Capital Gains Tax on Property",
                "content": "CGT implications for property transfers...",
                "category": "capital_gains"
            }
        ]
        
        for guidance in tax_guidance:
            self._index_content(guidance, "tax_guidance", guidance["category"])
    
    def _fetch_gov_content(self, url: str) -> Dict[str, Any]:
        """Fetch content from GOV.UK (placeholder)"""
        # In real implementation, scrape the actual content
        return {
            "url": url,
            "content": f"Government guidance content from {url}",
            "last_updated": datetime.now().isoformat(),
            "source": "gov.uk"
        }
    
    def _fetch_bailii_cases(self, topic: str) -> List[Dict[str, Any]]:
        """Fetch case law from BAILII (placeholder)"""
        # In real implementation, query BAILII database
        return [
            {
                "case_name": f"Sample case for {topic}",
                "citation": "[2024] EWHC 123 (Ch)",
                "content": f"Legal precedent content for {topic}",
                "court": "High Court",
                "date": "2024-01-15"
            }
        ]
    
    def _index_content(self, content: Dict[str, Any], content_type: str, category: str):
        """Index content in vector database"""
        if not self.vector_store:
            return
        
        try:
            # Convert content to text
            text = json.dumps(content) if isinstance(content, dict) else str(content)
            
            # Split into chunks
            chunks = self.text_splitter.split_text(text)
            
            # Create metadata
            metadata = {
                "content_type": content_type,
                "category": category,
                "indexed_at": datetime.now().isoformat()
            }
            
            # Add to vector store
            self.vector_store.add_texts(
                texts=chunks,
                metadatas=[metadata] * len(chunks)
            )
            
        except Exception as e:
            print(f"Failed to index content: {e}")
    
    def search_legal_precedents(self, query: str, content_type: str = None, k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant legal precedents"""
        if not self.vector_store:
            return []
        
        try:
            # Build filter
            filter_dict = {}
            if content_type:
                filter_dict["content_type"] = content_type
            
            # Search
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter_dict if filter_dict else None
            )
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance_score": score,
                    "source": doc.metadata.get("content_type", "unknown")
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"Search failed: {e}")
            return []
    
    def get_contextual_information(self, case_type: str, query: str) -> Dict[str, Any]:
        """Get contextual legal information for a case"""
        
        # Search different content types
        legislation = self.search_legal_precedents(query, "legislation", k=3)
        case_law = self.search_legal_precedents(query, "case_law", k=3)
        guidance = self.search_legal_precedents(query, "government_guidance", k=3)
        
        return {
            "query": query,
            "case_type": case_type,
            "legislation": legislation,
            "case_law": case_law,
            "government_guidance": guidance,
            "total_sources": len(legislation) + len(case_law) + len(guidance)
        }
        
        """
Optional RAG Service - Only loads if Pinecone is available
"""

import os
from typing import Dict, List, Any
from datetime import datetime

class UKLegalRAGService:
    """Simplified RAG service for UK legal data"""
    
    def __init__(self):
        self.available = False
        try:
            # Only initialize if Pinecone is available
            import pinecone
            from langchain.embeddings import OpenAIEmbeddings
            
            if os.getenv("PINECONE_API_KEY"):
                self.available = True
                print("✅ RAG Service initialized")
            else:
                print("⚠️ Pinecone API key not found")
        except ImportError:
            print("⚠️ Pinecone not installed, RAG service disabled")
    
    def get_contextual_information(self, case_type: str, query: str) -> Dict[str, Any]:
        """Get contextual legal information"""
        if not self.available:
            return {
                "legislation": [],
                "case_law": [],
                "government_guidance": [],
                "total_sources": 0
            }
        
        # Placeholder implementation
        return {
            "legislation": [
                {"content": "Sample legislation content for " + query}
            ],
            "case_law": [
                {"content": "Sample case law content for " + query}
            ],
            "government_guidance": [
                {"content": "Sample government guidance for " + query}
            ],
            "total_sources": 3
        }