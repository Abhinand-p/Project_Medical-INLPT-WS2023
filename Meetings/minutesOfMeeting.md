# MOM: Minutes Of Meeting

## 21 - October - 2023 12:00
| Topics           | About                                                          | Decision                |
|------------------|----------------------------------------------------------------|-------------------------|
| Repo Creation    | Creating a repo, with log file following up with the meetings. | Done                    |
| Domain Selection | Discussing between Medial and Legal Domain.                    | Choosing Medical Domain |
| UI Framework     | Discussing between Django, Flask,                              | Django                  |

### Other points
1. Familiarize our selves with the content (Text-Analytics) and techs accordingly
2. Familiarizing our selves with NLP, Transformers, (Large) Language Models
3. Check the technology stack (create a UML around it to be understandable by all)
4. Agreeing sharing the stuff we search for on the discord channels

## 11 - November - 2023 11:00
| Topics              | About                                         | Decision |
|---------------------|-----------------------------------------------|----------|
| Splitting the tasks | 4 Subtasks has been identified in the project | Done     |
| Meeting Slot        | Decide on a common meeting time               | Done     |

### Task Division
| Sub Tasks                         | Assignment                                |
|-----------------------------------|-------------------------------------------|
| Data Acquisition<br/>Data crawler | Behrooz Montazeran<br/>Abhinand Poosarala |
| Cloud-based Storage               | John Hildenbrand<br/>Hussein Abdulreda    |
| Training Search Engine            | Behrooz Montazeran<br/>Abhinand Poosarala |
| User Interface                    | John Hildenbrand<br/>Hussein Abdulreda    |

## 20 - November - 2023 20:00
| Topics                | Discussion                                                                    | 
|-----------------------|-------------------------------------------------------------------------------|
| Data Acquisition      | Discussed 3 methods(Web crawler, API method and EDirect) on data acquisition. |
| Front-end development | Saw the Front-end development of the web-page, chat-bot interaction.          |
| Overall pipeline      | Overview idea on storage, LLM, vector DB ...                                  |

### Takeaway from the meeting
1. After Data Acquisition method, post processing is needed to select the important data.
2. In front-end development, the user entered query should be processed before passing it to the LLM.

## 4 - December - 2023 20:00
| Topics                | Discussion                                                              | 
|-----------------------|-------------------------------------------------------------------------|
| Data Acquisition      | Pushed raw data to github. Next step post processing and data analysis. |
| Overall pipeline      | Pipeline diagram discussed.                                             |

### Takeaways from the meeting
1. SingleStore Vector DB
2. Bio BERT
3. Indexing and Semantic Search

## 11 - December - 2023 20:00
| Topics                                    | Status  |
|-------------------------------------------|---------|
| Post processing                           | Done    | 
| VectorDB first implementation             | Done    | 
| UI first loop                             | Ongoing |
| Questions to tutor                        | Ongoing |
| Creating custom dataset for benchmarking  | Ongoing |

### Next points to discuss 
1. Handle Mis-spelling and synonyms 
2. Identify other tasks like this so this can be put forward to the tutor
3. Types of LLMs to use
4. Finding a cloud server that hosts both the dataset and model

## 15 - December - 2023 12:30
## Tutor meeting

1. We need to change the embedding method of performing for the whole abstracts.
2. Refer the lecture to understand the question types. We have to analyze it and proceed one at a time.
3. As we are using a multiple database for a meta-data and vector database, we need to reduce the footprints as it is not preferable.
4. All decisions should be logged in the experiment section in git.
5. All team members should follow contribution tagging on the repo.
6. We should try to convert the repository to an organization so the tutor can be made to admin.
7. We should decide on the Must-to Have / Should have / Nice to have features.
8. Baselines should be created (TFIDF Retrieval / Semantic Search)
9. Utilizing ChatGPT data or about another system retrieval method to set as a baseline model.
10. The whole process experience is graded here, and the experiments have to justify the decisions.

## 8 - January - 2024 20:00
1. Discussed about the model that will be presented at the first-milestone.
2. Evaluation metrics - questions generation methods.
3. Tokenization methods - different approaches 

### Next points to discuss 
1. Implementing a local lama-2 model for question generations.
2. Implementing a template to capture questions and answers from ChatGPT to use as an evaluation metric.
3. Completing the vanilla RAG model before improving any specific tasks.

## 11 - January - 2024 13:30 First Milestone with the Tutor

### Import Points discussed:
1. Opensearch
2. Spell checker
3. Synchronization
4. Unified Database 
5. Evaluation System (100 pairs)

## 15 - January - 2024 20:00
1. Switch to move-over to opensearch as a single data source.
2. New data-set containing abstract along with metadata.
3. Evaluation techniques.
