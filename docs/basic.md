# Motivation

Current flashcard systems such as anki have room for improvement. The first issue is the spacing algorihtm. SM-2 was created in the 80s and its simplicity makes it unlikely to be anywhere near optimal. When using anki this manifests as studying cards that are too easy or studying cards which are too hard. The simplest solution will be gathering data (based on SM-2) and tuning machine learning and statistical models with better metrics. Piotr Wozniak's blog has metrics which can be used to measure improvements.
Anothoer important change is using relational information. Current flashcards systems essentially link two pieces of information and by studying that card over time I learn the mapping A -> B (but often not the reverse). This knowledge is brittle, for example not knowing B -> A, or small changes in the card being difficult. This is due to overfitting to the specific langauge of the card and not the content. What I really want from a system is a knowledge graph of information, which serves two purposes: (1) generating novel cards and (2) reviewing cards updating learning time for similar/connected cards. (1) can be achieved in anki by writing many cards for the same topic but it's a clunky approach and weaker than algorithmic. Hopefully NLP can be encoporated in the future to generate different wordings for cards, but to start a knowledge graph with a set of node types and edge types could be use to generate a large number of cards per 'atom' (an individual concept) - based on the structure of the graph. This should reduce memorisation of the card, and increase memorisation of the concept. (2) By creating many cards for a concept, they should not be studied similtaneously, as this will result in working memory affecting the quality of recall task. In addition, similar concepts, not just generations of the same concept, should affect the review interval for a correct/incorrect response.
Another important issue I want to address is a concept called 'evergreen notes'. I first heard this term from the obsidian community, where notes are continually updates over their life span. This would make a lot of sense for a flashcard system, which often suffers from notes that go stale overtime. In addition, as new concepts are learnt and added to the knowledge graph, they should be tied back into previous knowledge.

# Goals for project

- Develop a simple ui for studying flashcards
- Apply machine learning to find more efficient study intervals
- Descriptive statistics page
- Generative flashcards
  - NLP
  - GenAI
  - Knowledge Graph
-
