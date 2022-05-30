# Advanced PII detection and anonymization with Hugging Face Transformers and Amazon SageMaker


repository [philschmid/advanced-pii-huggingface-sagemaker](https://github.com/philschmid/advanced-pii-huggingface-sagemaker)

PII or Personally identifiable information (PII) is any data that could potentially identify a specific individual, e.g. to distinguish one person from another. Below are a few examples of PII:

- Name
- Address
- Date of birth
- Telephone number
- Credit Card number

Protecting PII is essential for personal privacy, data privacy, data protection, information privacy, and information security. With just a few bits of an individual's personal information, thieves can create false accounts in the person's name, incur debt, create a falsified passport or sell a person's identity to a criminal.

Transformer models are changing the world of machine learning, starting with natural language processing (NLP), and now, with audio and computer vision. Hugging Face’s mission is to democratize good machine learning and give anyone the opportunity to use these new state-of-the-art machine learning models.

Models Like BERT, RoBERTa, T5, and GPT-2 captured the NLP space and are achieving state-of-the-art results across almost any NLP tasks including, text-classification, question-answering, and token-classification. 

---

In this blog, you will learn how to use state-of-the-art Transformers models to recognize, detect and anonymize PII using Hugging Face Transformers, Presidio & Amazon SageMaker.