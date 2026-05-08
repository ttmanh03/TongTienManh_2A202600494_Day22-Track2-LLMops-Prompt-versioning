QA_PAIRS = [
    {
        "question": "What are the three main types of machine learning?",
        "answer": "The three main types of machine learning are supervised learning, unsupervised learning, and reinforcement learning."
    },
    {
        "question": "What is overfitting in machine learning?",
        "answer": "Overfitting occurs when a model learns the training data too well including its noise, resulting in poor performance on new unseen data. Signs include very low training error but high test error."
    },
    {
        "question": "Explain the bias-variance tradeoff.",
        "answer": "The bias-variance tradeoff describes the tension between bias (error from overly simplistic assumptions causing underfitting) and variance (error from sensitivity to small fluctuations causing overfitting). As model complexity increases, bias decreases but variance increases."
    },
    {
        "question": "How does regularization prevent overfitting?",
        "answer": "Regularization adds a penalty term to the loss function to prevent overfitting. L1 (Lasso) promotes sparsity, L2 (Ridge) keeps weights small, and Dropout randomly deactivates neurons during training."
    },
    {
        "question": "What is cross-validation?",
        "answer": "Cross-validation is a technique for evaluating model performance on unseen data. K-fold cross-validation divides data into k subsets, trains on k-1 folds and tests on the remaining fold, repeating k times to provide more reliable performance estimates."
    },
    {
        "question": "What is backpropagation?",
        "answer": "Backpropagation is the algorithm used to train neural networks. It computes gradients of the loss function with respect to each weight using the chain rule of calculus, flowing gradients backwards from output to input layers so optimizers can update weights."
    },
    {
        "question": "What are Convolutional Neural Networks primarily used for?",
        "answer": "Convolutional Neural Networks (CNNs) are primarily used for image recognition, object detection, and computer vision tasks. They use convolutional layers to detect local features like edges, textures, and shapes, and share weights across spatial locations."
    },
    {
        "question": "How do LSTM networks address the vanishing gradient problem?",
        "answer": "LSTM networks address the vanishing gradient problem through a gating mechanism with three gates: the forget gate, input gate, and output gate. The cell state acts as long-term memory that can carry information across many time steps, enabling LSTMs to learn long-range dependencies."
    },
    {
        "question": "What activation functions are commonly used in neural networks?",
        "answer": "Common activation functions include ReLU (max(0,x)) widely used in hidden layers, Sigmoid for binary classification output (0,1), Tanh for outputs in (-1,1), and Softmax for multi-class classification. Leaky ReLU and GELU are variants that address ReLU's dying neuron problem."
    },
    {
        "question": "What is the role of pooling layers in CNNs?",
        "answer": "Pooling layers in CNNs reduce the spatial dimensions of feature maps, providing translation invariance and reducing computation. Max pooling takes the maximum value in each window preserving prominent features, while average pooling takes the mean for smoother downsampling."
    },
    {
        "question": "What is the transformer architecture?",
        "answer": "The transformer architecture, introduced in Attention Is All You Need (2017), relies entirely on attention mechanisms without recurrence. It consists of an encoder and decoder with multi-head self-attention layers and feed-forward networks, using positional encodings to inject sequence order information."
    },
    {
        "question": "What are word embeddings?",
        "answer": "Word embeddings are dense vector representations of words that capture semantic meaning, where words with similar meanings have similar vectors. Word2Vec uses CBOW or Skip-gram approaches, GloVe combines global statistics with local context, and contextual embeddings from BERT and GPT vary by context."
    },
    {
        "question": "What is transfer learning in NLP?",
        "answer": "Transfer learning in NLP involves pretraining a language model on a large corpus to learn general language representations, then fine-tuning on a specific downstream task with a smaller labeled dataset. This reduces the need for task-specific labeled data. BERT, GPT, and T5 are common pretrained models."
    },
    {
        "question": "How does BERT handle language understanding?",
        "answer": "BERT handles language understanding through masked language modeling and next sentence prediction pretraining. It is bidirectional, considering both left and right context simultaneously. During fine-tuning, a task-specific head is added on top of BERT contextual representations, achieving state-of-the-art on GLUE and SQuAD."
    },
    {
        "question": "What is self-attention in transformers?",
        "answer": "Self-attention allows each token in a sequence to attend to all other tokens by computing a weighted sum of their value vectors. Queries, keys, and values are computed for each token, and the attention score is the dot product of query and key vectors, scaled and passed through softmax. Multi-head attention runs multiple attention operations in parallel."
    },
    {
        "question": "What is GPT and how is it trained?",
        "answer": "GPT (Generative Pre-trained Transformer) uses a decoder-only transformer architecture trained with causal language modeling, predicting the next token given all previous tokens. GPT-3 has 175 billion parameters, and GPT-4 further improved reasoning and multimodal capabilities. GPT models are autoregressive, generating text one token at a time."
    },
    {
        "question": "What is instruction tuning?",
        "answer": "Instruction tuning fine-tunes a pretrained language model on diverse tasks formatted as natural language instructions and responses. This helps models follow user instructions more reliably across tasks. Models like InstructGPT, FLAN-T5, and Alpaca use instruction tuning to improve helpfulness and generalization."
    },
    {
        "question": "What is RLHF?",
        "answer": "RLHF (Reinforcement Learning from Human Feedback) aligns language models with human preferences through three steps: supervised fine-tuning on demonstrations, training a reward model from human comparisons of outputs, and using RL (typically PPO) to optimize the language model against the reward model. It is used in ChatGPT and Claude."
    },
    {
        "question": "What is chain-of-thought prompting?",
        "answer": "Chain-of-thought prompting encourages language models to produce intermediate reasoning steps before giving a final answer. By including step-by-step reasoning examples in the prompt, models solve complex multi-step problems more accurately. Zero-shot chain-of-thought adds the phrase let us think step by step to the prompt."
    },
    {
        "question": "What is the context length of GPT-4?",
        "answer": "GPT-4 has a context length of up to 128,000 tokens in its extended version, allowing it to process very long documents. The standard GPT-4 context window is 8,192 tokens. Context length determines how much text the model can consider at once for tasks like summarization and question answering."
    },
    {
        "question": "What is Retrieval-Augmented Generation?",
        "answer": "Retrieval-Augmented Generation (RAG) enhances language model outputs by retrieving relevant information from external knowledge sources at inference time. Instead of relying solely on knowledge in model parameters, RAG dynamically retrieves documents and provides them as context to the LLM, reducing hallucination and enabling access to up-to-date or private knowledge."
    },
    {
        "question": "What are the main components of a RAG pipeline?",
        "answer": "The main components of a RAG pipeline are: a document ingestion pipeline that splits, embeds, and indexes documents; a retriever that finds relevant chunks given a query; a prompt template that formats the retrieved context and question; an LLM that generates answers conditioned on the context; and an output parser."
    },
    {
        "question": "What is dense retrieval?",
        "answer": "Dense retrieval uses neural text embeddings to represent both queries and documents as dense vectors in a shared semantic space. Similarity is measured by cosine similarity or dot product. Models like DPR, E5, and OpenAI text-embedding-3 produce meaningful dense representations. Dense retrieval captures semantic similarity better than keyword matching."
    },
    {
        "question": "Why is chunking strategy important in RAG?",
        "answer": "Chunking strategy in RAG is critical because it determines how documents are split for indexing and retrieval. Chunks too large may include irrelevant information; too small may miss context. Chunk size of 256-512 tokens with 10-20 percent overlap is a common starting point, with the optimal strategy depending on document type and query characteristics."
    },
    {
        "question": "What advanced RAG techniques exist beyond basic retrieval?",
        "answer": "Advanced RAG techniques include HyDE (Hypothetical Document Embeddings) which generates a hypothetical answer to improve retrieval, query decomposition for multi-hop questions, re-ranking with cross-encoders, recursive retrieval, FLARE which generates retrieval queries during generation, and self-RAG which trains models to decide when to retrieve."
    },
    {
        "question": "What are vector databases used for?",
        "answer": "Vector databases store, index, and search high-dimensional vector embeddings efficiently. They enable semantic similarity search at scale. Use cases include semantic search, recommendation systems, RAG pipelines, image similarity search, and anomaly detection. Popular vector databases include Pinecone, Weaviate, Qdrant, Milvus, and Chroma."
    },
    {
        "question": "What is FAISS?",
        "answer": "FAISS (Facebook AI Similarity Search) is an open-source library for efficient similarity search and clustering of dense vectors. It provides multiple index types including Flat (exact), IVF (approximate), HNSW, and PQ. FAISS is highly optimized for CPU and GPU, supporting billion-scale vector search, and is widely used in production RAG systems."
    },
    {
        "question": "How do text embeddings capture semantic meaning?",
        "answer": "Text embeddings capture semantic meaning by mapping text to high-dimensional vectors such that semantically similar texts are close in the embedding space. They are trained using contrastive learning where similar texts are pulled together and dissimilar texts are pushed apart, enabling semantic search, clustering, and nearest-neighbor retrieval."
    },
    {
        "question": "What is HNSW?",
        "answer": "HNSW (Hierarchical Navigable Small World) is a graph-based approximate nearest neighbor algorithm. It builds a multi-layer graph where the top layer has few nodes with long-range edges for fast navigation and lower layers have more nodes with local edges for refinement. HNSW achieves high recall with low latency and is widely used in production vector databases."
    },
    {
        "question": "What is hybrid search in vector databases?",
        "answer": "Hybrid search combines dense vector search with sparse keyword search like BM25 to leverage strengths of both approaches. Dense search captures semantic similarity; sparse search handles exact keyword matching and rare terms. Results are merged using reciprocal rank fusion or weighted combination. Hybrid search often outperforms either approach alone."
    },
    {
        "question": "What is LangChain?",
        "answer": "LangChain is an open-source framework for building applications with large language models. It provides abstractions for chains, agents, memory, retrievers, tools, and callbacks. LangChain enables composing LLM calls with external data sources, APIs, and computational tools, supporting many LLM providers and vector databases."
    },
    {
        "question": "What is LangChain Expression Language (LCEL)?",
        "answer": "LangChain Expression Language (LCEL) is a declarative interface for composing LangChain components into chains using the pipe operator. Each component receives the output of the previous one. LCEL chains support streaming by default, are parallelizable, and provide full observability through LangSmith."
    },
    {
        "question": "What is LangGraph?",
        "answer": "LangGraph is a library built on LangChain for building stateful multi-actor applications with LLMs. It models workflows as graphs with nodes for processing steps and edges for transitions. LangGraph supports cycles, conditional branching, and persistent state, enabling complex agent workflows, multi-agent systems, and human-in-the-loop applications."
    },
    {
        "question": "What memory types does LangChain support?",
        "answer": "LangChain supports ConversationBufferMemory (stores full history), ConversationBufferWindowMemory (stores last k turns), ConversationSummaryMemory (stores a running summary), EntityMemory (tracks mentioned entities), and VectorStoreRetrieverMemory (stores memories in a vector store for semantic retrieval)."
    },
    {
        "question": "What are LangChain retrievers?",
        "answer": "LangChain retrievers are components that return relevant documents given a query. Types include VectorStoreRetriever for nearest-neighbor search, MultiQueryRetriever which generates multiple queries, ContextualCompressionRetriever which compresses results, EnsembleRetriever which combines multiple retrievers, and SelfQueryRetriever which converts natural language filters to structured queries."
    },
    {
        "question": "What is LangSmith?",
        "answer": "LangSmith is an observability and evaluation platform for LLM applications built by the LangChain team. It provides tracing, debugging, testing, evaluation, and monitoring capabilities. LangSmith captures every LLM call with full input and output data, latency, token usage, and cost, and integrates natively with LangChain via the @traceable decorator."
    },
    {
        "question": "What information do LangSmith traces capture?",
        "answer": "LangSmith traces capture input and output at every step of a chain, latency for each component, token counts and estimated cost, error messages and stack traces, run metadata like tags and key-value pairs, retrieval results including retrieved documents, and model parameters. Traces are organized hierarchically showing parent-child relationships between chain steps."
    },
    {
        "question": "What is the LangSmith Prompt Hub?",
        "answer": "The LangSmith Prompt Hub is a versioned prompt management system that allows teams to store, version, and share prompt templates. Prompts are pushed via client.push_prompt() and pulled via client.pull_prompt(). Each push creates a new version enabling rollback, and teams can compare prompt versions to track which version is in production."
    },
    {
        "question": "How does LangSmith help monitor production LLM applications?",
        "answer": "LangSmith helps monitor production LLM applications through real-time dashboards showing latency percentiles, error rates, and token usage. It supports custom feedback logging, configurable alerting for error spikes or latency thresholds, and allows collecting production traces into datasets for regression testing and evaluation."
    },
    {
        "question": "What are LangSmith datasets used for?",
        "answer": "LangSmith datasets are curated collections of input-output examples used for testing and evaluation. They can be created manually, by uploading CSV or JSON files, or by adding traces from the monitoring UI. Datasets are used for regression testing, fine-tuning data collection, prompt comparison experiments, and evaluation benchmark creation."
    },
    {
        "question": "What is RAGAS?",
        "answer": "RAGAS (Retrieval-Augmented Generation Assessment) is an open-source framework for evaluating RAG pipelines. It provides metrics that assess different aspects of RAG quality using LLMs as evaluators. Key metrics include faithfulness, answer relevancy, context recall, and context precision. RAGAS helps identify which component of a RAG pipeline needs improvement."
    },
    {
        "question": "How does RAGAS compute faithfulness?",
        "answer": "RAGAS computes faithfulness by measuring whether every claim in the generated answer can be inferred from the retrieved contexts. It extracts claims from the answer using an LLM, then checks whether each claim is supported by the context. The faithfulness score is the fraction of claims that are supported by the retrieved context."
    },
    {
        "question": "What is answer relevancy in RAGAS?",
        "answer": "Answer relevancy in RAGAS measures how directly the generated answer addresses the original question. It generates multiple hypothetical questions from the answer using an LLM, then measures the average cosine similarity between these hypothetical questions and the original question. A high score means the answer directly addresses what was asked."
    },
    {
        "question": "What is context recall in RAGAS?",
        "answer": "Context recall in RAGAS measures how much of the information in the reference answer is covered by the retrieved contexts. It decomposes the reference answer into individual claims and checks whether each claim can be attributed to the retrieved context. A high context recall means the retriever successfully retrieved documents containing ground-truth information."
    },
    {
        "question": "What inputs does RAGAS evaluation require?",
        "answer": "RAGAS evaluation requires for each sample: user_input (the question), response (the generated answer from the LLM), retrieved_contexts (list of retrieved text chunks), and optionally reference (ground-truth answer required for context recall and context precision). These are encapsulated in SingleTurnSample objects and collected into an EvaluationDataset."
    },
    {
        "question": "What is Guardrails AI?",
        "answer": "Guardrails AI is a Python framework for adding input and output validation to LLM applications. It provides a declarative way to define validators that check and optionally repair LLM outputs. Validators can detect PII, enforce JSON schemas, check for toxicity, and more. Custom validators are created by subclassing Validator and using @register_validator."
    },
    {
        "question": "What is PII and why is it important to detect in LLM responses?",
        "answer": "PII (Personally Identifiable Information) includes data that can identify a specific individual such as email addresses, phone numbers, social security numbers, and credit card numbers. Detecting and redacting PII in LLM responses is important for privacy compliance (GDPR, HIPAA), preventing data leakage, and protecting users from harm."
    },
    {
        "question": "What does structured output validation ensure?",
        "answer": "Structured output validation ensures that LLM responses conform to an expected format such as valid JSON. LLMs sometimes produce malformed JSON with trailing commas or single quotes, or wrap JSON in markdown code fences. Validators detect these issues and attempt auto-repair, which is critical when LLM responses are parsed programmatically by downstream systems."
    },
    {
        "question": "What is Constitutional AI?",
        "answer": "Constitutional AI (CAI) is a technique developed by Anthropic for training AI systems to be helpful, harmless, and honest using a set of principles called a constitution. During training the model critiques and revises its own outputs according to these principles. CAI uses a self-improvement loop to identify and correct harmful or unhelpful responses."
    },
    {
        "question": "What are common AI safety concerns with LLMs?",
        "answer": "Common AI safety concerns with LLMs include hallucination (generating false information confidently), bias amplification (reflecting societal biases from training data), prompt injection (malicious inputs overriding instructions), jailbreaking (bypassing safety guidelines), privacy leakage, and toxic content generation. Mitigations include RLHF, constitutional AI, red-teaming, and output guardrails."
    },
]

QUESTIONS = [pair["question"] for pair in QA_PAIRS]
ANSWERS   = [pair["answer"]   for pair in QA_PAIRS]
