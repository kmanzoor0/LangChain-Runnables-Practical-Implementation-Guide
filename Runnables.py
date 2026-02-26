#✅ 1️⃣ RunnableSequence (Linear Flow)
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model_name="llama-3.1-8b-instant")

prompt = ChatPromptTemplate.from_template(
    "Write a short joke about {topic}"
)

parser = StrOutputParser()

sequence = RunnableSequence(prompt, model, parser)

result = sequence.invoke({"topic": "AI"})
print(result)

#👉 Runs step-by-step: prompt → model → parser

#✅ 2️⃣ RunnableParallel (Runs Multiple Chains Together)
from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

joke_prompt = ChatPromptTemplate.from_template(
    "Tell a joke about {topic}"
)

explain_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple words"
)

joke_chain = joke_prompt | model | StrOutputParser()
explain_chain = explain_prompt | model | StrOutputParser()

parallel = RunnableParallel(
    joke=joke_chain,
    explanation=explain_chain
)

result = parallel.invoke({"topic": "AI"})
print(result)

#👉 Returns dictionary:

{
  "joke": "...",
  "explanation": "..."
}
#✅ 3️⃣ RunnableBranch (Conditional Execution)
from langchain_core.runnables import RunnableBranch

joke_chain = (
    ChatPromptTemplate.from_template("Tell a joke about {input}")
    | model
    | StrOutputParser()
)

fact_chain = (
    ChatPromptTemplate.from_template("Give a fact about {input}")
    | model
    | StrOutputParser()
)

branch = RunnableBranch(
    (lambda x: "joke" in x["input"].lower(), joke_chain),
    fact_chain  # default chain
)

print(branch.invoke({"input": "tell me a joke about AI"}))
print(branch.invoke({"input": "AI"}))

#👉 If condition true → joke_chain
#👉 Otherwise → fact_chain

#✅ 4️⃣ RunnablePassthrough (Pass Input Forward)

#Used when you want to keep original input while modifying it.

from langchain_core.runnables import RunnablePassthrough

chain = RunnablePassthrough() | (
    ChatPromptTemplate.from_template(
        "Rewrite this in a polite tone: {input}"
    )
    | model
    | StrOutputParser()
)

print(chain.invoke("Give me your report now"))

#👉 RunnablePassthrough() forwards original input unchanged.