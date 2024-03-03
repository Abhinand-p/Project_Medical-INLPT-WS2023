# Project_Medical_INLPT_WS2023
## Key Informtion
Your report needs to give the following information:
● Title: The final title of your project.
### Team Members
1. Abhinand Poosarala, Abhinand-p
2. Behrooz Montazeran, 3769073, behrooz.montazeran@stud.uni-heidelberg.de, BehroozMontazeran
3. Hussein Abdulreda, 3769915, HRida
4. John Hildenbrand, Johncrtz

* Adisor: Ashish Chouhan
* Anti-plagiarism Confirmation: 
By submitting this work, We confirm that it is entirely our own original creation and that We have not plagiarized any material from any source. We have cited all sources used appropriately, and any similarities found with existing works are purely coincidental. We understand that any form of plagiarism is strictly prohibited and may result in severe consequences, including academic penalties.

* Responsibilities:

| Data Acquisition | Data Preprocessing | Data Retrieval | Fronend | Backend | ... |

|--------------------|----------------------|-----------------|-----------|----------|---|

| Abhinand---------| Behrooz------------| all-------------  | John------| John----| Cell 6   |

| Behrooz-----------| ---------------------| ---------------  | Hussein--   | Hussein   | Cell 6   |


## Introduction
In an era dominated by vast amounts of scientific literature, accessing and comprehending relevant information poses a significant challenge for researchers and professionals. Our project addresses this issue by implementing a Retrieval Augmented Generation (RAG) system connected to GPT-3.5 and Llama 2, a state-of-the-art language model developed by OpenAI and Meta. This system aims to facilitate the extraction and synthesis of information from articles containing 'Intelligence' hosted on PubMed [1], a widely used database of biomedical literature.

The primary objective of our project is to provide an intuitive and efficient means for users to query articles stored from PubMed and receive comprehensive and contextually relevant answers to their questions. As none of the LLMs are working with updated data, they all suffer from providing answers based on most recent information. By leveraging the capabilities of GPT-3.5 and integrating it with a retrieval mechanism, we empower users to pose natural language queries and obtain synthesized responses tailored to their information needs based on most recent data.

In this report, we provide an overview of our project, including its motivation, methodology, and implementation details. We outline the key concepts and techniques employed in our approach, offering insights into how the integration of GPT-3.5 and PubMed enhances the information retrieval and synthesis process. Furthermore, we present the results of our experiments and evaluations, showcasing the effectiveness and performance of our RAG system. Finally, we discuss potential applications, limitations, and future directions for extending and refining our approach to meet evolving user needs and technological advancements.



"""The first section should explain what your project is all about, why the project and underlying
problems are interesting and relevant, and it should outline the rest of your report. The
introduction also outlines the key ideas of your approach without going into the details in
terms of realization and implementation. It is also possible to give an outlook of the results
the reader can expect to see in the later sections."""
## Related Work








"""This section of your report covers core prior work related to your project, and puts your work
into the context of current research. This includes papers that you used as a basis for your
approach or papers that used the same techniques as you did but applied them to a different
problem. In this section, you should emphasize how your work differs from previous work,
e.g., by outlining the limitations of previous work, or why your application domain is
different from those other researchers have already investigated. However, you should not go
into all the details about any of the work you cite, instead, you should outline how the major
points of previous work relate to your project."""
## Methods/Approach
In the following parts all the methods that are used to accomplish the final project are addressed. Those, that are labeled as [Outdated] are part of experiment we did but not used in the final product.

### Data Acquisition
From the pubmed section intelligence [2], we gathered abstracts between 2013-2023 that contains term 'Intelligence' from pubmed. To do this we provided different technique that is clarified as follow:

1. API:
   - By this approach we downloaded the xml file, which was later processed and the usefull data extracted, using the preprocessing notbook, and finally the csv file of the related data was created. As the whole dataset was too big to be pushed to github, we used hugging-face to host our dataset. This also changed later by storing the dataset and their embedding on opensearch.

2. Crawler:[Outdated]
   - Using this method we implement a crawler using selenium to extract each abstract, its title and the respective authors from Pubmed one by one.

