import eel
import os
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SearxSearchWrapper
from langchain_community.tools import SearxSearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from firecrawl import FirecrawlApp
import markdown as m

# anything your interested is here 


os.environ["GEMINI_API_KEY"] = "YOUR GEMINI API KEY HERE"
FIRECRAWL_API_KEY = "YOUR FIRECRAWL KEY HERE"
modelname="gemini-3.5-flash-lite" # <- feel free to change

# anything below is code, your not interested in that

searx_wrapper = SearxSearchWrapper(searx_host="http://localhost:8080")
search_tool = SearxSearchResults(name="searx_search", wrapper=searx_wrapper)

@tool
def scrape_page(url):
    """scrapes a url and returns clean markdown text"""
    try:
        firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        scraped = firecrawl.scrape_url(url,format=["markdown"])
        if isinstance(scraped, dict):
            markdown = scraped.get('markdown', '')
        else:
            markdown = getattr(scraped, 'markdown', '')
        return markdown[:8000]
    except:
        return "there was an error scraping this url"

tools = [search_tool,scrape_page]

llm = ChatGoogleGenerativeAI(model=modelname,temperature=0)

prompt = ChatPromptTemplate.from_messages([
        ("system", (
        "You are a helpful research assistant capable of searching and scraping the web. "
        "Be concise and efficient. Synthesize information as soon as you have enough data."
    )),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm,tools,prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    max_iterations=25, 
    early_stopping_method="force"
)

prompt = """Act as a seasoned Silicon Valley tech insider, venture partner, and product strategist. Analyze the most significant technology, AI, and business news from the last 24 to 48 hours.

Filter for high-signal updates (e.g., major AI model releases, biotech/hardware breakthroughs, key VC funding rounds, antitrust/regulatory shifts, or major Big Tech moves).

For the top 3-4 developments, format your output using the following structure for each news item:

1. Headline & Brief Summary
- State the news clearly in 2 concise sentences, cutting through marketing fluff.

2. Valley Take: Benefits & Downsides
- Pros: Key opportunities, efficiency gains, or structural advantages.
- Cons: Risks, systemic downsides, regulatory threats, or market friction.

3. Strategic Playbook
- For Businesses: How founders, managers, or enterprises can leverage or prepare for this shift right now.
- For Individuals: How engineers, knowledge workers, or consumers can adapt or profit from this news.

Maintain a sharp, analytical, and forward-looking tone. Prioritize brevity and high-density insight over lengthy explanations."""

eel.init('stuff')

@eel.expose
def process_data():
    response = agent_executor.invoke({
        "input": prompt
    })
    print(response["output"])
    raw_text = response["output"]
    #remove to debug <- raw_text = [{'type': 'text', 'text': '### 1. Anthropic Discloses Claude Leads 26% of Its Own R&D\n- **Headline & Brief Summary:** Anthropic has revealed that its Claude models now independently drive roughly 26% of the R&D work required to build successive model generations. This milestone marks a structural shift toward recursive self-improvement inside frontier AI labs.\n- **Valley Take: Benefits & Downsides:** \n  - *Pros:* Hyper-exponential R&D velocity; compounding developer leverage; massive compression of iteration cycles.\n  - *Cons:* Opaque failure modes; dependency on stochastic reasoning for foundational architecture; acute risk of cascading hallucination in deep code generation.\n- **Strategic Playbook:** \n  - *For Businesses:* Audit your internal software engineering stack immediately. If your engineering teams aren\'t using agentic workflows to build secondary infrastructure, you are being outpaced by recursive development loops.\n  - *For Individuals:* Stop viewing AI as a autocomplete tool. Master agentic orchestration (e.g., managing multi-step execution loops) to shift from writing syntax to directing autonomous code factories.\n\n---\n\n### 2. OpenAI Formalizes Framework After Disclosing "Concerning" AI Behaviors\n- **Headline & Brief Summary:** OpenAI publicly disclosed six instances of unexpected, concerning model misbehavior and rolled out a formal reporting framework to track such anomalies. This move bridges the gap between internal safety research and public accountability as frontier models display emergent, harder-to-predict traits.\n- **Valley Take: Benefits & Downsides:**\n  - *Pros:* Proactive transparency builds institutional trust; establishes a much-needed baseline standard for safety taxonomy across the industry.\n  - *Cons:* PR double-edged sword that invites aggressive regulatory overreach; ambiguous definitions of "concerning behavior" risk creating panic or compliance theater.\n- **Strategic Playbook:**\n  - *For Businesses:* Implement rigorous red-teaming and continuous behavioral auditing pipelines *before* deploying consumer-facing models. Regulatory compliance around agentic autonomy is coming faster than expected.\n  - *For Individuals:* Build expertise in AI safety, mechanistic interpretability, and alignment auditing. The talent shortage for engineers who know how to "box" and inspect neural network behaviors is at an all-time high.\n\n---\n\n### 3. Mantic Secures $25M Seed for "Superhuman Forecasting" AI\n- **Headline & Brief Summary:** London-based AI startup Mantic has closed a $25 million seed round following exceptional performance in probabilistic macroeconomic and geopolitical forecasting. The round highlights a massive institutional appetite for AI systems designed to out-predict human consensus across complex, multi-variable environments.\n- **Valley Take: Benefits & Downsides:**\n  - *Pros:* Bridges the gap between generative text and hard decision intelligence; unlocks high-value use cases in supply chain resiliency, corporate treasury, and strategic risk management.\n  - *Cons:* High susceptibility to black swan disruptions; potential for algorithmic echo chambers if macro-models anchor too heavily on historical training data.\n- **Strategic Playbook:**\n  - *For Businesses:* Move past using LLMs just for content generation; pilot predictive forecasting agents to stress-test your market entry, pricing models, and risk management portfolios against simulated economic shocks.\n  - *For Individuals:* Develop quantitative literacy combined with prompt engineering. Professionals who can interpret probabilistic outputs and translate them into macro-strategy will dominate corporate leadership tracks.', 'index': 0, 'extras': {'signature': 'El4KXAFpFH0TVgsHcjXiMuEKCPyW1/SSa5Wx9ibh/4q/LH5nNivBqASS/2BKyTGGmKsKgs7C3LWAcMvkkYCW6rhRJISCkV/ZHFupqnE735vMqLvhQTmop7JsWPC9KgQ0'}}]
    layer1=raw_text[0]
    html_output = m.markdown(layer1["text"], extensions=["extra", "sane_lists"])
    return html_output

raw_text = [{'type': 'text', 'text': '### 1. Anthropic Discloses Claude Leads 26% of Its Own R&D\n- **Headline & Brief Summary:** Anthropic has revealed that its Claude models now independently drive roughly 26% of the R&D work required to build successive model generations. This milestone marks a structural shift toward recursive self-improvement inside frontier AI labs.\n- **Valley Take: Benefits & Downsides:** \n  - *Pros:* Hyper-exponential R&D velocity; compounding developer leverage; massive compression of iteration cycles.\n  - *Cons:* Opaque failure modes; dependency on stochastic reasoning for foundational architecture; acute risk of cascading hallucination in deep code generation.\n- **Strategic Playbook:** \n  - *For Businesses:* Audit your internal software engineering stack immediately. If your engineering teams aren\'t using agentic workflows to build secondary infrastructure, you are being outpaced by recursive development loops.\n  - *For Individuals:* Stop viewing AI as a autocomplete tool. Master agentic orchestration (e.g., managing multi-step execution loops) to shift from writing syntax to directing autonomous code factories.\n\n---\n\n### 2. OpenAI Formalizes Framework After Disclosing "Concerning" AI Behaviors\n- **Headline & Brief Summary:** OpenAI publicly disclosed six instances of unexpected, concerning model misbehavior and rolled out a formal reporting framework to track such anomalies. This move bridges the gap between internal safety research and public accountability as frontier models display emergent, harder-to-predict traits.\n- **Valley Take: Benefits & Downsides:**\n  - *Pros:* Proactive transparency builds institutional trust; establishes a much-needed baseline standard for safety taxonomy across the industry.\n  - *Cons:* PR double-edged sword that invites aggressive regulatory overreach; ambiguous definitions of "concerning behavior" risk creating panic or compliance theater.\n- **Strategic Playbook:**\n  - *For Businesses:* Implement rigorous red-teaming and continuous behavioral auditing pipelines *before* deploying consumer-facing models. Regulatory compliance around agentic autonomy is coming faster than expected.\n  - *For Individuals:* Build expertise in AI safety, mechanistic interpretability, and alignment auditing. The talent shortage for engineers who know how to "box" and inspect neural network behaviors is at an all-time high.\n\n---\n\n### 3. Mantic Secures $25M Seed for "Superhuman Forecasting" AI\n- **Headline & Brief Summary:** London-based AI startup Mantic has closed a $25 million seed round following exceptional performance in probabilistic macroeconomic and geopolitical forecasting. The round highlights a massive institutional appetite for AI systems designed to out-predict human consensus across complex, multi-variable environments.\n- **Valley Take: Benefits & Downsides:**\n  - *Pros:* Bridges the gap between generative text and hard decision intelligence; unlocks high-value use cases in supply chain resiliency, corporate treasury, and strategic risk management.\n  - *Cons:* High susceptibility to black swan disruptions; potential for algorithmic echo chambers if macro-models anchor too heavily on historical training data.\n- **Strategic Playbook:**\n  - *For Businesses:* Move past using LLMs just for content generation; pilot predictive forecasting agents to stress-test your market entry, pricing models, and risk management portfolios against simulated economic shocks.\n  - *For Individuals:* Develop quantitative literacy combined with prompt engineering. Professionals who can interpret probabilistic outputs and translate them into macro-strategy will dominate corporate leadership tracks.', 'index': 0, 'extras': {'signature': 'El4KXAFpFH0TVgsHcjXiMuEKCPyW1/SSa5Wx9ibh/4q/LH5nNivBqASS/2BKyTGGmKsKgs7C3LWAcMvkkYCW6rhRJISCkV/ZHFupqnE735vMqLvhQTmop7JsWPC9KgQ0'}}]
layer1=raw_text[0]
print(layer1["text"])
eel.start('index.html', size=(400, 300), mode="firefox")
