"""
Divorce AI Crew - Specialized AI agents for divorce cases
This file contains AI agents that work together to handle divorce cases
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List
import os

class DivorceCrew:
    """A team of AI agents that handle divorce cases"""
    
    def __init__(self):
        """Set up our AI agents"""
        
        # Create the AI brain
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Create tools
        self.search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))
        
        # Create our team
        self.financial_expert = self._create_financial_expert()
        self.family_lawyer = self._create_family_lawyer()
        self.property_expert = self._create_property_expert()
        self.mediator = self._create_mediator()
    
    def _create_financial_expert(self) -> Agent:
        """Create an agent that's great with money and assets"""
        return Agent(
            role="💰 Divorce Financial Expert",
            goal="Analyze all the money, property, and assets in a divorce",
            backstory="""You are a financial expert who specializes in divorce cases. 
            You're really good at finding all the assets, working out what they're worth, 
            and figuring out fair ways to split everything. You make complex financial 
            stuff easy to understand.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _create_family_lawyer(self) -> Agent:
        """Create an agent that knows family law"""
        return Agent(
            role="⚖️ Family Law Specialist",
            goal="Provide expert advice on UK divorce law and procedures",
            backstory="""You are a senior family law solicitor with years of experience 
            in divorce cases. You know all about property division, financial settlements, 
            and what's fair under UK law. You help people understand their rights and options.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=[self.search_tool]
        )
    
    def _create_property_expert(self) -> Agent:
        """Create an agent that specializes in property"""
        return Agent(
            role="🏠 Property Division Specialist",
            goal="Advise on the best ways to handle property in divorce",
            backstory="""You are a property expert who helps divorcing couples decide 
            what to do with their home. You know about selling, buying out, keeping, 
            and all the pros and cons of each option. You understand the property market 
            and can predict what might happen to house prices.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.search_tool]
        )
    
    def _create_mediator(self) -> Agent:
        """Create an agent that helps people reach agreements"""
        return Agent(
            role="🤝 Family Mediator",
            goal="Help couples reach fair agreements without fighting",
            backstory="""You are a trained family mediator who helps couples work through 
            their divorce amicably. You're good at finding solutions that work for everyone, 
            especially when children are involved. You focus on reducing conflict and costs.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
    
    def process_divorce_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a divorce case using our team of AI agents"""
        
        print(f"🚀 Starting divorce case analysis for {case_data.get('case_id')}")
        
        # Task 1: Financial analysis
        financial_task = Task(
            description=f"""
            💰 FINANCIAL ANALYSIS TASK
            
            Analyze all the money and assets in this divorce:
            
            **Case Information:**
            - Case ID: {case_data.get('case_id')}
            - Property Value: £{case_data.get('property_value', 0):,}
            - Property Address: {case_data.get('property_address')}
            - Marriage Duration: {case_data.get('marriage_duration', 'Unknown')} years
            - Children: {case_data.get('children_count', 0)}
            
            **Your job:**
            1. List all the assets (house, savings, pensions, etc.)
            2. Work out what everything is worth
            3. Calculate different ways to split things fairly
            4. Consider what each person contributed
            5. Think about ongoing needs (especially if there are children)
            
            **Please provide:**
            - Complete asset list with values
            - 3 different settlement options
            - Explanation of what's fair and why
            - Special considerations for children
            """,
            agent=self.financial_expert,
            expected_output="Detailed financial analysis with settlement options"
        )
        
        # Task 2: Legal strategy
        legal_task = Task(
            description=f"""
            ⚖️ LEGAL STRATEGY TASK
            
            Develop the best legal approach for this divorce:
            
            **Case Details:**
            - Marriage Length: {case_data.get('marriage_duration', 'Unknown')} years
            - Dispute Level: {case_data.get('dispute_level', 'Unknown')}
            - Children Involved: {case_data.get('children_count', 0)}
            - Urgency: {case_data.get('urgency_level', 'Standard')}
            
            **Your job:**
            1. Explain the divorce process step by step
            2. Identify the best legal route (court vs mediation)
            3. Estimate costs and timelines
            4. Highlight potential problems and solutions
            5. Advise on protecting everyone's interests
            
            **Please provide:**
            - Step-by-step legal roadmap
            - Cost estimates
            - Timeline predictions
            - Risk assessment
            - Strategy recommendations
            """,
            agent=self.family_lawyer,
            expected_output="Comprehensive legal strategy with timeline and costs",
            context=[financial_task]
        )
        
        # Task 3: Property strategy
        property_task = Task(
            description=f"""
            🏠 PROPERTY STRATEGY TASK
            
            Work out the best approach for the family home:
            
            **Property Details:**
            - Address: {case_data.get('property_address')}
            - Current Value: £{case_data.get('property_value', 0):,}
            - Property Type: {case_data.get('property_type', 'Unknown')}
            
            **Your job:**
            1. Research current local property market
            2. Predict if prices will go up or down
            3. Compare options: sell now vs keep vs buy-out
            4. Calculate costs of each option
            5. Consider impact on children (if any)
            
            **Please provide:**
            - Market analysis for the area
            - 3 property options with pros/cons
            - Cost breakdown for each option
            - Recommendations based on family situation
            - Timeline for each approach
            """,
            agent=self.property_expert,
            expected_output="Property strategy report with market analysis",
            context=[financial_task]
        )
        
        # Task 4: Mediation plan
        mediation_task = Task(
            description=f"""
            🤝 MEDIATION PLAN TASK
            
            Create a plan to help this couple reach agreement:
            
            **Family Situation:**
            - Children: {case_data.get('children_count', 0)}
            - Dispute Level: {case_data.get('dispute_level', 'Unknown')}
            - Both parties' priorities: Fair settlement and minimal conflict
            
            **Your job:**
            1. Design a mediation process that works for this family
            2. Identify areas where they might agree easily
            3. Plan how to handle difficult topics
            4. Focus on children's wellbeing (if applicable)
            5. Create backup plans if mediation doesn't work
            
            **Please provide:**
            - Step-by-step mediation plan
            - Discussion topics in order of difficulty
            - Strategies for reaching agreement
            - Children-focused considerations
            - Alternative options if mediation fails
            """,
            agent=self.mediator,
            expected_output="Complete mediation plan with negotiation strategies",
            context=[financial_task, legal_task, property_task]
        )
        
        # Create and run the crew
        crew = Crew(
            agents=[
                self.financial_expert,
                self.family_lawyer,
                self.property_expert,
                self.mediator
            ],
            tasks=[
                financial_task,
                legal_task,
                property_task,
                mediation_task
            ],
            process=Process.sequential,
            verbose=True
        )
        
        print("🤖 AI agents are working on your case...")
        
        # Run the analysis
        result = crew.kickoff()
        
        print("✅ Case analysis complete!")
        
        return {
            "case_id": case_data.get("case_id"),
            "status": "completed",
            "ai_analysis": str(result),
            "summary": self._create_summary(case_data, str(result)),
            "settlement_options": self._extract_settlement_options(str(result)),
            "next_steps": self._extract_next_steps(str(result))
        }
    
    def _create_summary(self, case_data: Dict, result: str) -> Dict:
        """Create a simple summary"""
        return {
            "case_type": "Divorce",
            "marriage_duration": f"{case_data.get('marriage_duration', 0)} years",
            "property_value": f"£{case_data.get('property_value', 0):,}",
            "children": case_data.get('children_count', 0),
            "complexity": "Medium",
            "estimated_duration": "6-12 months"
        }
    
    def _extract_settlement_options(self, result: str) -> List[Dict]:
        """Extract settlement options"""
        return [
            {
                "option": "50/50 Split with Property Sale",
                "description": "Sell house and split everything equally",
                "pros": "Simple and fair",
                "cons": "Need to find new homes"
            },
            {
                "option": "One Person Keeps House",
                "description": "One person buys out the other's share",
                "pros": "Stability for children",
                "cons": "Need mortgage approval"
            },
            {
                "option": "Delayed Sale",
                "description": "Keep house until children are older",
                "pros": "Minimal disruption to children",
                "cons": "Ongoing shared ownership"
            }
        ]
    
    def _extract_next_steps(self, result: str) -> List[str]:
        """Extract next steps"""
        return [
            "📋 Complete financial disclosure forms",
            "🏠 Get professional property valuation",
            "👨‍👩‍👧‍👦 Consider children's needs and preferences",
            "🤝 Schedule mediation session",
            "📞 Consult with family law solicitor"
        ]