### Data Preprocessing
   During this phase of the project, we engaged in the utilization of XML files sourced from Pubmed, aiming to extract a comprehensive set of 17 metadata attributes accompanied by their corresponding data points. Subsequently, in the subsequent phase, we proceeded to curate an additional dataset comprising solely the unique identifiers (PMID) alongside amalgamated columns encompassing abstracts, titles, publication dates, author information, medical subject headings pertinent to each abstract, and journal titles. The construction of this refined dataset facilitates enhanced analytical capabilities, thereby enabling the exploration and resolution of a wider array of inquiries, as delineated in our project objectives [Types of Questions and Answers](#Types-of-Questions-and-Answers). This augmentation of data granularity and scope contributes to the enrichment of our research endeavors, fostering deeper insights and robust conclusions within the domain under investigation.
### Data Storage
1. Opensearch: Cloud based

2. OpenSearch [3], a cloud-based platform:
    adopts a split approach for efficient management of data. Regarding storage, the utilization of diverse embedding models necessitated the segmentation of dataset contexts due to the limitations imposed by maximum length constraints. Consequently, each abstract's context was partitioned into chunks, each identified by a relative ID format, such as PMID-chunk_number. These chunks, along with their associated embeddings, context, and pertinent resources, are stored within the OpenSearch infrastructure. Concerning retrieval, a hybrid search methodology is employed, leveraging the capabilities of OpenSearch to retrieve the k most relevant pieces of data efficiently. This approach enhances the effectiveness of information retrieval within the system, facilitating optimized access to pertinent information. Further exploration of the mechanisms underlying this hybrid search strategy may shed light on its efficacy and potential avenues for refinement and improvement.

3. Pinecone: Cloud based, split approach[Outdated]
   - Storage: Uploading embedding vectors on cloud based VectorDB (Pinecone) and respective abstract's metadata in seperate no-SQL DB (FaunaDB). Use a key to map vectors to metadata between the databases.
   - Retrieval: Retrieve a document by first finding top k matches between embedded query and stored vectors (cosine similarity) in Pinecone, use the ids from the top k matches to query text+metadata, implemented via given API keys into our servers backend/frontend



### Data Retrieval
### 1. Embeddings
#### 1. Approach
1. PubMedBERT, per-abstract embedding
   - BERT model finetuned on PubMed data, information retrieval/ QA, maps into 768 dimensional vectorspace, up to 512 token.
   - Created one embedding per abstract
     -> Turned out to be badly implemented because models max input size was not taken into consideration
2. e5-large-V2, embed chunks and store chunks in abstract
   - "E5 is a general-purpose embedding model for tasks requiring a single-vector representation of texts such as retrieval, clustering, and classification, achieving strong performance in both zero-shot and fine-tuned settings." 1024 Output dimension, 512 input size
   - Chunk abstract after 512 tokens, between each chunk of an abstract create overlapping chunks
   - Added 'local context' to each chunks metadata which is the text that appears before and after the chunk (local context appr. 20% of abstracts size). This will later on be concatinated with the chunks text so that the model in charge of answering the prompt has a better understanding of the chunk role in the abstract itself (context)
   - We embedded and stored each chunk to our vector space which resulted in appr. 68k vectors
   - Code can be found at: embedding\INLPT2023_2024.ipynb
3. One could also take the embedded chunks of an abstract and combine them by f.e. mean pooling, this way we end up with one embedding per abstarct agin
   - Not sure about the quality of the resulting embedding
### 2. Approach
   - In this methodology, drawn from the Transformer library, the AutoTokenizer module is employed to perform tokenization on the dataset utilizing the pretrained model 'sentence-transformers/all-distilroberta-v1' [4]. This process is facilitated by the 'RecursiveCharacterTextSplitter' function from the langchain.text_splitter module. Given the constraint that the maximum input length for this model is 512 tokens, yielding an output dimensionality of 768, a decision was made to partition the data into chunks of size 400, with a 50-token overlap between consecutive chunks. This strategy is implemented to preserve the contextual coherence within each abstract. The adoption of character-based splitting ensures a degree of robustness to misspellings, thereby enhancing the model's retrieval capabilities. Admittedly, chunking the data results in an increased number of units, yet it concurrently enhances the efficiency of data retrieval and search operations. This trade-off between granularity and efficiency underscores the pragmatic considerations governing the data preprocessing stage in natural language processing tasks.
### 2. TF-IDF[Outdated]
   - In this Approach we used the TfidfVectorizer from sklearn and set the analyzing level to characters which provided us the misspelling tolerance. Moreover, we used nltk to add the synonyms to the search of most k relevant abstacts. 

## Types of Questions and Answers
The provided final product can answer following questions type:
1. Confirmation Questions [yes or no]:
   - Is Moog the author of article 'CASK Disorders'?
   - 

2. Factoid-type Questions [what, which, when, who, how]:
   - Who is Moog?
   - which articles were published in 2015?
   - What is CASK Disorders?
   - How to treat the CASK Disorders?

3. List-type Questions: 
   - List the name of auhtors of article 'CASK Disorders'.
   - 

4. Causal Questions [why or how]: 
   - Why lung cancer is deadly?
   - 

5. Hypothetical Questions:
   - What would happen if CASK Disorders is not treated?
   - 

● Complex Questions:
   - What is relation of CASK Disorders in increasing the rate of breast cancer?
   - 





"""This section gives all the conceptual details of the system you developed and is intended for
readers who want to fully understand your system, its functionality, and its components. This
includes the (data) processing pipelines you realized, the algorithms you developed, and all
other key methods you designed during the project.Here’s some advice for this section:.
● Be specific about your methods. In this section, you can show your detailed
understanding of the matter. Include equations where necessary and show figures,
such that the reader can better follow and understand your approach.
● If some part of your work is original or especially creative, make it clear, such that the
reader (e.g., your mentor) can understand the novelty of your approach. You do not
need to show any false modesty in this part of your work. If you use any existing
methods, however, you need to recognize and properly cite them. Be consistent
throughout your report and stick to a fixed vocabulary before writing. This includes
mathematical terms and notations, method names, names for data sets, and the like.
Only a few things are more irritating than changing naming and writing conventions
during a report.
● If you have any baseline approaches, they should also be described. This can be
detailed if you created the baseline yourself or just briefly if there is an external
source from which you took the baseline."""

## Experimental Setup and Results







"""This section needs to cover the following information:
● Data: Describe the data you used for the project. Outline where, when, and how you
have gathered the dataset. Providing a clear understanding of the data can be very
helpful for readers to follow your analysis. If you have any interesting or insightful
metrics of your data, this is the place to show them.
● Evaluation Method: Be clear about how you are going to evaluate your project. Do
you use an existing quantitative metric? Or did you define your evaluation metric? If
you use your method, be sure to motivate what you try to achieve with it, and what it
does reflect. In any case, define your evaluation metric, be it a qualitative or
quantitative one, automatic or human-defined.
● Experimental Details: If your methods rely on configurable parameters, specify
them, such that your results are replicable. Explain why you chose the parameters in
that way (e.g., did you do some grid search?).
● Results: The results section of your report highly depends on your project. If you
have a baseline to which you can compare your approach, you obviously should do
this. In such cases, tables and plots are suitable means to present your achievements.
In any case, use the evaluation metrics defined before. Moreover, comment on your
results: are they in line with your expectations? Or are they better or worse? What are
the potential reasons for this?
● Analysis: You can include some qualitative analysis in this section. Does your system
work as expected? Are there cases in which your approach consistently succeeds in
the task, or surprisingly fails? If you have a baseline, you can also compare if they
succeed and fail in the same contexts or if your approach may be suitable for other
applications than the baseline. Underpin your points using examples or metrics
instead of stating unproven claims."""

## Conclusion and Future Work
Recap the main contributions of your project. Highlight your achievements, but also reflect
on the limitations of your work. Potentially, you can also outline how your model can be
extended or improved in the future, or you can briefly give insights into what you have
learned during the project.
## References

[1]: #ref1
[2]: #ref2
[3]: #ref3
[4]: #ref4




[National Center for Biotechnology Information. (n.d.). PubMed. Retrieved Oct. 30, 2023, from https://pubmed.ncbi.nlm.nih.gov/](#ref1)

[National Center for Biotechnology Information. (n.d.). PubMed. Retrieved Nov. 05, 2023, from https://pubmed.ncbi.nlm.nih.gov/?term=intelligence+%5BTitle%2Fabstract%5D&filter=simsearch1.fha&filter=years.2013-2023&sort=date&size=200](#ref2)

[OpenSearch. (n.d.). About OpenSearch. Retrieved Feb. 01, 2024, from https://opensearch.org/docs/latest/about/](#ref3)

[Hugging Face. (n.d.). README.md. Sentence Transformers - DistilRoBERTa, a distilled version of RoBERTa. Retrieved Feb. 01, 2024, from https://huggingface.co/sentence-transformers/all-distilroberta-v1/blame/e5e0bbabc6e2c6e494a64b5018d1b40775b173a7/README.md](#ref4)



"""List your references at the end of your report. You can add them as a list at the end of your
report and refer to the author's name and year in the text, e.g., [Gertz et al.
2020](#link-to-the-bib-section). Make sure you follow proper citation methods and include
all author's names, the name of the journal or conference, the full title of the paper, and the
publication year."""