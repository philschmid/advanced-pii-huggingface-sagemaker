
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer import AnalyzerEngine
from typing import List

from presidio_analyzer import AnalyzerEngine, EntityRecognizer, RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts
from transformers import pipeline

# load spacy model -> workaround
import os
os.system("spacy download en_core_web_lg")

# list of entities: https://microsoft.github.io/presidio/supported_entities/#list-of-supported-entities
DEFAULT_ANOYNM_ENTITIES = [
    "CREDIT_CARD",
    "CRYPTO",
    "DATE_TIME",
    "EMAIL_ADDRESS",
    "IBAN_CODE",
    "IP_ADDRESS",
    "NRP",
    "LOCATION",
    "PERSON",
    "PHONE_NUMBER",
    "MEDICAL_LICENSE",
    "URL",
    "ORGANIZATION"
]

# init anonymize engine
engine = AnonymizerEngine()

class HFTransformersRecognizer(EntityRecognizer):
    def __init__(
        self,
        model_id_or_path=None,
        aggregation_strategy="simple",
        supported_language="en",
        ignore_labels=["O", "MISC"],
    ):
        # inits transformers pipeline for given mode or path
        self.pipeline = pipeline(
            "token-classification", model=model_id_or_path, aggregation_strategy=aggregation_strategy, ignore_labels=ignore_labels
        )
        # map labels to presidio labels
        self.label2presidio = {
            "PER": "PERSON",
            "LOC": "LOCATION",
            "ORG": "ORGANIZATION",
        }

        # passes entities from model into parent class
        super().__init__(supported_entities=list(self.label2presidio.values()), supported_language=supported_language)

    def load(self) -> None:
        """No loading is required."""
        pass

    def analyze(
        self, text: str, entities: List[str] = None, nlp_artifacts: NlpArtifacts = None
    ) -> List[RecognizerResult]:
        """
        Extracts entities using Transformers pipeline
        """
        results = []

        # keep max sequence length in mind
        predicted_entities = self.pipeline(text)
        if len(predicted_entities) > 0:
            for e in predicted_entities:
                converted_entity = self.label2presidio[e["entity_group"]]
                if converted_entity in entities or entities is None:
                    results.append(
                        RecognizerResult(
                            entity_type=converted_entity, start=e["start"], end=e["end"], score=e["score"]
                        )
                    )
        return results


def model_fn(model_dir):
    transformers_recognizer = HFTransformersRecognizer(model_dir)
    # Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers
    analyzer = AnalyzerEngine()
    analyzer.registry.add_recognizer(transformers_recognizer)
    return analyzer


def predict_fn(data, analyzer):
    sentences = data.pop("inputs", data)
    if "parameters" in data:
        anonymization_entities = data["parameters"].get("entities", DEFAULT_ANOYNM_ENTITIES)
        anonymize_text = data["parameters"].get("anonymize", False)
    else:
        anonymization_entities = DEFAULT_ANOYNM_ENTITIES
        anonymize_text = False

    # identify entities
    results = analyzer.analyze(text=sentences, entities=anonymization_entities, language="en")
    # anonymize text
    if anonymize_text:
        result = engine.anonymize(text=sentences, analyzer_results=results)
        return {"anonymized": result.text}

    return {"found": [entity.to_dict() for entity in results]}
